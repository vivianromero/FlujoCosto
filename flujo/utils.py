from django.db.models import F, Case, Value, When, DecimalField, Sum, Max
from django.db import transaction
from django.db.models.functions import Coalesce
from django.conf import settings

from .models import *

from codificadores.models import OperacionDocumento, TipoProductoDepartamento, ClaseMateriaPrima
from codificadores import ChoiceClasesMatPrima, ChoiceTiposProd


def ids_documentos_versat_procesados(fecha_inicio, fecha_fin, departamento, ueb):
    # id de los documentos que se han introducido al sistema durante el mes que se está procesando, ya que en el cierre
    # mensual no se permite dejar doc del versat sin procesar
    query_doc_acept = DocumentoOrigenVersat.objects.filter(fecha_documentoversat__gte=fecha_inicio,
                                                           fecha_documentoversat__lte=fecha_fin,
                                                           documento__departamento=departamento,
                                                           documento__ueb=ueb).values(iddocversat=F('documentoversat')).\
                                                      all()

    # id de los documentos que se han rechazado en el mes que se está procesando, ya que en el cierre
    # mensual no se permite dejar doc del versat sin procesar
    query_doc_rechaz = DocumentoVersatRechazado.objects.filter(
        fecha_documentoversat__gte=fecha_inicio,
        fecha_documentoversat__lte=fecha_fin,
        ueb=ueb).values(iddocversat=F('documentoversat')).all()

    docs = query_doc_acept.union(query_doc_rechaz)
    ids = [i['iddocversat'] for i in docs]
    return ids


@transaction.atomic
def dame_valor_anterior(doc, docs_en_edicion):
    # docum anteriores al actual que tienen el producto
    # docs_anteriors = docs_en_edicion.filter(documento__numeroconsecutivo__lt=doc.numeroconsecutivo)
    docs_anteriors = docs_en_edicion.filter(documento__numeroconsecutivo__lt=doc.numeroconsecutivo).order_by(
        'documento__numeroconsecutivo')

    # se obtiene el total del producto se suman las entradas y se restan las salidas
    total_anterior = docs_anteriors.annotate(
        adjusted_quantity=Case(
            When(documento__tipodocumento__operacion=OperacionDocumento.ENTRADA, then=F('cantidad')),
            When(documento__tipodocumento__operacion=OperacionDocumento.SALIDA, then=-F('cantidad')),
            default=Value(0),
            output_field=DecimalField()
        )
    ).aggregate(
        total_ant=Coalesce(Sum('adjusted_quantity'), Value(0), output_field=DecimalField())
    )['total_ant']
    return total_anterior


@transaction.atomic
def actualiza_existencias(doc, docs_en_edicion, existencia_product):
    docs_posteriores = docs_en_edicion.filter(documento__numeroconsecutivo__gt=doc.numeroconsecutivo).order_by(
        'documento__numeroconsecutivo')

    documento_detalles = []
    documento_error = []
    error = False

    docs = Documento.objects.select_for_update().filter(pk__in=[x.documento.pk for x in docs_posteriores])

    for p in docs_posteriores:
        operacion = p.documento.operacion
        existencia_product = float(p.cantidad) * operacion + float(existencia_product)
        error = True if existencia_product < 0 else False
        p.existencia = existencia_product if not error else p.existencia
        doc = p.documento
        doc.error = error
        documento_detalles.append(p)
        documento_error.append(doc)

    docs_posteriores.bulk_update(documento_detalles, ['existencia'])
    docs.bulk_update(documento_error, ['error'])


@transaction.atomic
def genera_numero_doc(departamento, ueb, tipodoc):
    config = settings.NUMERACION_DOCUMENTOS_CONFIG
    consecutivo_conf = config[TipoNumeroDoc.NUMERO_CONSECUTIVO]
    control_conf = config[TipoNumeroDoc.NUMERO_CONTROL]

    numeros_consec_control = [(), ()]

    # se bloquea el registro que lleva el control de los numeros de los documentos
    prefijo = ''
    tipo = TipoDocumento.objects.get(pk=tipodoc)
    if control_conf['prefijo']:
        # tipo = TipoDocumento.objects.get(pk=tipodoc)
        prefijo = tipo.prefijo

    numeros_consec_control[0] = (1, consecutivo_conf['sistema'], '', consecutivo_conf)
    numeros_consec_control[1] = (1, control_conf['sistema'], prefijo, control_conf)

    numeros = NumeroDocumentos.objects.select_for_update().filter(ueb=ueb)

    if numeros:
        numeros_consec_control[0] = dame_numero(numeros, consecutivo_conf, departamento,
                                                TipoNumeroDoc.NUMERO_CONSECUTIVO, '')
        numeros_consec_control[1] = dame_numero(numeros, control_conf, departamento, TipoNumeroDoc.NUMERO_CONTROL,
                                                prefijo)

    if tipo.generado: # si el doc es generado se actualiza los numeros para evitar sea tomado por otro proceso
        actualiza_nros = [NumeroDocumentos(ueb=ueb, numero=numeros_consec_control[0][0], tiponumero=TipoNumeroDoc.NUMERO_CONSECUTIVO,
                                           departamento=departamento),
                          NumeroDocumentos(ueb=ueb, numero=numeros_consec_control[1][0], tiponumero=TipoNumeroDoc.NUMERO_CONTROL,
                                           departamento=departamento)
                          ]
        NumeroDocumentos.objects.bulk_update_or_create(actualiza_nros,
                                                       ['ueb', 'numero', 'tiponumero',
                                                        'departamento'],
                                                       match_field=['ueb', 'departamento', 'tiponumero'])

    return numeros_consec_control


def dame_numero(numeros, conf, departamento, tiponumero, prefijo):
    dicc_filter = {'tiponumero': tiponumero}
    if conf['departamento']:
        dicc_filter['departamento'] = departamento
    numeros_ = numeros.filter(**dicc_filter)
    if numeros_.exists():
        return (numeros_[0].numero + 1, conf['sistema'], '' if not prefijo else prefijo, conf)
    return (1, conf['sistema'], prefijo, conf)


@transaction.atomic
def actualiza_numeros(ueb, departamento, consecutivo, control, pk):
    dicc_filter_consec = {'tiponumero':TipoNumeroDoc.NUMERO_CONSECUTIVO}
    dicc_filter_control = {'tiponumero':TipoNumeroDoc.NUMERO_CONTROL}

    config = settings.NUMERACION_DOCUMENTOS_CONFIG
    config_fechas = settings.FECHAS_PROCESAMIENTO
    consecutivo_conf = config[TipoNumeroDoc.NUMERO_CONSECUTIVO]
    control_conf = config[TipoNumeroDoc.NUMERO_CONTROL]

    departamento_consec = None
    departamento_control = None

    docs_consec = None
    docs_control = None

    dicc_filter = {'ueb': ueb}

    if config_fechas and ueb in config_fechas.keys() and departamento in config_fechas[ueb].keys():
        fecha_procesamiento = config_fechas[ueb][departamento]['fecha_procesamiento']
        dicc_filter.update({'fecha': fecha_procesamiento})

    if config[TipoNumeroDoc.NUMERO_CONSECUTIVO]['departamento']:
        dicc_filter.update({'departamento': departamento})
        dicc_filter_consec.update({'departamento': departamento})

    docs_consec = Documento.objects.select_for_update().filter(**dicc_filter).exclude(pk=pk)

    if not docs_consec and pk==None: #cuando es eliminar
        NumeroDocumentos.objects.select_for_update().filter(**dicc_filter_consec).delete()
        NumeroDocumentos.objects.select_for_update().filter(**dicc_filter_control).delete()
        return

    if config[TipoNumeroDoc.NUMERO_CONTROL]['departamento']:
        dicc_filter.update({'departamento': departamento})
        dicc_filter_control.update({'departamento': departamento})

    docs_control = Documento.objects.select_for_update().filter(**dicc_filter).exclude(pk=pk)

    max_consec = docs_consec.aggregate(numeromax=Max('numeroconsecutivo', default=0))['numeromax']

    if consecutivo and consecutivo>max_consec:
        max_consec = consecutivo

    max_control = 0 if not pk else control

    for p in docs_control:
        ncontrol = p.get_numerocontrol()
        max_control = ncontrol if ncontrol > max_control else max_control

    actualiza_nros = [NumeroDocumentos(ueb=ueb, numero=max_consec, tiponumero=TipoNumeroDoc.NUMERO_CONSECUTIVO,
                                       departamento=departamento),
                      NumeroDocumentos(ueb=ueb, numero=max_control, tiponumero=TipoNumeroDoc.NUMERO_CONTROL,
                                       departamento=departamento)
                      ]
    NumeroDocumentos.objects.bulk_update_or_create(actualiza_nros,
                                                   ['ueb', 'numero', 'tiponumero',
                                                    'departamento'],
                                                   match_field=['ueb', 'departamento', 'tiponumero'])

    return


def dame_productos(documentopadre, queryproductos):
    departamento = documentopadre.departamento
    tipoproducto = []
    claseproducto = []
    productos = departamento.departamentoproductoentrada.all() if documentopadre.tipodocumento.operacion == OperacionDocumento.ENTRADA else departamento.departamentoproductosalida.all()
    for p in productos:
        match p.pk:
            case TipoProductoDepartamento.MATERIAPRIMA:
                claseproducto = [x.pk for x in ClaseMateriaPrima.objects.filter(capote_fortaleza__in=['C', 'F', 'P'])]
            case TipoProductoDepartamento.CAPASINCLASIFICAR:
                claseproducto.append(ChoiceClasesMatPrima.CAPASINCLASIFICAR)
            case TipoProductoDepartamento.CAPACLASIFICADA:
                claseproducto.append(ChoiceClasesMatPrima.CAPACLASIFICADA)
            case TipoProductoDepartamento.PESADA:
                tipoproducto.append(ChoiceTiposProd.PESADA)
            case TipoProductoDepartamento.LINEASINTERMINAR:
                tipoproducto.append(ChoiceTiposProd.LINEASINTERMINAR)
            case TipoProductoDepartamento.LINEASALIDA:
                tipoproducto.append(ChoiceTiposProd.LINEASALIDA)
            case TipoProductoDepartamento.VITOLA:
                tipoproducto.append(ChoiceTiposProd.VITOLA)

    return queryproductos.filter(Q(tipoproducto__in=tipoproducto) |
                                 Q(productoflujoclase_producto__clasemateriaprima__in=claseproducto))


@transaction.atomic
def existencia_anterior(doc, producto, elimina):
    producto = DocumentoDetalle.objects.select_for_update().get(pk=producto)
    existencia = producto.existencia
    cantidad = producto.cantidad
    operacion = doc.operacion
    ueb = doc.ueb
    existencia_product = existencia if not elimina else float(existencia) - float((cantidad * operacion))
    dicc = {'documento__estado': EstadosDocumentos.EDICION,
            'documento__departamento': doc.departamento, 'producto': producto.producto,
            'estado': producto.estado, 'documento__ueb': ueb}

    docs_en_edicion = DocumentoDetalle.objects.select_for_update().filter(**dicc)

    actualiza_existencias(doc, docs_en_edicion, existencia_product)


@transaction.atomic
def existencia_producto(docs_en_edicion, doc, producto, estado, cantidad):
    departamento = doc.departamento
    ueb = doc.ueb
    operacion = doc.operacion
    existencia = ExistenciaDpto.objects.select_for_update().filter(departamento=departamento, estado=estado,
                                                                   producto=producto, ueb=ueb)
    importe_exist = 0.00
    cantidad_existencia = 0.00

    if existencia:
        exist = existencia.first()
        importe_exist = exist.importe
        cantidad_existencia = exist.cantidad_final

    total_anterior = dame_valor_anterior(doc, docs_en_edicion)

    # se actualiza la existencia del producto en el detalle actual
    existencia_product = float(cantidad_existencia) + float(cantidad) * operacion + float(
        total_anterior)

    return existencia_product


@transaction.atomic
def actualiza_existencias_anteriores(numeroconsecutivo, numeroconcecutivo_anterior, docs_en_edicion,
                                     producto):

    existencia_product = producto.existencia
    cantidad = producto.cantidad
    operacion = producto.documento.operacion
    existencia_anterior = float(existencia_product) - (operacion * float(cantidad))
    docs_anteriores = docs_en_edicion.filter(documento__numeroconsecutivo__lt=numeroconsecutivo,
                                             documento__numeroconsecutivo__gt=numeroconcecutivo_anterior).\
                                      order_by('-documento__numeroconsecutivo')

    documento_detalles = []
    documento_error = []
    error = False

    docs = Documento.objects.select_for_update().filter(pk__in=[x.documento.pk for x in docs_anteriores])

    for p in docs_anteriores:
        error = True if existencia_anterior < 0 else False
        p.existencia = existencia_anterior if not error else p.existencia

        operacion = p.documento.operacion
        existencia_product = p.existencia
        cantidad = p.cantidad
        existencia_anterior = float(existencia_anterior) - (operacion * float(p.cantidad)) if not error else existencia_product

        doc = p.documento
        doc.error = error
        documento_detalles.append(p)
        documento_error.append(doc)

    docs_anteriores.bulk_update(documento_detalles, ['existencia'])
    docs.bulk_update(documento_error, ['error'])
