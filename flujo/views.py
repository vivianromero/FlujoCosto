import calendar
import datetime
from datetime import datetime
from ast import literal_eval
import calendar

import sweetify
from django.http import HttpResponse
from django.db import IntegrityError
from django.db.models import Max
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.utils.translation import gettext_lazy as _
from django_htmx.http import HttpResponseLocation

from app_apiversat.functionapi import getAPI
from app_index.views import CommonCRUDView, BaseModalFormView
from codificadores.models import FechaInicio
from cruds_adminlte3.inline_crud import InlineAjaxCRUD
from cruds_adminlte3.templatetags.crud_tags import crud_inline_url
from flujo.filters import DocumentoFilter
from flujo.tables import DocumentoTable, DocumentosVersatTable, DocumentosVersatDetalleTable
from .forms import *
from .forms import DepartamentoDocumentosForm
from .models import *
from .utils import ids_documentos_versat_procesados


# Create your views here.

# ------ DocumentoDetalle / AjaxCRUD ------
class DocumentoDetalleAjaxCRUD(InlineAjaxCRUD):
    model = DocumentoDetalle
    base_model = Documento
    namespace = 'app_index:flujo'
    inline_field = 'documento'
    add_form = DocumentoDetalleForm
    update_form = DocumentoDetalleForm
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

    title = ""

    def get_create_view(self):
        create_view = super().get_create_view()

        class CreateView(create_view):

            def get_context_data(self, **kwargs):
                context = super().get_context_data(**kwargs)
                return context

            def form_valid(self, form):
                try:
                    doc = self.model_id
                    existencia = None if doc.tipodocumento.operacion == OperacionDocumento.ENTRADA else valida_existencia_producto(doc, form.cleaned_data[
                        'producto'], form.cleaned_data['estado'],
                                                                                                                                   form.cleaned_data[
                                                                                                                                       'cantidad'])
                    if doc.tipodocumento.operacion == OperacionDocumento.SALIDA and not existencia:
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
                return HttpResponse(""" """)

        return CreateView

    def get_update_view(self):
        view = super().get_update_view()

        class OEditView(view):

            def form_valid(self, form):
                try:
                    self.object = form.save(commit=False, doc=self.model_id)
                    setattr(self.object, self.inline_field, self.model_id)
                    self.object.save()
                except IntegrityError as e:
                    # Maneja el error de integridad (duplicación de campos únicos)
                    mess_error = "El producto ya existe para la norma"
                    form.add_error(None, mess_error)
                    return self.form_invalid(form)
                return HttpResponse(""" """)

        return OEditView

    def get_delete_view(self):
        # djDeleteView = super(InlineAjaxCRUD, self).get_delete_view()
        delete_view = super().get_delete_view()

        class DeleteView(delete_view):
            # inline_field = self.inline_field
            # base_model = self.base_model
            # name = self.name
            # views_available = self.views_available[:]

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
                return "/"

            def post(self, request, *args, **kwargs):
                self.model_id = get_object_or_404(
                    self.base_model, pk=kwargs['model_id']
                )
                if self.model_id:
                    url_father = self.base_model.get_absolute_url(self=self.model_id)
                else:
                    url_father = self.get_success_url()
                doc = self.model_id
                producto = self.kwargs['pk']

                response = delete_view.post(self, request, *args, **kwargs)

                return HttpResponse(" ")

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

    inlines = [DocumentoDetalleAjaxCRUD]

    def get_create_view(self):
        view = super().get_create_view()

        class OCreateView(view):

            def get_form_kwargs(self):
                form_kwargs = super().get_form_kwargs()
                departamento = self.request.GET.get('departamento', None)
                if departamento is None and self.request.htmx.current_url_abs_path and 'departamento' in self.request.htmx.current_url_abs_path:
                    deps = [i for i in self.request.htmx.current_url_abs_path.split('?')[1].split('&') if i != '']
                    departamento = next((x for x in deps if 'departamento' in x), [None]).split('=')[1]
                tipo_doc = self.request.GET.get('tipo_doc', None)
                form_kwargs.update(
                    {
                        "user": self.request.user,
                        "departamento": departamento,
                        "tipo_doc": tipo_doc,
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
                    # url = reverse_lazy(crud_url_name(self.model, 'update'), kwargs={"pk": self.object.id})
                    url = self.model.get_absolute_url(self.object)
                    # return HttpResponseLocation(url, target='#dialog',)
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
                    DepartamentoDocumentosForm(initial={'departamento': self.dep}),
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
                # if self.request.htmx and self.request.htmx.current_url_abs_path.split('?').__len__() > 1:
                #     depx = [i for i in self.request.htmx.current_url_abs_path.split('?')[1].split('&') if i != '']
                # else:
                #     depx = []
                if self.dep is not None and self.dep != '':
                    qdict['departamento'] = self.dep
                    # queryset = queryset.filter(departamento=self.dep)
                if self.dep == '' or self.dep is None:
                    # queryset = queryset.none()
                    return self.model.objects.none()
                if rango_fecha is not None and rango_fecha != '':
                    fechas = rango_fecha.strip().split('-')
                    qdict['fecha__gte'] = datetime.strptime(fechas[0].strip(), formating).date()
                    qdict['fecha__lte'] = datetime.strptime(fechas[1].strip(), formating).date()
                    # queryset = queryset.filter(
                    #     fecha__gte=datetime.datetime.strptime(fechas[0].strip(), formating).date(),
                    #     fecha__lte=datetime.datetime.strptime(fechas[1].strip(), formating).date()
                    # )
                # if len(depx) > 0:
                #     depxs = depx[0].split('=')
                #     if self.dep is None:
                #         if depxs[0] == 'departamento':
                #             queryset = queryset.filter(departamento=depxs[1])
                #             self.dep = depxs[1]
                #     elif fecha is None:
                #         if depxs[0] == 'fecha':
                #             fechas = depxs[1].strip().split('-')
                #             fechas[0] = fechas[0].replace('%20', '').replace('%2F', '/')
                #             fechas[1] = fechas[1].replace('%20', '').replace('%2F', '/')
                #             queryset = queryset.filter(
                #                 fecha__gte=datetime.datetime.strptime(fechas[0].strip(), formating).date(),
                #                 fecha__lte=datetime.datetime.strptime(fechas[1].strip(), formating).date()
                #             )
                # else:
                #     queryset = queryset.none()
                # if qdict:
                #     return queryset.filter(**qdict)
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

        return ODeleteView


def confirmar_documento(request, pk):
    # Para confirmar un documento se valida:
    #  - que contenga detalles
    #  - que no existan documentos en edición anteriores a él
    with transaction.atomic():
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
            # list_dicc = [objeto.to_dict() for objeto in exist_dpto]
            # dicc_existencias = dame_diccionario_exist(list_dicc)
            actualizar_existencia = []
            for d in detalles:
                producto = d.producto
                estado = d.estado
                exist = exist_dpto.filter(producto=producto, estado=estado).first()
                inicial_exist = 0 if not exist else exist.cantidad_inicial
                entradas_exist = 0 if not exist else exist.cantidad_entrada
                salidas_exist = 0 if not exist else exist.cantidad_salida
                cantidad_final_exist = 0 if not exist else exist.cantidad_final
                importe_exist = 0 if not exist else exist.importe

                precio = d.precio
                cantidad = d.cantidad
                importe = d.importe

                if operacion == OperacionDocumento.ENTRADA and exist:  # calcular el precio promedio
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
                'confirmed': 'true',
            }
        )


def existen_documentos_sin_confirmar(obj):
    conf = settings.NUMERACION_DOCUMENTOS_CONFIG[TipoNumeroDoc.NUMERO_CONSECUTIVO]
    departamento = obj.departamento
    ueb = obj.ueb
    tipodoc = obj.tipodocumento
    numeroconsecutivo = obj.numeroconsecutivo

    docs = Documento.objects.filter(ueb=ueb, numeroconsecutivo__lt=numeroconsecutivo)

    if conf['tipo_documento'] and conf['departamento']:
        doc = docs.filter(tipodocumento=tipodoc, departamento=departamento)
    elif conf['departamento']:
        doc = docs.filter(departamento=departamento)
    elif conf['tipo_documento']:
        doc = docs.filter(tipodocumento=tipodoc)
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

    # detalles de los doc que están en edición de la ueb y el departamento y contienen el producto
    docs_en_edicion = DocumentoDetalle.objects.select_for_update().filter(**dicc)

    # docum anteriores al actual que tienen el producto
    docs_anteriors = docs_en_edicion.filter(documento__numeroconsecutivo__lt=doc.numeroconsecutivo)

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

    # se actualiza la existencia del producto en el detalle actual
    existencia_product = float(cantidad_existencia) + float(cantidad) * operacion + float(total_anterior)
    return None if existencia_product < 0 else existencia_product


class ObtenerDocumentoVersatModalFormView(BaseModalFormView):
    template_name = 'app_index/modals/modal_form.html'
    form_class = ObtenerDocumentoVersatForm
    viewname = 'app_index:appversat:prod_appversat'
    inline_table = DocumentosVersatDetalleTable([])
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
        ctx = super().get_context_data(**kwargs)
        ctx.update({
            'btn_rechazar': 'Rechazar Documento',
            'btn_aceptar': 'Aceptar Documento',
            'inline_table': self.inline_table,
            'detalle': detalle,
        })
        return ctx

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        iddocumento_numero = self.request.GET.get('iddocumento_numero')
        iddocumento_numctrl = self.request.GET.get('iddocumento_numctrl')
        iddocumento_fecha = self.request.GET.get('iddocumento_fecha')
        iddocumento_concepto = self.request.GET.get('iddocumento_concepto')
        iddocumento_almacen = self.request.GET.get('iddocumento_almacen')
        iddocumento_sumaimporte = self.request.GET.get('iddocumento_sumaimporte')
        kwargs['initial'].update({
            "iddocumento_numero": iddocumento_numero,
            "iddocumento_numctrl": iddocumento_numctrl,
            "iddocumento_fecha": iddocumento_fecha,
            "iddocumento_concepto": iddocumento_concepto,
            "iddocumento_almacen": iddocumento_almacen,
            "iddocumento_sumaimporte": iddocumento_sumaimporte,
        })
        return kwargs
