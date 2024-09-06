import base64
import json
from decimal import *

import sweetify
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from codificadores.models import FichaCostoFilas, TipoNumeroDoc, TipoDocumento, FechaInicio, NumeracionDocumentos, \
    ConfiguracionesGen
from flujo.models import FechaPeriodo, Documento, NumeroDocumentos
from django.db.models import Q, Max, F
from django.db import transaction

KEY_ENCRIP = "DATAZUCAR-ETTVC-SISGESFC"


def codificar(clear):
    enc = []
    key = KEY_ENCRIP
    for i in range(len(clear)):
        key_c = key[i % len(key)]
        enc_c = chr((ord(clear[i]) + ord(key_c)) % 256)
        enc.append(enc_c)

    return base64.urlsafe_b64encode((''.join(enc)).encode("utf-8", "replace")).decode()


def decodificar(enc):
    dec = []
    enc = (base64.urlsafe_b64decode(enc)).decode("utf-8", "replace")
    key = KEY_ENCRIP
    for i in range(len(enc)):
        key_c = key[i % len(key)]
        dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
        dec.append(dec_c)

    return ''.join(dec)


def obtener_version():
    app_version_file = open(settings.APP_VERSION, 'r')
    valor = app_version_file.read()

    return decodificar(valor)


def obtener_numero_fila(pk_padre):
    if pk_padre:
        padre = FichaCostoFilas.objects.get(pk=pk_padre)
        fila = padre.children.all().aggregate(ultima=Max('fila'))['ultima']
        numero = int(fila.split('.')[1]) + 1 if fila else 1
        numero = padre.fila + '.' + str(numero)
        return numero

    fila = FichaCostoFilas.objects.filter(~Q(fila__contains='.'), encabezado=True).aggregate(ultima=Max('fila'))[
        'ultima']
    return str(int(fila) + 1) if fila else '1'


def message_error(request, title, text):
    sweetify.error(
        request=request,
        title=title,
        text=text,
        confirmButtonColor='#3085d6',
        confirmButtonText=_('Accept'),
        backdrop=True,
        showLoaderOnConfirm=True,
        persistent=_("Close"),
    )


def message_success(request, title, text):
    sweetify.success(
        request=request,
        title=title,
        text=text,
        confirmButtonColor='#3085d6',
        confirmButtonText=_('Accept'),
        backdrop=True,
        showLoaderOnConfirm=True,
        persistent=_("Close"),
    )


def message_warning(request, title, text):
    sweetify.warning(
        request=request,
        title=title,
        text=text,
        confirmButtonColor='#3085d6',
        confirmButtonText=_('Accept'),
        backdrop=True,
        showLoaderOnConfirm=True,
        persistent=_("Close"),
    )


def json_response(message=None, success=True, **data):
    """
    Args:
        message:
        success:
        **data:
    """
    if not message:
        json_object = {'success': success}
    else:
        json_object = {'success': success, 'message': message}

    json_object.update(data)
    return json.dumps(json_object)


def genera_numero_doc(departamento, ueb, tipodoc):
    config = settings.NUMERACION_DOCUMENTOS_CONFIG
    consecutivo_conf = config[TipoNumeroDoc.NUMERO_CONSECUTIVO]
    control_conf = config[TipoNumeroDoc.NUMERO_CONTROL]

    numeros_consec_control = [(), ()]

    numeros = NumerosDocumentos.objects.filter(ueb=ueb)

    numeros_consec_control[0] = dame_numero(numeros, consecutivo_conf, departamento, tipodoc,
                                            TipoNumeroDoc.NUMERO_CONSECUTIVO)
    numeros_consec_control[1] = dame_numero(numeros, control_conf, departamento, tipodoc, TipoNumeroDoc.NUMERO_CONTROL)
    return numeros_consec_control


def dame_numero(numeros, conf, departamento, tipodoc, tiponumero):
    if conf['tipo_documento'] and conf['departamento']:
        numero = numeros.filter(tipodocumento=tipodoc, departamento=departamento)
    elif conf['departamento']:
        numero = numeros.filter(departamento=departamento)
    elif conf['tipo_documento']:
        numero = numeros.filter(tipodocumento=tipodoc)
    else:
        numero = numeros

    if numero:
        prefijo = numero[0].tipodocumento.prefijo if conf['prefijo'] else ''
        return (numero[0].consecutivo + 1 if tiponumero == TipoNumeroDoc.NUMERO_CONSECUTIVO else numero[0].control + 1,
                conf['sistema'], '' if not prefijo else prefijo)

    pre = ''
    if conf['prefijo']:
        tipo = TipoDocumento.objects.get(pk=tipodoc)
        pre = tipo.prefijo
    prefijo = '' if not pre else pre
    return (1, conf['sistema'], prefijo)

@transaction.atomic
def get_fechas_procesamiento_inicio(ueb=None):
    fechas = FechaPeriodo.objects.select_for_update().all()
    if ueb:
        fechas = fechas.filter(ueb=ueb)
    fechasinicio = FechaInicio.objects.select_for_update().all()
    list_dicc = [objeto.to_dict() for objeto in fechas]
    fechas_dict = {}
    for item in list_dicc:
        ueb = item.pop('ueb')
        dpto = [x for x in item.keys()][0]
        inicio = fechasinicio.filter(ueb=ueb, departamento=dpto).first()
        if ueb in fechas_dict.keys():
            fechas_dict[ueb][dpto] = item[dpto]
            fechas_dict[ueb][dpto]['fecha_inicio'] = inicio.fecha if inicio else None
        else:
            fechas_dict[ueb] = item
            fechas_dict[ueb][dpto]['fecha_inicio'] = inicio.fecha if inicio else None
    return fechas_dict


def get_configuracion_numeracion():
    numeracion = NumeracionDocumentos.objects.all()
    list_dicc = [objeto.to_dict() for objeto in numeracion]
    return {item["tiponumero"]: item for item in list_dicc}


def get_otras_configuraciones():
    numeracion = ConfiguracionesGen.objects.all()
    list_dicc = [objeto.to_dict() for objeto in numeracion]
    return {item["clave"]: item for item in list_dicc}


def dame_fechas_inicio_procesamiento(ueb, deoartamento):
    fecha_procesamiento = None
    fecha_inicio = None

    if settings.FECHAS_PROCESAMIENTO and ueb in settings.FECHAS_PROCESAMIENTO.keys() and departamento in \
            settings.FECHAS_PROCESAMIENTO[ueb].keys():
        fecha_procesamiento = settings.FECHAS_PROCESAMIENTO[ueb][departamento]['fecha_procesamiento']
        fecha_inicio = settings.FECHAS_PROCESAMIENTO[ueb][departamento]['fecha_inicio']

    return (fecha_procesamiento, fecha_inicio)

# #TODO ver si se va a usar
# def crear_superusuario(credentials):
#
#     user, created = User.objects.get_or_create(
#         username = credentials["username"],
#         email=credentials["email"],
#         defaults={"is_active": True, "is_staff": True, "is_superuser": True},
#     )
#     if created:
#         user.set_password(credentials["password"])
#         user.save()
#         msg = "Superusuario - %(email)s creado satisfactoriamente " % credentials
#     else:
#         msg = "Superusuario - %(email)s ya existe " % credentials
#     return msg
