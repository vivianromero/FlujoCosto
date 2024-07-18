import calendar
import datetime
import json
from ast import literal_eval
from datetime import datetime

import sweetify
from crispy_forms.templatetags.crispy_forms_filters import as_crispy_field
from django.db import IntegrityError
from django.db.models import F, Value, DecimalField, Sum, Max
from django.db.models import ProtectedError
from django.db.models.functions import Coalesce
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django_htmx.http import HttpResponseLocation

import settings
from app_apiversat.functionapi import getAPI
from app_index.views import CommonCRUDView, BaseModalFormView
from codificadores.models import *
from cruds_adminlte3.inline_htmx_crud import InlineHtmxCRUD
from flujo.filters import DocumentoFilter
from flujo.tables import DocumentoTable, DocumentosVersatTable, DocumentosVersatDetalleTable, DocumentoDetalleTable
from utiles.decorators import *
from utiles.utils import message_error
from .forms import *
from .models import *
from .utils import ids_documentos_versat_procesados, dame_valor_anterior, actualiza_numeros, \
    existencia_anterior


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
    table_class = DocumentoDetalleTable
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

    hx_retarget = '#edit_modal_inner'
    hx_reswap = 'innerHTML'
    hx_swap = 'innerHTML'
    hx_form_target = '#edit_modal_inner'
    hx_form_swap = 'innerHTML'

    def get_create_view(self):
        create_view = super().get_create_view()

        class CreateView(create_view):
            integrity_error = "El producto ya existe para el documento!"

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
                    return super().form_valid(form)
                return super().form_valid(form)

        return CreateView

    def get_update_view(self):
        view = super().get_update_view()

        class OEditView(view):
            integrity_error = "El producto ya existe para el documento!"

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
                return context

            def form_valid(self, form):
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
                return super().form_valid(form)

        return OEditView

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

            def get(self, request, *args, **kwargs):
                self.model_id = get_object_or_404(
                    self.base_model, pk=kwargs['model_id'])
                return super().get(self, request, *args, **kwargs)

            def get_success_url(self):
                return super().get_success_url()

            def post(self, request, *args, **kwargs):
                self.model_id = get_object_or_404(
                    self.base_model, pk=kwargs['model_id']
                )
                doc = self.model_id
                detalle = DocumentoDetalle.objects.get(pk=self.kwargs['pk'])
                producto = detalle.producto
                existencia_anterior(doc, detalle, True)
                doc_error = False
                if doc.documentodetalle_documento.filter(error=True).exclude(producto=producto).exists():
                    doc_error = True

                estado = EstadosDocumentos.EDICION if not doc_error else EstadosDocumentos.ERRORES
                Documento.objects.filter(pk=doc.pk).update(error=doc_error, estado=estado)
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
                fecha_procesamiento = date.today().replace(day=1)
                fecha_periodo = dpto.fechaperiodo_departamento.all()
                if fecha_periodo.exists():
                    fecha_procesamiento = fecha_periodo[0].fecha
                tipo_doc = self.request.GET.get('tipo_doc', None)
                form_kwargs.update(
                    {
                        "user": self.request.user,
                        "departamento": departamento,
                        "tipo_doc": tipo_doc,
                        "fecha_procesamiento": fecha_procesamiento,
                    }
                )
                return form_kwargs

            def get_context_data(self, **kwargs):
                ctx = super().get_context_data(**kwargs)
                params_hx = ''
                dep = self.request.GET.get('departamento', None)
                tipo_doc = self.request.GET.get('tipo_doc', None)
                departamento = Departamento.objects.get(pk=dep) if dep else None
                tipodocumento = TipoDocumento.objects.get(pk=tipo_doc) if tipo_doc else None
                title = 'Departamento: %s | Documento: %s' % (departamento, tipodocumento)
                if self.request.htmx.current_url_abs_path.split('?').__len__() > 1:
                    params_hx = '?' + self.request.htmx.current_url_abs_path.split('?')[1]
                ctx.update({
                    'modal_form_title': title,
                    "hx_target": '#table_content_documento_swap',
                    'max_width': '1250px',
                    'getparams_hx': params_hx,
                })
                return ctx

            def get_success_url(self):
                return super().get_success_url()

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
                if self.inlines:
                    for inline in self.inlines:
                        if 'actions' in inline.table_class.col_vis:
                            inline.table_class.col_vis.remove('actions')
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
                        existencia_anterior(doc, d, True)
                    self.object.delete()
                    actualiza_numeros(doc.ueb, doc.departamento, None, control, None)
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
            modal = self.modal

            def get_context_data(self, **kwargs):
                ctx = super().get_context_data()
                return ctx

        return ODetailView


@transaction.atomic
def confirmar_documento(request, pk):
    # Para confirmar un documento se valida:
    #  - que contenga detalles
    #  - que no existan documentos en edición anteriores a él, que el umtimo consecutivo confirmado sea el anterior a su numero
    # Procedimiento
    #  - Despues de validar y todo ok se procede a la confirmación
    #  - Si actualizan las existencias
    #  - Si es un documento de entrada se actualiza el precio
    #  - Si el documento lo requiere se genera el documento en el destino
    there_is_htmx_params = request.htmx.current_url_abs_path.split('?').__len__() > 1
    getparams_hx = '?' + request.htmx.current_url_abs_path.split('?')[1] if there_is_htmx_params else ''
    obj = Documento.objects.select_for_update().get(pk=pk)
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

        # crear el documento de entrada en el destino
        if obj.tipodocumento.pk == ChoiceTiposDoc.TRANSF_HACIA_DPTO:
            new_tipo = ChoiceTiposDoc.TRANSF_DESDE_DPTO
            departamento_destino = obj.documentotransfdepartamento_documento.get().departamento
            new_doc = crea_documento_generado(ueb, departamento_destino, new_tipo, obj)

            departamento_origen = departamento
            DocumentoTransfDepartamentoRecibida.objects.create(documento=new_doc, documentoorigen=obj)

            crea_detalles_generado(new_doc, detalles)
        title = 'Confirmación terminada'
        text = 'El Documento %s - %s se confirmó satisfactoriamente !' % (obj.numeroconsecutivo, obj.tipodocumento)
        sweetify.success(request, title, text=text, persistent=True)
    else:
        title = 'No puede ser confrimado el documento '
        text = 'No tiene productos asociados' if detalles_count <= 0 else 'Existen documentos anteriores a él sin Confirmar'
        text = 'Este documento contiene errores' if obj.error else text
        sweetify.error(request, title + obj.__str__() + ' (' + str(obj.numeroconsecutivo) + ') ' + '!', text=text,
                       persistent=True)

    return HttpResponseLocation(
        reverse_lazy(crud_url_name(Documento, 'list', 'app_index:flujo:')) + getparams_hx,
        target='#table_content_documento_swap',
        headers={
            'HX-Trigger': request.htmx.trigger,
            'HX-Trigger-Name': request.htmx.trigger_name,
            'event_action': 'confirmed',
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
        existencia_product, hay_error = existencia_producto(
            docs_en_edicion.filter(producto=d.producto, estado=d.estado), doc,
            d.producto, d.estado, d.cantidad)
        d.existencia = existencia_product
        d.error = hay_error
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
                fecha=date.today().replace(day=1),
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
            ids = ids_documentos_versat_procesados(fecha_mes_procesamiento, fecha_periodo, dpto,
                                                   unidadcontable) if datos else []
            datos = list(filter(lambda x: x['iddocumento'] not in ids, datos))
            [datos[x].update({'json_data': literal_eval(json.dumps(datos[x]))}) for x in range(len(datos))]
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
    total_anterior, hay_error = dame_valor_anterior(doc.numeroconsecutivo, docs_en_edicion)

    # se actualiza la existencia del producto en el detalle actual
    existencia_product = float(cantidad_existencia) + float(cantidad) * operacion + float(total_anterior)
    return None if existencia_product < 0 else existencia_product


def precioproducto(request):
    producto = request.GET.get('producto')
    pk_doc = request.GET.get('documento_hidden')
    documento = Documento.objects.get(pk=pk_doc)
    estado = request.GET.get('estado')

    if not producto or not estado or documento.tipodocumento.operacion == OperacionDocumento.ENTRADA:
        return

    precio = dame_precio_salida(producto, estado, documento)
    data = {
        'producto': producto,
        'precio': precio,
        'doc': documento
    }
    form = DocumentoDetalleForm(data)

    response = HttpResponse(
        as_crispy_field(form['precio']).replace('is-invalid', ''),
        content_type='text/html'
    )
    return response


@transaction.atomic
def aceptar_documento_versat(kwargs):
    """
    Aceptar un documento
    """
    func_ret = {
        'success': True,
        'errors': {},
        'success_title': 'El documento fue aceptado',
        'error_title': 'El documento no fue aceptado. Existen productos que no están en el sistema, o no coinciden las unidades de medida',
    }
    detalles = kwargs['detalles']

    no_existen = [d for d in detalles if not d['existe_sistema']]
    if len(no_existen) > 0:
        func_ret.update({
            'success': False
        })
    else:
        iddocumento = kwargs['iddocumento']
        request = kwargs['request']
        json_data = literal_eval(kwargs['json_data'])
        departamento = ''
        if request.htmx.current_url_abs_path and 'departamento' in request.htmx.current_url_abs_path:
            departamento = request.htmx.current_url_abs_path.split('&')[0].split('=')[1]
        dicc_detalle = {}
        detalles_generados = []
        for p in detalles:
            dicc_detalle[p['producto_codigo']] = {'cantidad': float(p['cantidad']), 'um': p['medida_clave'].strip(),
                                                  'precio': float(p['precio'])}

        prods = ProductoFlujo.objects.filter(codigo__in=list(dicc_detalle.keys()))

        new_tipo = ChoiceTiposDoc.ENTRADA_DESDE_VERSAT
        departamento = Departamento.objects.get(pk=departamento)
        new_doc = crea_documento_generado(request.user.ueb, departamento, new_tipo, None)

        for p in prods:
            detalles_generados.append(DocumentoDetalle(cantidad=dicc_detalle[p.codigo]['cantidad'],
                                                       precio=dicc_detalle[p.codigo]['precio'],
                                                       importe=round(float(dicc_detalle[p.codigo]['cantidad']) * float(
                                                           dicc_detalle[p.codigo]['precio']), 2),
                                                       documento=new_doc,
                                                       estado=EstadoProducto.BUENO,
                                                       producto=p
                                                       ))
        crea_detalles_generado(new_doc, detalles_generados)
        fecha = kwargs['iddocumento_fecha']
        partes = fecha.split('/')
        partes.reverse()
        fecha_doc = '-'.join(partes)
        DocumentoOrigenVersat.objects.create(documentoversat=iddocumento, documento=new_doc,
                                             fecha_documentoversat=fecha_doc, documento_origen=json_data)

    return func_ret


@transaction.atomic
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

    iddocumento = kwargs['iddocumento']
    request = kwargs['request']
    fecha = kwargs['iddocumento_fecha']
    partes = fecha.split('/')
    partes.reverse()
    fecha_doc = '-'.join(partes)
    json_data = literal_eval(kwargs['json_data'])
    DocumentoVersatRechazado.objects.create(documentoversat=iddocumento, fecha_documentoversat=fecha_doc,
                                            documento_origen=json_data, ueb=request.user.ueb)

    return func_ret


@transaction.atomic
def rechazar_documento(request, pk):
    """
    Rechazar un documento
    """

    there_is_htmx_params = request.htmx.current_url_abs_path.split('?').__len__() > 1
    getparams_hx = '?' + request.htmx.current_url_abs_path.split('?')[1] if there_is_htmx_params else ''

    doc = Documento.objects.select_for_update().get(pk=pk)
    doc.estado = EstadosDocumentos.RECHAZADO
    doc.save()

    detalles = doc.documentodetalle_documento.all()

    for d in detalles:
        existencia_anterior(doc, d, True)

    # Si al rechazar un documento este genera otro documento
    # Para los tipos de documentos
    # -Transferencia desde departamento, Devolución Recibida (si se rechaza genera Devolución Recibida en el dpto que realizó la transf o dev)
    match doc.tipodocumento.pk:
        case ChoiceTiposDoc.TRANSF_DESDE_DPTO:
            departamento_destino = doc.documentotransfdepartamentorecibida_documento.get().documentoorigen.departamento
        case ChoiceTiposDoc.DEVOLUCION_RECIBIDA:
            departamento_destino = doc.documentodevolucionrecibida_documento.get().documentoorigen.departamento

    new_tipo = ChoiceTiposDoc.DEVOLUCION_RECIBIDA
    new_doc = crea_documento_generado(doc.ueb, departamento_destino, new_tipo, doc)
    crea_detalles_generado(new_doc, detalles)
    DocumentoDevolucionRecibida.objects.create(documento=new_doc, documentoorigen=doc)

    title = 'Documento rechazado'
    text = 'El Documento %s - %s se rechazó satisfactoriamente !' % (doc.numeroconsecutivo, doc.tipodocumento)
    sweetify.success(request, title, text=text, persistent=True)

    return HttpResponseLocation(
        reverse_lazy(crud_url_name(Documento, 'list', 'app_index:flujo:')) + getparams_hx,
        target='#table_content_documento_swap',
        headers={
            'HX-Trigger': request.htmx.trigger,
            'HX-Trigger-Name': request.htmx.trigger_name,
            'event_action': 'refused',
        }
    )


class ObtenerDocumentoVersatModalFormView(BaseModalFormView):
    template_name = 'app_index/modals/modal_form.html'
    form_class = ObtenerDocumentoVersatForm
    father_view = 'app_index:flujo:flujo_documento_list'

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
        json_data = self.request.GET.get('json_data', None)
        if detalle:
            detalle = literal_eval(detalle)
            json_data = literal_eval(json_data)
            codigos_versat = [p['producto_codigo'] for p in detalle]
            productos = ProductoFlujo.objects.values('codigo', 'medida__clave').filter(codigo__in=codigos_versat).all()
            codigos_sistema = [(p['codigo'], p['medida__clave'].strip()) for p in productos]
            for d in detalle:
                d['existe_sistema'] = (d['producto_codigo'], d['medida_clave'].strip()) in codigos_sistema

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
        iddocumento_fecha_hidden = self.request.GET.get('iddocumento_fecha')
        iddocumento_concepto = self.request.GET.get('iddocumento_concepto')
        iddocumento_almacen = self.request.GET.get('iddocumento_almacen')
        iddocumento_sumaimporte = self.request.GET.get('iddocumento_sumaimporte')
        json_data = self.request.GET.get('json_data')
        kwargs['initial'].update({
            "iddocumento": iddocumento,
            "iddocumento_numero": iddocumento_numero,
            "iddocumento_numctrl": iddocumento_numctrl,
            "iddocumento_fecha": iddocumento_fecha,
            "iddocumento_fecha_hidden": iddocumento_fecha_hidden,
            "iddocumento_concepto": iddocumento_concepto,
            "iddocumento_almacen": iddocumento_almacen,
            "iddocumento_sumaimporte": iddocumento_sumaimporte,
            "json_data": json_data,
        })
        return kwargs

    def get_fields_kwargs(self, form):
        kw = {}
        kw.update({
            'request': self.request,
            'iddocumento': form.cleaned_data['iddocumento'],
            'iddocumento_fecha': form.cleaned_data['iddocumento_fecha_hidden'],
        })
        if self.request.POST['event_action'] in ['submitted', 'refused']:
            kw.update(
                {'detalles': self.inline_tables[0]['table'].data.data, 'json_data': form.cleaned_data['json_data']})
        return kw


@transaction.atomic
def dame_precio_salida(producto, estado, doc):
    # documentos anteriores que son entradas y no están confirmados
    dicc = {'documento__estado': EstadosDocumentos.EDICION,
            'documento__departamento': doc.departamento, 'documento__ueb': doc.ueb,
            'documento__tipodocumento__operacion': OperacionDocumento.ENTRADA,
            'documento__numeroconsecutivo__lt': doc.numeroconsecutivo,
            'producto': producto,
            'estado': estado}

    anteriores = DocumentoDetalle.objects.select_for_update().filter(**dicc). \
        aggregate(cantidad_ant=Coalesce(Sum('cantidad'), Value(0.0), output_field=DecimalField()),
                  importe_ant=Coalesce(Sum(F('precio') * F('cantidad')), Value(0.0), output_field=DecimalField())
                  )
    cantidad_anterior = float(anteriores['cantidad_ant'])
    importe_anterior = float(anteriores['importe_ant'])

    dicc = {'departamento': doc.departamento, 'ueb': doc.ueb,
            'producto': producto,
            'estado': estado}

    existencias = ExistenciaDpto.objects.select_for_update().filter(**dicc)
    cantidad_existencia = 0.00
    importe_existencia = 0.00

    if existencias.exists():
        existe = existencias.first()
        cantidad_existencia = float(existe.cantidad_final)
        importe_existencia = float(existe.cantidad_final) * float(existe.precio)

    cantidad_total = cantidad_existencia + cantidad_anterior
    importe_total = importe_existencia + importe_anterior

    precio = importe_total / cantidad_total if cantidad_total > 0 else 0.00
    return round(precio, 7)
