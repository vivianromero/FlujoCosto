import uuid
import datetime
from datetime import datetime
from ast import literal_eval
import calendar

from django.db import IntegrityError
from django.db.models import Max
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.utils.translation import gettext_lazy as _
from django_htmx.http import HttpResponseLocation
from django.views.generic.edit import FormView

import settings
from app_apiversat.functionapi import getAPI
from app_index.views import CommonCRUDView, BaseModalFormView
from codificadores.models import *
from cruds_adminlte3.inline_crud import InlineAjaxCRUD
from cruds_adminlte3.inline_htmx_crud import InlineHtmxCRUD
from flujo.filters import DocumentoFilter
from flujo.tables import *
from .forms import *
from .models import *
from .utils import ids_documentos_versat_procesados, dame_valor_anterior, actualiza_numeros, actualiza_numero_eliminado, \
    existencia_anterior
from rest_framework.views import APIView
from utiles.utils import message_error


# Create your views here.


# ------ DocumentoDetalle / HtmxCRUD ------
class DocumentoDetalleHtmxCRUD(InlineHtmxCRUD):
    model = DocumentoDetalle
    base_model = Documento
    namespace = 'app_index:flujo'
    inline_field = 'documento'
    add_form = DocumentoDetalleForm
    update_form = DocumentoDetalleForm
    detail_form = DocumentoDetalleDetailForm
    list_fields = [
        'producto',
        'estado',
        'cantidad',
        'precio',
        'importe',
        'existencia',
    ]

    views_available = [
        'list',
        'list_detail',
        'create',
        'update',
        'delete',
        'detail',
    ]

    title = "Detalles de documentos"

    table_class = DocumentoDetalleTable

    def get_create_view(self):
        create_view = super().get_create_view()

        class CreateView(create_view):

            def get_form_kwargs(self):
                form_kwargs = super().get_form_kwargs()
                form_kwargs.update(
                    {
                        "doc": self.model_id,
                    }
                )
                return form_kwargs

            def get_context_data(self, **kwargs):
                context = super().get_context_data(**kwargs)
                title = 'Formulario Htmx Modal'
                context.update({
                    'modal_form_title': title,
                })
                return context

            def form_valid(self, form):
                try:
                    doc = self.model_id
                    existencia = None if doc.tipodocumento.operacion == OperacionDocumento.ENTRADA else valida_existencia_producto(
                        doc, form.cleaned_data[
                            'producto'], form.cleaned_data['estado'],
                        form.cleaned_data[
                            'cantidad'])
                    if doc.tipodocumento.operacion == OperacionDocumento.SALIDA and existencia is None:
                        mess_error = "No se puede dar salida a esa cantidad"
                        form.add_error(None, mess_error)
                        return self.form_invalid(form)

                    self.object = form.save(commit=False, doc=doc, existencia=existencia)
                    setattr(self.object, self.inline_field, self.model_id)
                    self.object.save()
                except IntegrityError as e:
                    # Maneja el error de integridad (duplicación de campos únicos)
                    mess_error = "El producto ya existe para el documento"
                    form.add_error(None, mess_error)
                    return self.form_invalid(form)
                return super().form_valid(form)

        return CreateView

    def get_detail_view(self):
        detail_view = super().get_detail_view()

        class DetailView(detail_view):

            def get_form_kwargs(self):
                form_kwargs = super().get_form_kwargs()
                form_kwargs.update(
                    {
                        "doc": self.model_id,
                    }
                )
                return form_kwargs

            def get_context_data(self, **kwargs):
                return super(DetailView, self).get_context_data()

        return DetailView

    def get_update_view(self):
        view = super().get_update_view()

        class UpdateView(view):

            def get_form_kwargs(self):
                form_kwargs = super().get_form_kwargs()
                form_kwargs.update(
                    {
                        "doc": self.model_id,
                    }
                )
                return form_kwargs

            def get_context_data(self, **kwargs):
                ctx = super().get_context_data(**kwargs)
                title = 'Editar ' + self.name
                ctx.update({
                    'modal_form_title': title,
                })
                return ctx

        return UpdateView

    def get_delete_view(self):
        delete_view = super().get_delete_view()

        class DeleteView(delete_view):

            def get_context_data(self, **kwargs):
                context = super(DeleteView, self).get_context_data(**kwargs)
                context['base_model'] = self.model_id
                context['inline_model'] = self.object
                context['name'] = self.name
                context['views_available'] = self.views_available
                if self.model_id:
                    url_father = self.base_model.get_absolute_url(self=self.model_id)
                else:
                    url_father = self.get_success_url()
                context['url_father'] = url_father
                return context

            # def get(self, request, *args, **kwargs):
            #     return self.post(self, request, *args, **kwargs)

            def post(self, request, *args, **kwargs):
                self.model_id = get_object_or_404(
                    self.base_model, pk=kwargs['model_id']
                )
                doc = self.model_id
                producto = self.kwargs['pk']
                existencia_anterior(doc, producto, True)
                return super().post(request, *args, **kwargs)

        return DeleteView


# ------ Documento / CRUD ------
class DocumentoCRUD(CommonCRUDView):
    model = Documento

    template_name_base = 'app_index/flujo'

    partial_template_name_base = 'app_index/flujo/partials'

    namespace = 'app_index:flujo'

    fields = [
        'fecha',
        'numerocontrol',
        'numeroconsecutivo',
        'suma_importe',
        'observaciones',
        'estado',
        'reproceso',
        'editar_nc',
        'comprob',
        'departamento',
        'tipodocumento',
        'ueb',
    ]

    add_form = DocumentoForm
    update_form = DocumentoForm
    detail_form = DocumentoDetailForm

    list_fields = fields

    filter_fields = fields

    views_available = ['list', 'update', 'create', 'delete', 'detail']
    view_type = ['list', 'update', 'create', 'delete', 'detail']

    filterset_class = DocumentoFilter

    # Table settings
    paginate_by = 25
    table_class = DocumentoTable

    inlines = [DocumentoDetalleHtmxCRUD]

    # htmx
    hx_target = '#table_content_documento_swap'
    hx_swap = 'outerHTML'
    hx_form_target = '#dialog'
    hx_form_swap = 'outerHTML'
    hx_retarget = '#dialog'
    hx_reswap = 'outerHTML'

    def get_create_view(self):
        view = super().get_create_view()

        class OCreateView(view):

            def get_form_kwargs(self):
                form_kwargs = super().get_form_kwargs()
                departamento = self.request.GET.get('departamento', None)

                if departamento is None and self.request.htmx.current_url_abs_path and 'departamento' in self.request.htmx.current_url_abs_path:
                    deps = [i for i in self.request.htmx.current_url_abs_path.split('?')[1].split('&') if i != '']
                    departamento = next((x for x in deps if 'departamento' in x), [None]).split('=')[1]
                dpto = Departamento.objects.get(pk=departamento)
                dpto.fechaperiodo_departamento.all()
                tipo_doc = self.request.GET.get('tipo_doc', None)
                form_kwargs.update(
                    {
                        "user": self.request.user,
                        "departamento": departamento,
                        "tipo_doc": tipo_doc,
                        # "fecha_procesam": ,
                    }
                )
                return form_kwargs

            def get_context_data(self, **kwargs):
                ctx = super().get_context_data(**kwargs)
                dep = self.request.GET.get('departamento', None)
                tipo_doc = self.request.GET.get('tipo_doc', None)
                departamento = Departamento.objects.get(pk=dep) if dep else None
                tipodocumento = TipoDocumento.objects.get(pk=tipo_doc) if tipo_doc else None
                title = 'Departamento: %s | Documento: %s' % (departamento, tipodocumento)
                ctx.update({
                    'modal_form_title': title,
                    "hx_target": '#table_content_documento_swap',
                    'max_width': '1250px',
                })
                return ctx

            def get_success_url(self):
                if "inline" in self.request.POST:
                    url = self.model.get_absolute_url(self.object)
                else:
                    url = super().get_success_url()
                return url

            def form_valid(self, form):
                try:
                    return super().form_valid(form)
                except IntegrityError as e:
                    # Maneja el error de integridad (duplicación de campos únicos)
                    mess_error = settings.NUMERACION_DOCUMENTOS_CONFIG[
                        TipoNumeroDoc.NUMERO_CONSECUTIVO if e.args[0].find(
                            'numeroconsecutivo') > 0 else TipoNumeroDoc.NUMERO_CONTROL]['mensaje_error']
                    form.add_error(None, mess_error)
                    return self.form_invalid(form)
                except Exception as e:
                    form.add_error(None, 'Existe un error al salvar los datos')
                    return self.form_invalid(form)

        return OCreateView

    def get_filter_list_view(self):
        view = super().get_filter_list_view()

        class OFilterListView(view):
            def get_context_data(self, *, object_list=None, **kwargs):
                context = super().get_context_data(**kwargs)
                dep_queryset = context['form'].fields['departamento'].queryset
                ueb = self.request.user.ueb
                dep_queryset = dep_queryset.filter(unidadcontable=ueb)
                context['form'].fields['departamento'].queryset = dep_queryset
                tiposdoc = TipoDocumento.objects.filter(generado=False)
                tipo_doc_entrada = tiposdoc.filter(operacion=OperacionDocumento.ENTRADA)
                tipo_doc_salida = tiposdoc.filter(operacion=OperacionDocumento.SALIDA)
                dpto = dep_queryset.get(pk=self.dep) if self.dep else None
                inicializado = False if not self.dep else dpto.inicializado(ueb)
                if not inicializado:
                    tipo_doc_entrada = tipo_doc_entrada.filter(pk=ChoiceTiposDoc.CARGA_INICIAL)
                else:
                    tipo_doc_entrada = tipo_doc_entrada.exclude(pk=ChoiceTiposDoc.CARGA_INICIAL)

                tableversat = DocumentosVersatTable([])
                url_docversat = None
                if not inicializado and self.dep:
                    tableversat.empty_text = 'El departamento "%s" no se ha inicializado' % dpto

                if not self.dep:
                    tableversat.empty_text = "Seleccione un departamento"

                if self.dep and inicializado:
                    dpto = self.request.GET.get('departamento', None)
                    datostableversat = dame_documentos_versat(self.request, dpto if dpto else self.dep)
                    tableversat = DocumentosVersatTable([]) if datostableversat == None else DocumentosVersatTable(
                        datostableversat)
                    if 'actions' in tableversat.col_vis:
                        tableversat.col_vis.remove('actions')
                    tableversat.empty_text = "Error de concexión con la API Versat para obtener los datos" if datostableversat == None else "No hay datos para mostrar"
                    DepartamentoDocumentosForm(initial={'departamento': self.dep})
                    url_docversat = reverse_lazy(crud_url_name(Documento, 'list', 'app_index:flujo:'))

                context.update({
                    'filter': False,
                    'select_period': True,
                    'period_form': DepartamentoDocumentosForm(initial={'departamento': self.dep}),
                    'tableversat': tableversat if tableversat else None,
                    "hx_get": reverse_lazy(crud_url_name(Documento, 'list', 'app_index:flujo:')),
                    "hx_target": '#table_content_documento_swap',
                    "col_vis_hx_include": "[name='departamento'], [name='rango_fecha']",
                    'create_link_menu': True,
                    'url_docversat': url_docversat,
                    'hay_departamento': not self.dep == None,
                    'tipo_doc_entrada': tipo_doc_entrada,
                    'tipo_doc_salida': tipo_doc_salida,
                    'inicializado': inicializado,
                    'confirm': True,
                    'texto_confirm': "Al confirmar no podrá modificar el documento.¡Esta acción no podrá revertirse!",
                    'texto_inicializar': "Una vez inicializado el departamento, podrá realizar acciones en él.",
                })
                return context

            def get_queryset(self):
                qdict = {}
                queryset = super(OFilterListView, self).get_queryset()
                formating = '%d/%m/%Y'
                self.dep = self.request.GET.get('departamento', None)
                rango_fecha = self.request.GET.get('rango_fecha', None)
                if self.dep is not None and self.dep != '':
                    qdict['departamento'] = self.dep
                if self.dep == '' or self.dep is None:
                    return self.model.objects.none()
                if rango_fecha is not None and rango_fecha != '':
                    fechas = rango_fecha.strip().split('-')
                    qdict['fecha__gte'] = datetime.strptime(fechas[0].strip(), formating).date()
                    qdict['fecha__lte'] = datetime.strptime(fechas[1].strip(), formating).date()
                return queryset

        return OFilterListView

    def get_update_view(self):
        view = super().get_update_view()

        class OEditView(view):

            def get_context_data(self, **kwargs):
                ctx = super(OEditView, self).get_context_data(**kwargs)
                title = 'Departamento: %s | Documento: %s' % (self.object.departamento, self.object.tipodocumento)
                ctx.update({
                    'modal_form_title': title,
                    'max_width': '1250px',
                    'hx_target': '#table_content_documento_swap',
                    'confirm': True,
                    'texto_confirm': "Al confirmar no podrá modificar el documento.¡Esta acción no podrá revertirse!",
                    'object_model': self.model,
                })
                return ctx

            def form_valid(self, form):
                try:
                    return super().form_valid(form)
                except IntegrityError as e:
                    # Maneja el error de integridad (duplicación de campos únicos)
                    mess_error = settings.NUMERACION_DOCUMENTOS_CONFIG[
                        TipoNumeroDoc.NUMERO_CONSECUTIVO if e.args[0].find(
                            'numeroconsecutivo') > 0 else TipoNumeroDoc.NUMERO_CONTROL]['mensaje_error']
                    form.add_error(None, mess_error)
                    return self.form_invalid(form)

        return OEditView

    def get_delete_view(self):
        view = super().get_delete_view()

        class ODeleteView(view):

            def get_context_data(self, **kwargs):
                ctx = super().get_context_data(**kwargs)
                ctx.update({
                    'hx_target': '#table_content_documento_swap',
                    'hx-swap': 'outerHTML',
                })

                return ctx

            @transaction.atomic
            def post(self, request, *args, **kwargs):
                self.object = self.get_object()
                try:
                    detalles = self.object.documentodetalle_documento.all()
                    doc = self.object
                    control = doc.get_numerocontrol()
                    consecutivo = doc.numeroconsecutivo
                    for d in detalles:
                        existencia_anterior(doc, d.pk, True)
                    self.object.delete()
                    actualiza_numero_eliminado(doc.ueb, doc.departamento, control, consecutivo)
                except ProtectedError as e:
                    protected_details = ", ".join([str(obj) for obj in e.protected_objects])
                    title = 'No se puede eliminar '
                    text = 'Este elemento contiene o está relacionaco con: \n'
                    message_error(self.request,
                                  title + self.object.__str__() + '!',
                                  text=text + protected_details)
                    sweetify.error(self.request, title + self.object.__str__() + '!', text=text + protected_details,
                                   persistent=True)
                    return HttpResponseRedirect(self.get_success_url())
                if self.success_message:
                    sweetify.success(self.request, self.success_message)
                return HttpResponseRedirect(self.get_success_url())

        return ODeleteView

    def get_detail_view(self):
        view = super().get_detail_view()

        class ODetailView(view):
            hx_target = self.hx_target
            hx_swap = self.hx_swap
            hx_form_target = self.hx_form_target
            hx_form_swap = self.hx_form_swap

            def get_context_data(self, **kwargs):
                ctx = super().get_context_data()
                return ctx

        return ODetailView


def confirmar_documento(request, pk):
    # Para confirmar un documento se valida:
    #  - que contenga detalles
    #  - que no existan documentos en edición anteriores a él, que el umtimo consecutivo confirmado sea el anterior a su numero
    # Procedimiento
    #  - Despues de validar y todo ok se procede a la confirmación
    #  - Si actualizan las existencias
    #  - Si es un documento de entrada se actualiza el precio
    #  - Si el documento lo requiere se genera el documento en el destino

    obj = Documento.objects.select_for_update().get(pk=pk)
    params = '?' + request.htmx.current_url_abs_path.split('?')[1]
    departamento = obj.departamento
    ueb = obj.ueb
    operacion = obj.tipodocumento.operacion
    max_numero_editado = 0
    detalles = obj.documentodetalle_documento.all()
    detalles_count = detalles.count()
    if detalles_count > 0 and not existen_documentos_sin_confirmar(obj) and not obj.error:
        exist_dpto = ExistenciaDpto.objects.select_for_update().filter(departamento=departamento, ueb=ueb)
        actualizar_existencia = []
        for d in detalles:
            producto = d.producto
            estado = d.estado
            exist = exist_dpto.filter(producto=producto, estado=estado).first()
            inicial_exist = 0 if not exist else exist.cantidad_inicial
            entradas_exist = 0 if not exist else exist.cantidad_entrada
            salidas_exist = 0 if not exist else exist.cantidad_salida
            cantidad_final_exist = 0 if not exist else exist.cantidad_final

            precio = d.precio if not exist else exist.precio
            cantidad = d.cantidad

            if operacion == OperacionDocumento.ENTRADA and exist:  # calcular el precio promedio
                importe = d.cantidad * d.precio
                importe_exist = 0 if not exist else (exist.cantidad_final * exist.precio)
                importe_t = importe + importe_exist
                cantidad_t = cantidad + cantidad_final_exist
                precio = importe_t / cantidad_t

            cantidad_entrada = cantidad + entradas_exist if operacion == OperacionDocumento.ENTRADA else entradas_exist
            cantidad_salida = cantidad + salidas_exist if operacion == OperacionDocumento.SALIDA else salidas_exist
            cantidad_final = inicial_exist + cantidad_entrada - cantidad_salida

            importe = cantidad_final * precio

            actualizar_existencia.append(
                ExistenciaDpto(ueb=ueb, departamento=departamento, producto=producto, estado=estado,
                               cantidad_entrada=cantidad_entrada, cantidad_salida=cantidad_salida,
                               cantidad_final=cantidad_final, importe=importe,
                               precio=precio))
        ExistenciaDpto.objects.bulk_update_or_create(actualizar_existencia,
                                                     ['cantidad_entrada', 'cantidad_salida', 'precio',
                                                      'cantidad_final', 'importe'],
                                                     match_field=['ueb', 'departamento', 'producto', 'estado'])
        obj.estado = EstadosDocumentos.CONFIRMADO  # Confirmado
        obj.save()

        if obj.tipodocumento.pk == ChoiceTiposDoc.TRANSF_HACIA_DPTO:  # crear el documento de entrada en el destino
            new_tipo = ChoiceTiposDoc.TRANSF_DESDE_DPTO
            departamento_destino = obj.documentotransfdepartamento_documento.get().departamento
            new_doc = crea_documento_generado(ueb, departamento_destino, new_tipo, obj)

            departamento_origen = departamento
            DocumentoTransfDepartamentoRecibida.objects.create(documento=new_doc, documentoorigen=obj)

            crea_detalles_generado(new_doc, detalles)

    else:
        title = 'No puede ser confrimado el documento '
        text = 'No tiene detalles asociados' if detalles_count <= 0 else 'Existen documentos anteriores a él sin Confirmar'
        text = 'Este documento contiene errores' if obj.error else text
        sweetify.error(request, title + obj.__str__() + ' (' + str(obj.numeroconsecutivo) + ') ' + '!', text=text,
                       persistent=True)

        return HttpResponseLocation(
            reverse_lazy(crud_url_name(Documento, 'list', 'app_index:flujo:')) + params,
            target='#table_content_documento_swap',
            headers={
                'HX-Trigger': request.htmx.trigger,
                'HX-Trigger-Name': request.htmx.trigger_name,
                'event_action': event_action,
            }
        )


def crea_documento_generado(ueb, departamento, tipodoc, doc_origen):
    numeros = genera_numero_doc(departamento, ueb, tipodoc)
    numerocontrol = str(numeros[1][0]) if not numeros[1][2] else str(numeros[1][0]) + '/' + str(numeros[1][2])
    numeroconsecutivo = numeros[0][0]

    fecha = settings.FECHAS_PROCESAMIENTO[ueb][departamento]['fecha_procesamiento']
    confconsec = ConfigNumero.DEPARTAMENTO if numeros[0][3]['departamento'] == True else ConfigNumero.UNICO
    confcontrol = ConfigNumero.DEPARTAMENTO if numeros[1][3]['departamento'] == True else ConfigNumero.UNICO

    return Documento.objects.create(fecha=fecha, numerocontrol=numerocontrol,
                                    numeroconsecutivo=numeroconsecutivo,
                                    departamento=departamento, tipodocumento=TipoDocumento.objects.get(pk=tipodoc),
                                    confconsec=confconsec,
                                    confcontrol=confcontrol, ueb=ueb)


@transaction.atomic
def crea_detalles_generado(doc, detalles):
    dicc = {'documento__estado': EstadosDocumentos.EDICION,
            'documento__departamento': doc.departamento, 'documento__ueb': doc.ueb}

    docs_en_edicion = DocumentoDetalle.objects.select_for_update().filter(**dicc)
    detalles_new = []
    for d in detalles:
        docs_en_edicion = DocumentoDetalle.objects.select_for_update().filter(**dicc)
        existencia_product = existencia_producto(docs_en_edicion.filter(producto=d.producto, estado=d.estado), doc,
                                                 d.producto, d.estado, d.cantidad)
        d.existencia = existencia_product
        d.id = uuid.uuid4()
        d.documento = doc
        detalles_new.append(d)

    DocumentoDetalle.objects.bulk_create(detalles_new)
    return


def existen_documentos_sin_confirmar(obj):
    conf = settings.NUMERACION_DOCUMENTOS_CONFIG[TipoNumeroDoc.NUMERO_CONSECUTIVO]
    departamento = obj.departamento
    ueb = obj.ueb
    tipodoc = obj.tipodocumento
    numeroconsecutivo = obj.numeroconsecutivo

    docs = Documento.objects.filter(ueb=ueb, numeroconsecutivo__lt=numeroconsecutivo)

    if conf['departamento']:
        doc = docs.filter(departamento=departamento)
    else:
        doc = docs

    numero = doc.aggregate(numconsec=Max('numeroconsecutivo'))['numconsec']
    if numero and docs.filter(numeroconsecutivo=numero).first().estado == EstadosDocumentos.EDICION:
        return True

    numero = numero if numero else 0

    return numeroconsecutivo - numero > 1


@transaction.atomic
def inicializar_departamento(request, pk):
    docs = Documento.objects.filter(departamento=pk, ueb=request.user.ueb).exclude(
        estado__in=[EstadosDocumentos.CONFIRMADO, EstadosDocumentos.CANCELADO])
    departamento = Departamento.objects.get(pk=pk)
    params = '?' + request.htmx.current_url_abs_path.split('?')[1]

    if not docs.exists():
        fecha_inicio, created = FechaInicio.objects.get_or_create(
            fecha=date.today().replace(day=1),
            departamento=departamento,
            ueb=request.user.ueb,
        )
        if created:
            cant_dias = calendar.monthrange(int(date.today().year), int(date.today().month))[1]
            fecha_inicio, created = FechaPeriodo.objects.get_or_create(
                fecha=date.today().replace(day=cant_dias),
                departamento=departamento,
                ueb=request.user.ueb,
            )
            title = 'El departamento %s se inicializó correctamente para %s!' % (departamento, request.user.ueb)
            text = 'Con fecha de inicio: %s' % date.today().replace(day=1)
            sweetify.success(request, title, text=text, persistent=True)
        else:
            title = 'El departamento %s para %s ya ha sido inicializado anteriormente' % (
                departamento, request.user.ueb)
            text = ''
            sweetify.info(request, title, text=text, persistent=True)
    else:
        title = 'No se completó la incialización'
        text = 'Existen documentos sin Confirmar, el departamento %s para %s no se puede inicializar' % (
            departamento, request.user.ueb)
        sweetify.warning(request, title, text=text, persistent=True)

    return HttpResponseLocation(
        reverse_lazy(crud_url_name(Documento, 'list', 'app_index:flujo:')) + params,
        target='#table_content_documento_swap',
        headers={
            'HX-Trigger': request.htmx.trigger,
            'HX-Trigger-Name': request.htmx.trigger_name,
            'initialized': 'true',
        }
    )


def dame_documentos_versat(request, dpto):
    unidadcontable = request.user.ueb

    title_error = _("Couldn't connect")
    text_error = _('Connection error to Versat API')

    try:
        dpto = Departamento.objects.get(pk=dpto)
        if not dpto.inicializado(unidadcontable):
            return redirect(crud_url_name(Documento, 'list', 'app_index:flujo:'))

        fecha_periodo = dpto.fechaperiodo_departamento.all()[0].fecha
        fecha_mes_procesamiento = str(fecha_periodo.year) + '-' + str(fecha_periodo.month) + '-01'

        param = {'fecha_desde': fecha_mes_procesamiento,
                 'fecha_hasta': fecha_periodo.strftime('%Y-%m-%d'),
                 'unidad': unidadcontable.codigo,
                 'centro_costo': dpto.centrocosto.clave
                 }
        response = getAPI('documentogasto', param)

        if response and response.status_code == 200:
            datos = response.json()['results']
            ids = ids_documentos_versat_procesados(fecha_mes_procesamiento, fecha_periodo, dpto, unidadcontable)
            datos = list(filter(lambda x: x['iddocumento'] not in ids, datos))
            return datos
    except Exception as e:
        return None


@transaction.atomic
def valida_existencia_producto(doc, producto, estado, cantidad):
    departamento = doc.departamento
    ueb = doc.ueb

    operacion = doc.operacion

    # tomo la existencia del producto
    existencia = ExistenciaDpto.objects.select_for_update().filter(departamento=departamento, estado=estado,
                                                                   producto=producto, ueb=ueb)
    importe_exist = 0.00
    cantidad_existencia = 0.00

    if existencia:
        exist = existencia.first()
        importe_exist = exist.importe
        cantidad_existencia = exist.cantidad_final

    dicc = {'documento__estado': EstadosDocumentos.EDICION,
            'documento__departamento': departamento, 'producto': producto, 'estado': estado, 'documento__ueb': ueb}

    docs_en_edicion = DocumentoDetalle.objects.select_for_update().filter(**dicc)
    total_anterior = dame_valor_anterior(doc, docs_en_edicion)

    # se actualiza la existencia del producto en el detalle actual
    existencia_product = float(cantidad_existencia) + float(cantidad) * operacion + float(total_anterior)
    return None if existencia_product < 0 else existencia_product


def precioproducto(request):
    tipoproducto = request.GET.get('tipoproducto')
    clasemp = request.GET.get('clase')
    clases_mp = ClaseMateriaPrima.objects.all().exclude(pk=ChoiceClasesMatPrima.CAPACLASIFICADA)
    tipoprod = TipoProducto.objects.all()
    context = {
        'esmatprim': None if tipoproducto != str(ChoiceTiposProd.MATERIAPRIMA) else 1,
        'clases_mp': clases_mp,
        'clase_seleccionada': None if not clasemp else clases_mp.get(pk=clasemp),
        'tipoprod': tipoprod,
        'tipo_selecc': None if not tipoproducto else tipoprod.get(pk=tipoproducto),
    }
    return render(request, 'app_index/partials/productclases.html', context)


def aceptar_documento_versat(kwargs):
    """
    Aceptar un documento
    """
    func_ret = {
        'success': True,
        'errors': {},
        'success_title': 'El documento fue aceptado',
        'error_title': 'El documento no fue aceptado',
    }

    # Aquí va la lógica de la vista/función
    # Simulamos que no hubo errores, simplemente devolvemos func_ret que tiene 'success': True por defecto

    # Simulamos que hubo errores, simplemente cambiamos el valor de 'success': False y si queremos devolver
    # detalles del error lo agregamos al diccionario 'errors' que va dentro de func_ret
    func_ret.update({
        'success': False
    })

    return func_ret


def rechazar_documento_versat(kwargs):
    """
    Rechazar un documento
    """

    func_ret = {
        'success': True,
        'errors': {},
        'success_title': 'El documento fue rechazado',
        'error_title': 'El documento no pudo ser rechazado. Por favor, revise',
    }

    # Aquí va la lógica de la vista/función
    # Simulamos que no hubo errores, simplemente devolvemos func_ret que tiene 'success': True por defecto

    # Simulamos que hubo errores, simplemente cambiamos el valor de 'success': False y si queremos devolver
    # detalles del error lo agregamos al diccionario 'errors' que va dentro de func_ret
    func_ret.update({
        'success': False
    })

    return func_ret


class ObtenerDocumentoVersatModalFormView(BaseModalFormView):
    template_name = 'app_index/modals/modal_form.html'
    form_class = ObtenerDocumentoVersatForm
    father_view = 'app_index:flujo:flujo_documento_list'
    # viewname = {
    #     'submitted': 'app_index:flujo:flujo_documento_versat_aceptar',
    #     'refused': 'app_index:flujo:flujo_documento_versat_rechazar',
    # }
    funcname = {
        'submitted': aceptar_documento_versat,
        'refused': rechazar_documento_versat,
    }
    inline_tables = [{
        "table": DocumentosVersatDetalleTable([]),
        "name": "documentosversatdetalletable",
        "visible": True,
        # "title": "Detalles del Documento"
    }]
    hx_target = '#table_content_documento_swap'
    hx_swap = 'outerHTML'
    hx_form_target = '#dialog'
    hx_form_swap = 'outerHTML'
    hx_retarget = '#dialog'
    hx_reswap = 'outerHTML'
    modal_form_title = 'Obtener Documento del Versat'
    max_width = '1150px'

    def get_context_data(self, **kwargs):
        detalle = self.request.GET.get('detalle', None)
        if detalle:
            detalle = literal_eval(detalle)
        self.inline_tables[0].update({
            "table": DocumentosVersatDetalleTable(detalle),
        })
        ctx = super().get_context_data(**kwargs)
        ctx.update({
            'btn_rechazar': 'Rechazar Documento',
            'btn_aceptar': 'Aceptar Documento',
            'inline_tables': self.inline_tables,
        })
        return ctx

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        iddocumento = self.request.GET.get('iddocumento')
        iddocumento_numero = self.request.GET.get('iddocumento_numero')
        iddocumento_numctrl = self.request.GET.get('iddocumento_numctrl')
        iddocumento_fecha = self.request.GET.get('iddocumento_fecha')
        iddocumento_concepto = self.request.GET.get('iddocumento_concepto')
        iddocumento_almacen = self.request.GET.get('iddocumento_almacen')
        iddocumento_sumaimporte = self.request.GET.get('iddocumento_sumaimporte')
        kwargs['initial'].update({
            "iddocumento": iddocumento,
            "iddocumento_numero": iddocumento_numero,
            "iddocumento_numctrl": iddocumento_numctrl,
            "iddocumento_fecha": iddocumento_fecha,
            "iddocumento_concepto": iddocumento_concepto,
            "iddocumento_almacen": iddocumento_almacen,
            "iddocumento_sumaimporte": iddocumento_sumaimporte,
        })
        return kwargs

    def get_fields_kwargs(self, form):
        kw = {}
        kw.update({
            'request': self.request,
        })
        for field in form.fields:
            if field == 'iddocumento':
                kw.update({field: form.cleaned_data[field]})
        return kw
