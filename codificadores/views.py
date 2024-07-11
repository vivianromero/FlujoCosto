import sweetify
from crispy_forms.templatetags.crispy_forms_filters import as_crispy_field
from django.contrib import messages
from django.db.models import ProtectedError
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import FormView
from django_ajax.response import JSONResponse
from django_htmx.http import HttpResponseLocation, HttpResponseClientRedirect
from django_tables2 import SingleTableMixin
from django_tables2.export import ExportMixin

from app_index.views import CommonCRUDView, BaseModalFormView, get_current_url_abs_path
from codificadores.filters import *
from codificadores.forms import *
from codificadores.models import VinculoCargoProduccion
from codificadores.tables import *
from cruds_adminlte3.inline_crud import InlineAjaxCRUD
from cruds_adminlte3.inline_htmx_crud import InlineHtmxCRUD
from cruds_adminlte3.templatetags.crud_tags import crud_inline_url
from exportar.views import crear_export_datos_table
from flujo.models import Documento
from utiles.utils import message_error
from . import ChoiceTiposProd
from django.db import IntegrityError


# ------ Departamento / CRUD ------
class DepartamentoCRUD(CommonCRUDView):
    model = Departamento

    namespace = 'app_index:codificadores'

    fields = [
        'codigo',
        'descripcion',
        'centrocosto',
        'unidadcontable',
        'relaciondepartamento',
        'departamentoproductoentrada',
        'departamentoproductosalida',
    ]

    # Hay que agregar __icontains luego del nombre del campo para que busque el contenido
    # y no distinga entre mayúsculas y minúsculas.
    # En el caso de campos relacionados hay que agregar __<nombre_campo_que_se_muestra>__icontains
    search_fields = [
        'codigo__contains',
        'descripcion__icontains',
        'centrocosto__descripcion__icontains',
        'unidadcontable__nombre__icontains',
    ]

    add_form = DepartamentoForm
    update_form = DepartamentoForm

    list_fields = fields

    filter_fields = fields

    filterset_class = DepartamentoFilter

    # Table settings
    table_class = DepartamentoTable

    def get_filter_list_view(self):
        view = super().get_filter_list_view()

        class OFilterListView(view):
            def get_context_data(self, *, object_list=None, **kwargs):
                context = super().get_context_data(**kwargs)
                context.update({
                    'url_importar': 'app_index:importar:dpto_importar',
                    'url_exportar': 'app_index:exportar:dpto_exportar',
                })
                return context

        return OFilterListView


# ------ NormaConsumoDetalle / AjaxCRUD ------
class NormaConsumoDetalleAjaxCRUD(InlineAjaxCRUD):
    model = NormaconsumoDetalle
    base_model = NormaConsumo
    namespace = 'app_index:codificadores'
    inline_field = 'normaconsumo'
    add_form = NormaConsumoDetalleForm
    update_form = NormaConsumoDetalleForm
    list_fields = [
        'norma_ramal',
        'norma_empresarial',
        'operativo',
        'producto',
        'medida',
    ]

    views_available = [
        'list',
        'list_detail',
        'create',
        'update',
        'delete',
        'detail',
    ]

    title = "Detalles de normas de consumo"
    table_class = NormaConsumoDetalleTable
    url_father = None

    def get_create_view(self):
        create_view = super().get_create_view()

        class CreateView(create_view):

            def get_context_data(self, **kwargs):
                context = super().get_context_data(**kwargs)
                return context

            def form_valid(self, form):
                try:
                    self.object = form.save(commit=False)
                    setattr(self.object, self.inline_field, self.model_id)
                    self.object.save()
                except IntegrityError as e:
                    # Maneja el error de integridad (duplicación de campos únicos)
                    mess_error = "El producto ya existe para la norma"
                    form.add_error(None, mess_error)
                    return self.form_invalid(form)
                return HttpResponse(""" """)

            def form_invalid(self, form, **kwargs):
                """If the form is invalid, render the invalid form."""
                ctx = self.get_context_data(**kwargs)
                ctx['form'] = form
                tpl = self.get_template_names()
                crud_inline_url(self.model_id, form.instance, 'create', self.namespace)
                response = render(self.request, tpl, ctx)
                response['HX-Retarget'] = '#edit_modal_inner'
                response['HX-Reswap'] = 'innerHTML'
                return response

        return CreateView

    def get_update_view(self):
        view = super().get_update_view()

        class UpdateView(view):

            def get_context_data(self, **kwargs):
                ctx = super(UpdateView, self).get_context_data(**kwargs)
                title = 'Formulario Ajax Modal'  # 'Departamento: %s | Documento: %s' % (self.object.departamento, self.object.tipodocumento)
                ctx.update({
                    'modal_form_title': title,
                    'max_width': '950px',
                    'hx_target': '#id_' + self.name + '_myList',
                    'confirm': True,
                    'texto_confirm': "Al confirmar no podrá modificar el documento.¡Esta acción no podrá revertirse!",
                    'object_model': self.model,
                })
                return ctx

            def form_valid(self, form):
                try:
                    self.object = form.save(commit=False)
                    setattr(self.object, self.inline_field, self.model_id)
                    self.object.save()
                    event_action = None
                    if self.request.method == 'POST':
                        event_action = self.request.POST.get('event_action', None)
                    elif self.request.method == 'GET':
                        event_action = self.request.GET.get('event_action', None)
                    kwargs = {'pk': self.model_id.id}
                    success_url = crud_url(
                        self.model_id,
                        'update',
                        namespace='app_index:codificadores',
                    )
                    success_url2 = crud_inline_url(self.model_id, self.object, 'list', 'app_index:codificadores')
                except IntegrityError as e:
                    # Maneja el error de integridad (duplicación de campos únicos)
                    mess_error = "El producto ya existe para la norma"
                    form.add_error(None, mess_error)
                    return self.form_invalid(form)
                return HttpResponseLocation(
                    success_url2,
                    target='#id_' + self.name + '_myList',
                    headers={
                        'HX-Trigger': self.request.htmx.trigger,
                        'HX-Trigger-Name': self.request.htmx.trigger_name,
                        'event_action': event_action,
                    },
                    values={
                        'event_action': event_action,
                    }
                )

        return UpdateView

    def get_delete_view(self):
        delete_view = super().get_delete_view()

        class DeleteView(delete_view):

            def get_context_data(self, **kwargs):
                context = super().get_context_data(**kwargs)
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
                    url_father = reverse_lazy(
                        crud_url_name(NormaConsumo, 'update', 'app_index:codificadores:'),
                        args=[self.model.normaconsumo_id]
                    )
                else:
                    url_father = self.get_success_url()
                response = delete_view.post(self, request, *args, **kwargs)
                return HttpResponse(" ")

        return DeleteView

    def get_filter_list_view(self):
        filter_list_view = super(InlineAjaxCRUD, self).get_filter_list_view()

        class FilterListView(filter_list_view):
            inline_field = self.inline_field
            base_model = self.base_model
            name = self.name
            views_available = self.views_available[:]

            def get_context_data(self, **kwargs):
                context = super(FilterListView, self).get_context_data(**kwargs)
                table = self.get_table(**self.get_table_kwargs())
                table.empty_text = 'No existen productos aún'
                context[self.get_context_table_name(table)] = table
                context['base_model'] = self.model_id
                context['name'] = self.name
                context['views_available'] = self.views_available
                return context

            def get_queryset(self):
                queryset = super(FilterListView, self).get_queryset()
                params = {
                    self.inline_field: self.model_id
                }
                queryset = queryset.filter(**params)
                return queryset

            def get(self, request, *args, **kwargs):
                self.model_id = get_object_or_404(
                    self.base_model, pk=kwargs['model_id'])
                return filter_list_view.get(self, request, *args, **kwargs)

        return FilterListView


# ------ NormaConsumoDetalle / HtmxCRUD ------
class NormaConsumoDetalleHtmxCRUD(InlineHtmxCRUD):
    model = NormaconsumoDetalle
    base_model = NormaConsumo
    namespace = 'app_index:codificadores'
    inline_field = 'normaconsumo'
    add_form = NormaConsumoDetalleForm
    update_form = NormaConsumoDetalleForm
    detail_form = NormaConsumoDetalleDetailForm
    list_fields = [
        'norma_ramal',
        'norma_empresarial',
        'operativo',
        'producto',
        'medida',
    ]

    views_available = [
        'list',
        'list_detail',
        'create',
        'update',
        'delete',
        'detail',
    ]

    title = "Detalles de normas de consumo"
    table_class = NormaConsumoDetalleTable
    url_father = None

    def get_create_view(self):
        create_view = super().get_create_view()

        class CreateView(create_view):

            def get_context_data(self, **kwargs):
                context = super().get_context_data(**kwargs)
                title = 'Formulario Htmx Modal'  # 'Departamento: %s | Documento: %s' % (self.object.departamento, self.object.tipodocumento)
                context.update({
                    'modal_form_title': title,
                    'confirm': True,
                    'texto_confirm': "Al confirmar no podrá modificar el documento.¡Esta acción no podrá revertirse!",
                })
                return context

            def get_success_url(self):
                return super().get_success_url()

            def form_valid(self, form):
                return super().form_valid(form)

            def form_invalid(self, form, **kwargs):
                return super().form_invalid(form, **kwargs)

        return CreateView

    def get_update_view(self):
        view = super().get_update_view()

        class UpdateView(view):

            def get_context_data(self, **kwargs):
                ctx = super(UpdateView, self).get_context_data(**kwargs)
                title = 'Formulario Ajax Modal'  # 'Departamento: %s | Documento: %s' % (self.object.departamento, self.object.tipodocumento)
                ctx.update({
                    'modal_form_title': title,
                    'max_width': '950px',
                    'hx_target': '#id_' + self.name + '_myList',
                    'confirm': True,
                    'texto_confirm': "Al confirmar no podrá modificar el documento.¡Esta acción no podrá revertirse!",
                    'object_model': self.model,
                })
                return ctx

            def get_success_url(self):
                return crud_inline_url(self.model_id, self.object, 'list', 'app_index:codificadores')

            def form_valid(self, form):
                event_action = None
                if self.request.method == 'POST':
                    event_action = self.request.POST.get('event_action', None)
                elif self.request.method == 'GET':
                    event_action = self.request.GET.get('event_action', None)
                target = '#id_%s_myList' % self.name
                try:
                    self.object = form.save(commit=False)
                    setattr(self.object, self.inline_field, self.model_id)
                    self.object.save()
                except IntegrityError as e:
                    # Maneja el error de integridad (duplicación de campos únicos)
                    mess_error = "El producto ya existe para la norma"
                    form.add_error(None, mess_error)
                    return self.form_invalid(form)
                return HttpResponseLocation(
                    self.get_success_url(),
                    target=target,
                    headers={
                        'HX-Trigger': self.request.htmx.trigger,
                        'HX-Trigger-Name': self.request.htmx.trigger_name,
                        'event_action': event_action,
                    },
                    values={
                        'event_action': event_action,
                    }
                )

        return UpdateView

    def get_delete_view(self):
        delete_view = super().get_delete_view()

        class DeleteView(delete_view):

            def get_context_data(self, **kwargs):
                context = super().get_context_data(**kwargs)
                return context

            def get_success_url(self):
                return super().get_success_url()

            def get(self, request, *args, **kwargs):
                return self.post(self, request, *args, **kwargs)

            def post(self, request, *args, **kwargs):
                return super().post(request, *args, **kwargs)

        return DeleteView

    def get_filter_list_view(self):
        filter_list_view = super().get_filter_list_view()

        class FilterListView(filter_list_view):
            inline_field = self.inline_field
            base_model = self.base_model
            name = self.name
            views_available = self.views_available[:]

            def get_context_data(self, **kwargs):
                context = super(FilterListView, self).get_context_data(**kwargs)
                return context

            def get_queryset(self):
                queryset = super(FilterListView, self).get_queryset()
                return queryset

            def get(self, request, *args, **kwargs):
                return filter_list_view.get(self, request, *args, **kwargs)

        return FilterListView


# ------ NormaConsumoDetalle / HtmxCRUD ------


# ------ NormaConsumo / CRUD ------
class NormaConsumoCRUD(CommonCRUDView):
    model = NormaConsumo

    namespace = 'app_index:codificadores'

    fields = [
        'fecha',
        'producto__tipoproducto',
        'producto',
        'cantidad',
        'medida',
        'confirmada',
        'activa',
    ]

    views_available = [
        'list',
        'create',
        'update',
        'delete',
        'detail',
    ]

    # Hay que agregar __icontains luego del nombre del campo para que busque el contenido
    # y no distinga entre mayúsculas y minúsculas.
    # En el caso de campos relacionados hay que agregar __<nombre_campo_que_se_muestra>__icontains
    search_fields = [
        'producto__tipoproducto',
        'cantidad__contains',
        'fecha',
        'medida__descripcion__icontains',
        'producto__descripcion__icontains',
    ]

    add_form = NormaConsumoForm
    update_form = NormaConsumoForm
    detail_form = NormaConsumoDetailForm

    list_fields = fields

    filter_fields = fields

    filterset_class = NormaConsumoFilter

    # Table settings
    table_class = NormaConsumoTable

    inlines = [NormaConsumoDetalleHtmxCRUD]

    # inline_tables = [
    #     {
    #         "table": NormaConsumoDetalleTable([]),
    #         "name": "normaconsumodetalletable",
    #         "visible": True,
    #     }
    # ]

    inline_actions = False

    def get_create_view(self):
        view = super().get_create_view()

        class OCreateView(view):

            def form_valid(self, form):
                if not self.related_fields:
                    return super(OCreateView, self).form_valid(form)

                self.object = form.save(commit=False)
                for key, value in self.context_rel.items():
                    setattr(self.object, key, value)
                self.object.save()
                edit_url = reverse_lazy(
                    crud_url_name(NormaConsumo, 'update', 'app_index:codificadores:'), args=[self.object.pk]
                )
                return HttpResponseLocation(
                    edit_url,
                    target='#main_content_swap',
                )

            def get_form_kwargs(self):
                form_kwargs = super().get_form_kwargs()
                form_kwargs.update(
                    {
                        "user": self.request.user,
                        "producto": self.request.GET['Producto'] if 'Producto' in self.request.GET else None,
                    }
                )
                return form_kwargs

        return OCreateView

    def get_filter_list_view(self):
        view = super().get_filter_list_view()

        class OFilterListView(view):
            def get_context_data(self, *, object_list=None, **kwargs):
                context = super().get_context_data(**kwargs)
                return_url = reverse_lazy(crud_url_name(NormaConsumoGrouped, 'list', 'app_index:codificadores:'))
                context.update({
                    'url_list_normaconsumo': False,
                    'return_url': return_url,
                    'confirm': True,
                    'activar': True,
                    'texto_confirm': "Al confirmar no podrá modificar la norma.!Esta acción no podrá revertirse!",
                    'texto_activar': "Las demás normas de este producto serán desactivadas",
                })
                pfilter = self.get_filter_dict()
                if 'producto__codigo' and 'producto__descripcion' in pfilter:
                    producto = ProductoFlujo.objects.get(
                        codigo=pfilter['producto__codigo'],
                        descripcion=pfilter['producto__descripcion']
                    )
                else:
                    producto = None
                context.update(self.get_filter_dict())
                context.update({'Producto': producto})
                return context

            def get_queryset(self):
                queryset = super(OFilterListView, self).get_queryset()
                qfilter = self.get_filter_dict()
                return queryset.filter(**qfilter)

            def get_filter_dict(self):
                qfilter = {}
                active_filters = self.filterset_class(self.request.GET).form.changed_data != []
                if active_filters and 'tipo' in self.filterset_class(self.request.GET).form.changed_data:
                    tipo = self.request.GET.get('tipo', None)
                else:
                    tipo = None
                producto = self.request.GET.get('Producto', None)
                if producto is not None:
                    if '?' in producto:
                        producto = producto.split('?')[0]
                    p = producto.split(' | ')
                    qfilter.update({
                        'producto__codigo': p[0],
                        'producto__descripcion': p[1]
                    })
                if tipo is not None:
                    qfilter.update({
                        'tipo': tipo
                    })
                return qfilter

        return OFilterListView

    def get_update_view(self):
        view = super().get_update_view()

        class OEditView(view):

            def get_context_data(self, **kwargs):
                ctx = super().get_context_data()
                if 'pk' in self.kwargs and self.inline_tables:
                    filter_dict = {'normaconsumo__id': self.kwargs['pk']}
                    data = NormaconsumoDetalle.objects.filter(**filter_dict)
                    self.inline_tables[0].update({
                        "table": NormaConsumoDetalleTable(data),
                    })
                    # for inline in self.inline_tables:
                    #     mdl = inline.model
                    #     base_mdl = inline.base_model
                    #     inline_field = inline.inline_field
                    #     filter_id = inline.inline_field + '__id'
                    #     filter_dict = {filter_id: self.kwargs['pk']}
                    #     inline.object_list = inline.model.objects.filter(**filter_dict)
                    #     inline.table = inline.table_class(inline.object_list)
                else:
                    inline_object_list = None
                    table = None
                ctx.update({
                    'inline_url_edit': reverse_lazy(
                        crud_url_name(NormaConsumo, 'update', 'app_index:codificadores:', ),
                        kwargs={'pk': self.kwargs['pk']}
                    ),
                    "add_button_href": 'app_index:codificadores:obtener_normaconsumodetalle_datos',
                    "add_button_hx_get": reverse_lazy('app_index:codificadores:obtener_normaconsumodetalle_datos'),
                    "add_button_hx_target": '#dialog_form',
                    "acept_btn_hx_get": self.get_success_url(),
                    "acept_btn_hx_target": '#main_content_swap',
                    "acept_btn_hx_swap": 'outerHTML',
                    "inline_tables": self.inline_tables,
                })
                return ctx

        return OEditView

    # def get_detail_view(self):
    #     view = super().get_detail_view()
    #
    #     class ODetailView(view):
    #
    #         def get_context_data(self, **kwargs):
    #             ctx = super().get_context_data()
    #             if 'pk' in kwargs:
    #                 obj = self.model.objects.get(id=self.kwargs['pk'])
    #                 ctx['form'] = self.form_class(instance=obj)
    #             elif 'object' in kwargs:
    #                 ctx['form'] = self.form_class(instance=kwargs['object'])
    #             return ctx
    #
    #     return ODetailView


class NormaConsumoGroupedCRUD(CommonCRUDView):
    env = {
        'normaconsumo': NormaConsumo
    }
    model = NormaConsumoGrouped

    namespace = 'app_index:codificadores'

    fields = [
        'tipo',
        'cantidad',
        'activa',
        'fecha',
        'medida',
        'producto',
        'Producto',
        'Tipo',
        'Cantidad_Normas',
    ]

    views_available = [
        'list',
        'create',
    ]

    # Hay que agregar __icontains luego del nombre del campo para que busque el contenido
    # y no distinga entre mayúsculas y minúsculas.
    # En el caso de campos relacionados hay que agregar __<nombre_campo_que_se_muestra>__icontains
    search_fields = [
        'tipo',
        'cantidad__contains',
        'fecha',
        'medida__descripcion__icontains',
        'producto__descripcion__icontains',
    ]

    add_form = NormaConsumoForm
    update_form = NormaConsumoForm

    list_fields = fields

    filter_fields = fields

    filterset_class = NormaConsumoGroupedFilter

    # Table settings
    table_class = NormaConsumoGroupedTable

    def get_filter_list_view(self):
        view = super().get_filter_list_view()

        class OFilterListView(view):
            def get_context_data(self, *, object_list=None, **kwargs):
                context = super().get_context_data(**kwargs)
                tipo = None
                active_filters = self.filterset_class(self.request.GET).form.changed_data != []
                if active_filters and 'tipo' in self.filterset_class(self.request.GET).form.changed_data:
                    tipo = self.filterset_class(self.request.GET).form.data.get('tipo', None)
                context.update({
                    'url_exportar': True,
                    'filtrar': True,
                    'url_importar': 'app_index:importar:nc_importar',
                    'url_list_normaconsumo': True,
                    'object2': self.env['normaconsumo'],
                    'return_url': None,
                    'tipo': tipo,
                })
                return context

            def get_queryset(self):
                queryset = super().get_queryset()
                return queryset

            def get(self, request, *args, **kwargs):
                myexport = request.GET.get("_export", None)
                if myexport and myexport == 'sisgest':
                    table = self.get_table(**self.get_table_kwargs())
                    datostable = table.data.data
                    idprods = [p['idprod'] for p in datostable]
                    datos = NormaConsumo.objects.select_related().filter(producto__id__in=idprods,
                                                                         confirmada=True)
                    datosdet = []
                    for d in datos:
                        datosdet.append(d.normaconsumodetalle_normaconsumo.all())
                    datos2 = [p.get() for p in datosdet]
                    return crear_export_datos_table(request, "NC", NormaConsumoGrouped, datos, datos2)
                else:
                    return super().get(request=request)

        return OFilterListView


# ------ UnidadContable / CRUD ------
class UnidadContableCRUD(CommonCRUDView):
    model = UnidadContable

    namespace = 'app_index:codificadores'

    fields = [
        'codigo',
        'nombre',
        'is_empresa',
        'is_comercializadora',
        'activo',
    ]

    # Hay que agregar __icontains luego del nombre del campo para que busque el contenido
    # y no distinga entre mayúsculas y minúsculas.
    # En el caso de campos relacionados hay que agregar __<nombre_campo_que_se_muestra>__icontains
    search_fields = [
        'codigo__icontains',
        'nombre__icontains',
        'activo',
        'is_empresa',
        'is_comercializadora',
    ]

    update_form = UnidadContableForm
    detail_form = UnidadContableDetailForm

    list_fields = [
        'codigo',
        'nombre',
        'activo',
        'is_empresa',
        'is_comercializadora',
    ]

    filter_fields = [
        'codigo',
        'nombre',
        'activo',
        'is_empresa',
        'is_comercializadora',
    ]

    views_available = ['list', 'update', 'detail']
    view_type = ['list', 'update']
    filterset_class = UnidadContableFilter

    # Table settings
    paginate_by = 15
    table_class = UnidadContableTable

    def get_filter_list_view(self):
        view = super().get_filter_list_view()

        class OFilterListView(view):
            def get_context_data(self, *, object_list=None, **kwargs):
                context = super().get_context_data(**kwargs)
                context.update({
                    'url_apiversat': 'app_index:apiversat:uc_apiversat',
                    'url_importar': 'app_index:importar:uc_importar',
                    'url_exportar': 'app_index:exportar:uc_exportar',
                    'sistema': 'VERSAT',
                })
                return context

        return OFilterListView


# ------ Medida / CRUD ------
class MedidaCRUD(CommonCRUDView):
    model = Medida

    namespace = 'app_index:codificadores'

    fields = [
        'clave',
        'descripcion',
        'activa',
    ]

    # Hay que agregar __icontains luego del nombre del campo para que busque el contenido
    # y no distinga entre mayúsculas y minúsculas.
    # En el caso de campos relacionados hay que agregar __<nombre_campo_que_se_muestra>__icontains
    search_fields = [
        'clave__icontains',
        'descripcion__icontains',
    ]

    add_form = MedidaForm
    update_form = MedidaForm

    list_fields = [
        'clave',
        'descripcion',
    ]

    filter_fields = [
        'clave',
        'descripcion',
    ]

    views_available = ['list', 'update']
    view_type = ['list', 'update']

    filterset_class = MedidaFilter

    # Table settings
    paginate_by = 15
    table_class = MedidaTable

    def get_filter_list_view(self):
        view = super().get_filter_list_view()

        class OFilterListView(view):
            def get_context_data(self, *, object_list=None, **kwargs):
                context = super().get_context_data(**kwargs)
                context.update({
                    'url_apiversat': 'app_index:appversat:um_appversat',
                    'url_importar': 'app_index:importar:um_importar',
                    'url_exportar': 'app_index:exportar:um_exportar',
                    'sistema': 'VERSAT',
                })
                return context

        return OFilterListView


# ------ MedidaConversion / CRUD ------
class MedidaConversionCRUD(CommonCRUDView):
    model = MedidaConversion

    namespace = 'app_index:codificadores'

    fields = [
        'factor_conversion',
        'medidao',
        'medidad',
    ]

    # Hay que agregar __icontains luego del nombre del campo para que busque el contenido
    # y no distinga entre mayúsculas y minúsculas.
    # En el caso de campos relacionados hay que agregar __<nombre_campo_que_se_muestra>__icontains
    search_fields = [
        'factor_conversion__contains',
        'medidao__descripcion__contains',
        'medidad__descripcion__contains',
    ]

    add_form = MedidaConversionForm
    update_form = MedidaConversionForm

    list_fields = [
        'factor_conversion',
        'medidao',
        'medidad',
    ]

    filter_fields = [
        'factor_conversion',
        'medidao',
        'medidad',
    ]
    filterset_class = MedidaConversionFilter

    # Table settings
    table_class = MedidaConversionTable

    def get_filter_list_view(self):
        view = super().get_filter_list_view()

        class OFilterListView(view):
            def get_context_data(self, *, object_list=None, **kwargs):
                context = super().get_context_data(**kwargs)
                context.update({
                    'url_importar': 'app_index:importar:umc_importar',
                    'url_exportar': 'app_index:exportar:umc_exportar',
                })
                return context

        return OFilterListView


# ------ Cuenta / CRUD ------
class CuentaCRUD(CommonCRUDView):
    model = Cuenta

    namespace = 'app_index:codificadores'

    fields = [
        'long_niv',
        'posicion',
        'clave',
        'descripcion',
        'activa',
    ]

    # Hay que agregar __icontains luego del nombre del campo para que busque el contenido
    # y no distinga entre mayúsculas y minúsculas.
    # En el caso de campos relacionados hay que agregar __<nombre_campo_que_se_muestra>__icontains
    search_fields = [
        'long_niv_contains',
        'posicion_contains',
        'clave_icontains',
        'descripcion_icontains',
        'activa',
    ]

    add_form = CuentaForm
    update_form = CuentaForm

    list_fields = [
        'long_niv',
        'posicion',
        'clave',
        'descripcion',
        'activa',
    ]

    filter_fields = [
        'long_niv',
        'posicion',
        'clave',
        'descripcion',
        'activa',
    ]

    views_available = ['list', 'update']
    view_type = ['list', 'update']

    filterset_class = CuentaFilter

    # Table settings
    paginate_by = 15
    table_class = CuentaTable

    def get_filter_list_view(self):
        view = super().get_filter_list_view()

        class OFilterListView(view):
            def get_context_data(self, *, object_list=None, **kwargs):
                context = super().get_context_data(**kwargs)
                context.update({
                    'url_apiversat': 'app_index:appversat:ccta_appversat',
                    'url_importar': 'app_index:importar:ccta_importar',
                    'url_exportar': 'app_index:exportar:ccta_exportar',
                    'sistema': 'VERSAT',
                })
                return context

        return OFilterListView


# ------ CentroCosto / CRUD ------
class CentroCostoCRUD(CommonCRUDView):
    model = CentroCosto

    namespace = 'app_index:codificadores'

    fields = [
        'clave',
        'descripcion',
        'activo',
    ]

    # Hay que agregar __icontains luego del nombre del campo para que busque el contenido
    # y no distinga entre mayúsculas y minúsculas.
    # En el caso de campos relacionados hay que agregar __<nombre_campo_que_se_muestra>__icontains
    search_fields = [
        'clave__icontains',
        'descripcion__icontains',
        'activo',
    ]

    add_form = CentroCostoForm
    update_form = CentroCostoForm

    list_fields = [
        'clave',
        'descripcion',
        'activo',
    ]

    filter_fields = [
        'clave',
        'descripcion',
        'activo',
    ]

    views_available = ['list', 'update']
    view_type = ['list', 'update']

    filterset_class = CentroCostoFilter

    # Table settings
    table_class = CentroCostoTable

    def get_filter_list_view(self):
        view = super().get_filter_list_view()

        class OFilterListView(view):
            def get_context_data(self, *, object_list=None, **kwargs):
                context = super().get_context_data(**kwargs)
                context.update({
                    'url_apiversat': 'app_index:apiversat:cc_apiversat',
                    'url_importar': 'app_index:importar:cc_importar',
                    'url_exportar': 'app_index:exportar:cc_exportar',
                    'sistema': 'VERSAT',
                })
                return context

        return OFilterListView


# ------ ProductoFlujo / CRUD ------
class ProductoFlujoCRUD(CommonCRUDView):
    model = ProductoFlujo

    namespace = 'app_index:codificadores'

    fields = [
        'codigo',
        'descripcion',
        'activo',
        'medida',
        'tipoproducto',
    ]

    # Hay que agregar __icontains luego del nombre del campo para que busque el contenido
    # y no distinga entre mayúsculas y minúsculas.
    # En el caso de campos relacionados hay que agregar __<nombre_campo_que_se_muestra>__icontains
    search_fields = [
        'codigo_icontains',
        'descripcion_icontains',
        'medida__descripcion__contains',
        'tipoproducto__descripcion__contains',
        'get_clasemateriaprima__descripcion__contains'
    ]

    add_form = ProductoFlujoForm
    update_form = ProductoFlujoUpdateForm

    list_fields = fields

    filter_fields = fields

    views_available = ['list', 'update', 'create', 'delete']
    view_type = ['list', 'update', 'create', 'delete']

    filterset_class = ProductoFlujoFilter

    # Table settings
    paginate_by = 15

    table_class = ProductoFlujoTable

    modal = True

    def get_filter_list_view(self):
        view = super().get_filter_list_view()

        class OFilterListView(view):
            def get_context_data(self, *, object_list=None, **kwargs):
                context = super().get_context_data(**kwargs)
                context.update({
                    'url_apiversat': 'app_index:codificadores:obtener_datos',
                    'url_importar': 'app_index:importar:prod_importar',
                    'filtrar': True,
                    'url_exportar': True,
                    "hx_get": reverse_lazy('app_index:codificadores:obtener_datos'),
                    # "hx_target": '#dialog',
                    # "hx_swap": 'outerHTML',
                    'sistema': 'VERSAT',
                })
                return context

            def get_queryset(self):
                qset = super().get_queryset()
                qset = qset.filter(
                    tipoproducto__in=[ChoiceTiposProd.MATERIAPRIMA, ChoiceTiposProd.SUBPRODUCTO]).exclude(
                    productoflujoclase_producto__clasemateriaprima=ChoiceClasesMatPrima.CAPACLASIFICADA)
                return qset

            def get(self, request, *args, **kwargs):
                myexport = request.GET.get("_export", None)
                if myexport and myexport == 'sisgest':
                    table = self.get_table(**self.get_table_kwargs())
                    datos = table.data.data
                    datos2 = [
                        dat.productoflujoclase_producto.get() if dat.tipoproducto.pk == ChoiceTiposProd.MATERIAPRIMA else None
                        for dat in datos]
                    if None in datos2:
                        datos2.remove(None)

                    return crear_export_datos_table(request, "PROD", ProductoFlujo, datos, datos2)
                else:
                    return super().get(request=request)

        return OFilterListView

    def get_update_view(self):
        view = super().get_update_view()

        class OEditView(view):

            def get_context_data(self, **kwargs):
                ctx = super().get_context_data()
                ctx.update({
                    'modal_form_title': 'Productos | Matrias Primas y Materiales',
                })
                return ctx

        return OEditView

    def get_create_view(self):
        view = super().get_create_view()

        class OCreateView(view):

            def get_context_data(self):
                ctx = super().get_context_data()
                ctx.update({
                    'modal_form_title': 'Productos | Matrias Primas y Materiales',
                })
                return ctx

        return OCreateView


# ------ ProductoFlujoCuenta / CRUD ------
class ProductoFlujoCuentaCRUD(CommonCRUDView):
    model = ProductoFlujoCuenta

    namespace = 'app_index:codificadores'

    fields = [
        'id',
        'cuenta',
        'producto',
    ]

    # Hay que agregar __icontains luego del nombre del campo para que busque el contenido
    # y no distinga entre mayúsculas y minúsculas.
    # En el caso de campos relacionados hay que agregar __<nombre_campo_que_se_muestra>__icontains
    search_fields = [
        'id__contains',
        'cuenta__descripcion__icontains',
        'producto__descripcion__icontains',
    ]

    add_form = ProductoFlujoCuentaForm
    update_form = ProductoFlujoCuentaForm

    list_fields = fields

    filter_fields = fields

    filterset_class = ProductoFlujoCuentaFilter

    # Table settings
    table_class = ProductoFlujoCuentaTable


# ------ Vitola / CRUD ------
class VitolaCRUD(CommonCRUDView):
    model = Vitola

    namespace = 'app_index:codificadores'

    fields = [
        'producto__codigo',
        'producto__descripcion',
        'diametro',
        'longitud',
        'cepo',
        'categoriavitola',
        'tipovitola',
        'destino',
        'producto__activo',
    ]

    # Hay que agregar __icontains luego del nombre del campo para que busque el contenido
    # y no distinga entre mayúsculas y minúsculas.
    # En el caso de campos relacionados hay que agregar __<nombre_campo_que_se_muestra>__icontains
    search_fields = [
        'producto__codigo__icontains',
        'producto__descripcion__icontains',
        'diametro__contains',
        'longitud__contains',
        'cepo__contains',
        'categoriavitola__descripcion__contains',
        'tipovitola__descripcion__icontains',
        'destino__icontains',
    ]

    add_form = VitolaForm
    update_form = VitolaForm

    list_fields = fields

    filter_fields = fields

    filterset_class = VitolaFilter

    # Table settings
    paginate_by = 15
    table_class = VitolaTable

    def get_filter_list_view(self):
        view = super().get_filter_list_view()

        class OFilterListView(view):
            def get_context_data(self, *, object_list=None, **kwargs):
                context = super().get_context_data(**kwargs)
                context.update({
                    'url_apiversat': 'app_index:appversat:vit_appversat',
                    'url_importar': 'app_index:importar:vit_importar',
                    'url_exportar': True,
                    'filtrar': True,
                    'sistema': 'Sispax'
                })
                return context

            def get(self, request, *args, **kwargs):
                myexport = request.GET.get("_export", None)
                if myexport and myexport == 'sisgest':
                    table = self.get_table(**self.get_table_kwargs())
                    datos2 = table.data.data
                    datos = []
                    for p in datos2:
                        datos.append(p.producto)
                        datos.append(p.capa)
                        datos.append(p.pesada)
                    return crear_export_datos_table(request, "Vit", Vitola, datos, datos2)
                else:
                    return super().get(request=request)

            def post(self, request, *args, **kwargs):
                self.object = self.get_object()
                try:
                    self.object.delete()
                except ProtectedError as e:
                    protected_details = ", ".join([str(obj) for obj in e.protected_objects])
                    title = _('Cannot delete ')
                    text = _('This element is related to: ')
                    message_error(self.request,
                                  title + self.object.__str__() + '!',
                                  text=text + protected_details)
                    return HttpResponseRedirect(self.get_success_url())
                if self.success_message:
                    messages.success(self.request, self.success_message)
                return HttpResponseRedirect(self.get_success_url())

        return OFilterListView


# ------ MarcaSalida / CRUD ------
class MarcaSalidaCRUD(CommonCRUDView):
    model = MarcaSalida

    namespace = 'app_index:codificadores'

    fields = [
        'codigo',
        'descripcion',
        'activa',
    ]

    # Hay que agregar __icontains luego del nombre del campo para que busque el contenido
    # y no distinga entre mayúsculas y minúsculas.
    # En el caso de campos relacionados hay que agregar __<nombre_campo_que_se_muestra>__icontains
    search_fields = [
        'codigo__icontains',
        'descripcion__icontains',
    ]

    add_form = MarcaSalidaForm
    update_form = MarcaSalidaForm

    list_fields = fields

    filter_fields = fields

    views_available = ['list', 'update', 'create']
    view_type = ['list', 'update', 'create']

    filterset_class = MarcaSalidaFilter

    # Table settings
    paginate_by = 15
    table_class = MarcaSalidaTable

    def get_filter_list_view(self):
        view = super().get_filter_list_view()

        class OFilterListView(view):
            def get_context_data(self, *, object_list=None, **kwargs):
                context = super().get_context_data(**kwargs)
                context.update({
                    'url_apiversat': 'app_index:appversat:ms_appversat',
                    'url_importar': 'app_index:importar:ms_importar',
                    'url_exportar': 'app_index:exportar:ms_exportar',
                    'sistema': 'SisGestMP',
                })
                return context

        return OFilterListView


# ------ MotivoAjuste / CRUD ------
class MotivoAjusteCRUD(CommonCRUDView):
    model = MotivoAjuste

    namespace = 'app_index:codificadores'

    fields = [
        'descripcion',
        'aumento',
        'activo',
    ]

    # Hay que agregar __icontains luego del nombre del campo para que busque el contenido
    # y no distinga entre mayúsculas y minúsculas.
    # En el caso de campos relacionados hay que agregar __<nombre_campo_que_se_muestra>__icontains
    search_fields = [
        'descripcion__icontains',
        'aumento',
        'activo',
    ]

    add_form = MotivoAjusteForm
    update_form = MotivoAjusteForm

    list_fields = fields

    filter_fields = fields

    views_available = ['list', 'update', 'create', 'delete']
    view_type = ['list', 'update', 'create', 'delete']

    filterset_class = MotivoAjusteFilter

    # Table settings
    table_class = MotivoAjusteTable

    def get_filter_list_view(self):
        view = super().get_filter_list_view()

        class OFilterListView(view):
            def get_context_data(self, *, object_list=None, **kwargs):
                context = super().get_context_data(**kwargs)
                context.update({
                    'url_importar': 'app_index:importar:ma_importar',
                    'url_exportar': 'app_index:exportar:ma_exportar',
                })
                return context

        return OFilterListView


# ------ Cambio de Producto / CRUD ------
class CambioProductoCRUD(CommonCRUDView):
    model = CambioProducto

    namespace = 'app_index:codificadores'

    fields = [
        'productoo',
        'productod',
    ]

    # Hay que agregar __icontains luego del nombre del campo para que busque el contenido
    # y no distinga entre mayúsculas y minúsculas.
    # En el caso de campos relacionados hay que agregar __<nombre_campo_que_se_muestra>__icontains
    search_fields = [
        'productoo__descripcion__contains',
        'productod__descripcion__contains',
    ]

    add_form = CambioProductoForm
    update_form = CambioProductoForm

    list_fields = [
        'productoo',
        'productoo',
    ]

    filter_fields = list_fields

    filterset_class = CambioProductoFilter

    # Table settings
    table_class = CambioProductoTable

    def get_filter_list_view(self):
        view = super().get_filter_list_view()

        class OFilterListView(view):
            def get_context_data(self, *, object_list=None, **kwargs):
                context = super().get_context_data(**kwargs)
                context.update({
                    'url_importar': 'app_index:importar:cprod_importar',
                    'url_exportar': 'app_index:exportar:cprod_exportar',
                })
                return context

        return OFilterListView


# ------ LineaSalida / CRUD ------
class LineaSalidaCRUD(CommonCRUDView):
    model = LineaSalida

    namespace = 'app_index:codificadores'

    fields = [
        'producto__codigo',
        'producto__descripcion',
        'envase',
        'vol_cajam3',
        'peso_bruto',
        'peso_neto',
        'peso_legal',
        'marcasalida',
        'vitola',
        'producto__activo'
    ]

    # Hay que agregar __icontains luego del nombre del campo para que busque el contenido
    # y no distinga entre mayúsculas y minúsculas.
    # En el caso de campos relacionados hay que agregar __<nombre_campo_que_se_muestra>__icontains
    search_fields = [
        'producto__codigo__icontains',
        'producto__descripcion__icontains',
        'envase__contains',
        'vol_cajam3__contains',
        'peso_bruto__contains',
        'peso_neto__contains',
        'peso_legal__contains',
        'marcasalida__descripcion__contains',
    ]

    add_form = LineaSalidaForm
    update_form = LineaSalidaForm

    list_fields = fields

    filter_fields = fields

    filterset_class = LineaSalidaFilter

    # Table settings
    paginate_by = 15
    table_class = LineaSalidaTable

    def get_filter_list_view(self):
        view = super().get_filter_list_view()

        class OFilterListView(view):
            def get_context_data(self, *, object_list=None, **kwargs):
                context = super().get_context_data(**kwargs)
                context.update({
                    'url_importar': 'app_index:importar:ls_importar',
                    'url_exportar': True,
                    'filtrar': True
                })
                return context

            def get(self, request, *args, **kwargs):
                myexport = request.GET.get("_export", None)
                if myexport and myexport == 'sisgest':
                    table = self.get_table(**self.get_table_kwargs())
                    datos2 = table.data.data
                    datos = []
                    for p in datos2:
                        datos.append(p.producto)
                    return crear_export_datos_table(request, "LS", LineaSalida, datos, datos2)
                else:
                    return super().get(request=request)

        return OFilterListView


# ------ ProductsCapasClaPesadas / CRUD ------
class ProductsCapasClaPesadasCRUD(CommonCRUDView):
    model = ProductsCapasClaPesadas

    namespace = 'app_index:codificadores'

    fields = [
        'codigo',
        'descripcion',
        'activo',
        'medida',
        'tipoproducto',
    ]

    # Hay que agregar __icontains luego del nombre del campo para que busque el contenido
    # y no distinga entre mayúsculas y minúsculas.
    # En el caso de campos relacionados hay que agregar __<nombre_campo_que_se_muestra>__icontains
    search_fields = [
        'codigo_icontains',
        'descripcion_icontains',
        'medida__descripcion__contains',
        'tipoproducto__descripcion__contains',
    ]

    list_fields = fields

    filter_fields = fields

    views_available = ['list']
    view_type = ['list']

    filterset_class = ProductsCapasClaPesadasFilter

    # Table settings
    paginate_by = 20

    table_class = ProductsCapasClaPesadasTable

    def get_filter_list_view(self):
        view = super().get_filter_list_view()

        class OFilterListView(view):
            def get_context_data(self, *, object_list=None, **kwargs):
                context = super().get_context_data(**kwargs)
                context.update({})
                return context

        return OFilterListView


# ------ NumeracionDocumentos / CRUD ------
class NumeracionDocumentosCRUD(CommonCRUDView):
    model = NumeracionDocumentos

    namespace = 'app_index:codificadores'

    fields = [
        'id',
        'sistema',
        'departamento',
        'prefijo'
    ]

    add_form = NumeracionDocumentosForm
    update_form = NumeracionDocumentosForm

    list_fields = fields

    filter_fields = fields

    views_available = ['list', 'update', 'create']
    view_type = ['list', 'update', 'create']

    # Table settings
    paginate_by = 5
    table_class = NumeracionDocumentosTable

    def get_filter_list_view(self):
        view = super().get_filter_list_view()

        class OFilterListView(view):
            def get_context_data(self, *, object_list=None, **kwargs):
                context = super().get_context_data(**kwargs)
                context.update({
                    'url_importar': 'app_index:importar:numdoc_importar',
                    'filter': False,
                    'url_exportar': 'app_index:exportar:numdoc_exportar'
                })
                return context

        return OFilterListView


class ConfCentrosElementosOtrosDetalleGroupedCRUD(CommonCRUDView):
    env = {
        'confdetalle': ConfCentrosElementosOtrosDetalle
    }
    model = ConfCentrosElementosOtrosDetalleGrouped

    namespace = 'app_index:codificadores'

    fields = [
        'descripcion',
        'valor',
        'clave',
        'Clave',
        'Elementos',
    ]

    views_available = [
        'create',
        'list',
        'detail',
        'delete',
        'update',
    ]

    # Hay que agregar __icontains luego del nombre del campo para que busque el contenido
    # y no distinga entre mayúsculas y minúsculas.
    # En el caso de campos relacionados hay que agregar __<nombre_campo_que_se_muestra>__icontains
    search_fields = [
        'clave__clave__icontains',
    ]

    list_fields = fields

    filter_fields = fields

    filterset_class = ConfCentrosElementosOtrosDetalleGroupedFilter

    # Table settings
    table_class = ConfCentrosElementosOtrosDetalleGroupedTable

    def get_filter_list_view(self):
        view = super().get_filter_list_view()

        class OFilterListView(view):
            def get_context_data(self, *, object_list=None, **kwargs):
                context = super().get_context_data(**kwargs)
                context.update({
                    'url_importar': 'app_index:importar:confccelemg_importar',
                    'filtrar': True,
                    'filter': False,
                    'url_exportar': True,
                    'object2': self.env['confdetalle'],
                    'return_url': None,
                })
                return context

            def get_queryset(self):
                queryset = super().get_queryset()
                return queryset

            def get(self, request, *args, **kwargs):
                myexport = request.GET.get("_export", None)
                if myexport and myexport == 'sisgest':
                    table = self.get_table(**self.get_table_kwargs())
                    datos = ConfCentrosElementosOtrosDetalle.objects.all()
                    datos2 = []
                    return crear_export_datos_table(request, "CONF_CC_ELEM", ConfCentrosElementosOtrosDetalleGrouped,
                                                    datos, datos2)
                else:
                    return super().get(request=request)

        return OFilterListView


# ------ ConfCentrosElementosOtrosDetalle / CRUD ------
class ConfCentrosElementosOtrosDetalleCRUD(CommonCRUDView):
    model = ConfCentrosElementosOtrosDetalle

    namespace = 'app_index:codificadores'

    fields = [
        'descripcion',
        'valor',
    ]

    # Hay que agregar __icontains luego del nombre del campo para que busque el contenido
    # y no distinga entre mayúsculas y minúsculas.
    # En el caso de campos relacionados hay que agregar __<nombre_campo_que_se_muestra>__icontains
    search_fields = [
        'valor__contains',
        'descripcion__icontains',
    ]

    update_form = ConfCentrosElementosOtrosDetalleForm

    list_fields = fields

    filter_fields = fields

    views_available = ['list', 'update']
    view_type = ['list', 'update']

    filterset_class = ConfCentrosElementosOtrosDetalleFilter

    # Table settings
    table_class = ConfCentrosElementosOtrosDetalleTable

    def get_filter_list_view(self):
        view = super().get_filter_list_view()

        class OFilterListView(view):
            def get_context_data(self, *, object_list=None, **kwargs):
                context = super().get_context_data(**kwargs)
                return_url = reverse_lazy(
                    crud_url_name(ConfCentrosElementosOtrosDetalleGrouped, 'list', 'app_index:codificadores:'))
                context.update({
                    'return_url': return_url,
                })
                return context

            def get_queryset(self):
                queryset = super(OFilterListView, self).get_queryset()

                qfilter = {}
                clave = self.request.GET.get('Clave', None)

                if clave is not None:
                    qfilter.update({
                        'clave_id': clave,
                    })
                    queryset = queryset.filter(**qfilter)

                return queryset

        return OFilterListView

    def get_update_view(self):
        view = super().get_update_view()

        class OEditView(view):

            def get_context_data(self, **kwargs):
                ctx = super().get_context_data(**kwargs)
                ctx.update({
                    'modal_form_title': 'Centros de Costo | Elementos',
                })
                return ctx

        return OEditView


class ObtenrDatosModalFormView(BaseModalFormView):
    template_name = 'app_index/modals/modal_form.html'
    form_class = ObtenerDatosModalForm
    viewname = {'submitted': 'app_index:appversat:prod_appversat'}
    hx_target = '#main_content_swap'
    hx_swap = 'outerHTML'
    hx_retarget = '#dialog'
    hx_reswap = 'outerHTML',
    modal_form_title = 'Obtener Datos'
    max_width = '500px'


class NormaConsumoDetalleModalFormView(FormView):
    template_name = 'app_index/modals/modal_form.html'
    form_class = NormaConsumoDetalleForm

    def form_valid(self, form):
        if form.is_valid():
            norma_ramal = form.cleaned_data['norma_ramal']
            norma_empresarial = form.cleaned_data['norma_empresarial']
            operativo = form.cleaned_data['operativo']
            producto = form.cleaned_data['producto']
            medida = form.cleaned_data['medida']
            self.success_url = reverse_lazy(
                'app_index:appversat:prod_appversat',
                kwargs={
                    'norma_ramal': norma_ramal,
                    'norma_empresarial': norma_empresarial,
                    'operativo': operativo,
                    'producto': producto,
                    'medida': medida,
                }
            )

            return HttpResponseLocation(
                self.get_success_url(),
                target='#main_content_swap',

            )
        else:
            return render(self.request, 'app_index/modals/modal_form.html', {
                'form': form,
            })


def classmatprima(request):
    tipoproducto = request.GET.get('tipoproducto')
    clasemp = request.GET.get('clase')
    clases_mp = ClaseMateriaPrima.objects.all().exclude(pk=ChoiceClasesMatPrima.CAPACLASIFICADA)
    tipoprod = TipoProducto.objects.all()
    data = {
        'tipoproducto': tipoproducto,
        'clase': clasemp,
        'precio_lop': 0.0,
    }
    form = ProductoFlujoForm(data)
    form.fields['clase'].queryset = clases_mp
    esmatprim = None if tipoproducto != str(ChoiceTiposProd.MATERIAPRIMA) else 1
    if not esmatprim:
        form.fields['clase'].disabled = True
        form.fields['clase'].widget.attrs.update({'style': 'display: none;'})
        form.fields['clase'].label = False
        form.fields['clase'].required = False
    else:
        form.fields['clase'].disabled = False
        form.fields['clase'].required = True
        form.fields['clase'].label = 'Clase Mat. Prima'
        form.fields['clase'].widget.attrs.update({
            'style': "width: 100%",
            'hx-get': reverse_lazy('app_index:codificadores:rendimientocapa'),
            'hx-target': "#div_id_rendimientocapa",
            # 'hx-swap': 'outerHTML',
            'hx-trigger': "change",
            'hx-include': '[name="rendimientocapa"]'
        })
    response = HttpResponse(
        as_crispy_field(form['clase']).replace('is-invalid', ''),
        content_type='text/html'
    )
    return response


def precio_lop(request):
    tipoproducto = request.GET.get('tipoproducto')
    clase = request.GET.get('clase')
    precio = request.GET.get('precio_lop')
    data = {
        'tipoproducto': tipoproducto,
        'clase': clase,
        'precio_lop': precio,
    }
    form = ProductoFlujoForm(data)
    esmatprim = None if tipoproducto != str(ChoiceTiposProd.MATERIAPRIMA) else 1
    if not esmatprim:
        form.fields['precio_lop'].widget.attrs.update({'style': 'display: none;'})
        form.fields['precio_lop'].label = False
        form.fields['precio_lop'].required = False
    else:
        form.fields['precio_lop'].required = True
        form.fields['precio_lop'].label = 'Precio LOP'
        form.fields['precio_lop'].widget.attrs.update({
            'decimal_places': 4,
            'max_digits': 10,
            'min_value': 0.0000,
            'step': "0.0001",
            'min': "0.0000",
            'style': 'display: block;',
            'hx-get': reverse_lazy('app_index:codificadores:precio_lop'),
            'hx-target': '#div_id_precio_lop',
            # 'hx-swap': 'outerHTML',
            'hx-trigger': 'change from:#div_id_tipoproducto',
            'hx-include': '[name="clase"], [name="tipoproducto"]',
        })
    response = HttpResponse(as_crispy_field(form['precio_lop']), content_type='text/html')
    return response


def rendimientocapa(request):
    clasemp = request.GET.get('clase')
    codigo = request.GET.get('codigo')
    clasemp = '0' if not clasemp else clasemp
    rendimientocapa = request.GET.get('rendimientocapa')
    rendimientocapa = rendimientocapa if rendimientocapa else '0'
    catvitolas = CategoriaVitola.objects.all()
    seleccvitolas = []
    prod = ProductoFlujo.objects.filter(codigo=codigo)
    if int(clasemp) == ChoiceClasesMatPrima.CAPASINCLASIFICAR and codigo and prod.exists():
        vitolas = prod.first().vitolas.all()
        seleccvitolas = [x.pk for x in vitolas]
    context = {
        'show_rendimiento': True if int(clasemp) == ChoiceClasesMatPrima.CAPASINCLASIFICAR else False,
        'valorrendimientocapa': rendimientocapa,
        'seleccvitolas': seleccvitolas,
        'vitolas': catvitolas,
    }
    data = {
        'vitolas': catvitolas,
        'clase': clasemp,
        'rendimientocapa': rendimientocapa,
    }
    form = ProductoFlujoForm(data)
    show_rendimiento = True if int(clasemp) == ChoiceClasesMatPrima.CAPASINCLASIFICAR else False
    if not show_rendimiento:
        form.fields['rendimientocapa'].disabled = True
        form.fields['rendimientocapa'].widget.attrs.update({'style': 'display: none;'})
        form.fields['rendimientocapa'].label = False
        form.fields['rendimientocapa'].required = False
    else:
        form.fields['rendimientocapa'].disabled = False
        # form.fields['rendimientocapa'].required = True
        form.fields['rendimientocapa'].label = 'Rend. Capa'
        form.fields['rendimientocapa'].widget.attrs.update({
            'style': "display: block;",
        })
    response = HttpResponse(as_crispy_field(form['rendimientocapa']), content_type='text/html')
    return response


def vitolas(request):
    tipoproducto = request.GET.get('tipoproducto')
    clasemp = request.GET.get('clase')
    codigo = request.GET.get('codigo', '0')
    # get_rendimientocapa = request.GET.get('rendimientocapa', '0')
    get_vitolas = request.GET.get('vitolas', None)
    catvitolas = CategoriaVitola.objects.all()
    seleccvitolas = []
    prod = ProductoFlujo.objects.filter(codigo=codigo)
    if int(clasemp) == ChoiceClasesMatPrima.CAPASINCLASIFICAR and codigo and prod.exists():
        vitolas = prod.first().vitolas.all()
        seleccvitolas = [x.pk for x in vitolas]
    context = {
        'show_rendimiento': True if int(clasemp) == ChoiceClasesMatPrima.CAPASINCLASIFICAR else False,
        'valorrendimientocapa': rendimientocapa,
        'seleccvitolas': seleccvitolas,
        'vitolas': catvitolas,
    }
    data = {
        'codigo': codigo,
        # 'vitolas': get_vitolas,
        'clase': clasemp,
        # 'rendimientocapa': get_rendimientocapa,
    }
    form = ProductoFlujoForm(data)
    show_rendimiento = True if int(clasemp) == ChoiceClasesMatPrima.CAPASINCLASIFICAR else False
    esmatprim = None if tipoproducto != str(ChoiceTiposProd.MATERIAPRIMA) else 1
    if not show_rendimiento:
        form.fields['vitolas'].widget.attrs.update({'style': 'display: none;'})
        form.fields['vitolas'].label = False
        form.fields['vitolas'].required = False
    else:
        form.fields['vitolas'].widget.attrs.update({
            'style': 'display: block;',
            'hx-get': reverse_lazy('app_index:codificadores:vitolas'),
            'hx-target': '#div_id_vitolas',
            'hx-swap': 'outerHTML',
            'hx-trigger': 'change from:#div_id_clase',
            'hx-include': '[name="clase"], [name="codigo"], [name="tipoproducto"]',
        })
        form.fields['vitolas'].required = True
        form.fields['vitolas'].label = 'Vitolas'
        # print(as_crispy_field(form['vitolas']))
    field = as_crispy_field(form['vitolas'])
    field = field.replace('is-invalid', '')
    response = HttpResponse(field, content_type='text/html')
    return response


def cargonorma(request):
    produccion = request.GET.get('vinculo_produccion')
    nr = request.GET.get('nr_media')
    norma = request.GET.get('norma_tiempo')

    context = {
        'show_norma_tiempo': True,
        'show_nr_media': produccion == str(VinculoCargoProduccion.DIRECTO),
        'valornr_media': nr if nr else 0,
        'valornorma_tiempo': norma if norma else 0.0000,
    }
    return render(request, 'app_index/partials/clasifcargosnormas.html', context)


def calcula_nt(request):
    nr = request.GET.get('nr_media')
    norma = 8 / int(nr) if nr and int(nr) > 0 else 0.0000
    nt = round(norma, 4)
    context = {
        'show_norma_tiempo': True,
        'show_nr_media': True,
        'valornorma_tiempo': '%.4f' % nt,
        'valornr_media': nr if nr else 0,
    }
    return render(request, 'app_index/partials/clasifcargosnormas.html', context)


# ------ TipoDocumento / CRUD ------
class TipoDocumentoCRUD(CommonCRUDView):
    model = TipoDocumento

    namespace = 'app_index:codificadores'

    fields = [
        'descripcion',
        'operacion',
        'generado',
        'prefijo'
    ]

    add_form = TipoDocumentoForm
    update_form = TipoDocumentoForm

    list_fields = fields

    filter_fields = fields

    views_available = ['list', 'update']
    view_type = ['list', 'update']

    # Table settings
    paginate_by = 25
    table_class = TipoDocumentoTable

    def get_filter_list_view(self):
        view = super().get_filter_list_view()

        class OFilterListView(view):
            def get_context_data(self, *, object_list=None, **kwargs):
                context = super().get_context_data(**kwargs)
                context.update({
                    'url_importar': 'app_index:importar:numdoc_importar',
                    'filter': False,
                    'url_exportar': 'app_index:exportar:numdoc_exportar'
                })
                return context

        return OFilterListView


def confirm_nc(request, pk):
    obj = NormaConsumo.objects.get(pk=pk)
    if obj.normaconsumodetalle_normaconsumo.count() > 0:
        obj.confirmada = True
        obj.save()
    else:
        title = 'No puede ser confrimada la norma de consumo '
        text = 'No tiene productos asociados'
        message_error(request,
                      title + obj.__str__() + '!',
                      text=text)
    return redirect(
        reverse_lazy(crud_url_name(NormaConsumo, 'list', 'app_index:codificadores:')) + "?Producto=" + request.GET[
            'Producto'])


def activar_nc(request, pk):
    with transaction.atomic():
        obj = NormaConsumo.objects.get(pk=pk)
        product = obj.producto
        objs = NormaConsumo.objects.filter(producto=product).update(activa=False)
        obj.activa = True
        obj.save()
    return redirect(
        reverse_lazy(crud_url_name(NormaConsumo, 'list', 'app_index:codificadores:')) + "?Producto=" + request.GET[
            'Producto'])


def productmedida(request):
    pk_prod = request.GET.get('producto')
    producto = ProductoFlujo.objects.get(pk=pk_prod)
    medida_seleccionada = producto.medida
    medidas = Medida.objects.filter(activa=True)
    context = {
        'medidas': medidas,
        'medida_seleccionada': medida_seleccionada,
    }
    return render(request, 'app_index/partials/productmedida.html', context)


def productmedidadetalle(request):
    pk_prod = request.GET.get('idproducto')
    producto = ProductoFlujo.objects.get(pk=pk_prod)
    medida_seleccionada = producto.medida
    result = {"id": medida_seleccionada.pk}
    return JsonResponse({"results": result})


# ------ ClasificadorCargos / CRUD ------
class ClasificadorCargosCRUD(CommonCRUDView):
    model = ClasificadorCargos

    namespace = 'app_index:codificadores'

    fields = [
        'codigo',
        'descripcion',
        'grupo__grupo',
        'actividad',
        'vinculo_produccion',
        'activo',
        'unidadcontable'
    ]

    # Hay que agregar __icontains luego del nombre del campo para que busque el contenido
    # y no distinga entre mayúsculas y minúsculas.
    # En el caso de campos relacionados hay que agregar __<nombre_campo_que_se_muestra>__icontains
    search_fields = [
        'codigo__contains',
        'descripcion__icontains',
        'grupo__grupo__icontains',
        'actividad__icontains',
        'grupo__salario__contains',
        'vinculo_produccion__icontains',
        'activo',
        'unidadcontable__nombre__icontains',
    ]

    add_form = ClasificadorCargosForm
    update_form = ClasificadorCargosForm

    list_fields = fields

    filter_fields = fields

    filterset_class = ClasificadorCargosFilter

    # Table settings
    table_class = ClasificadorCargosTable

    def get_filter_list_view(self):
        view = super().get_filter_list_view()

        class OFilterListView(view):
            def get_context_data(self, *, object_list=None, **kwargs):
                context = super().get_context_data(**kwargs)
                context.update({
                    'url_importar': 'app_index:importar:clacargos_importar',
                    'filtrar': True,
                    'url_exportar': True,
                })
                return context

            def get(self, request, *args, **kwargs):
                myexport = request.GET.get("_export", None)
                if myexport and myexport == 'sisgest':
                    table = self.get_table(**self.get_table_kwargs())
                    datos = table.data.data
                    return crear_export_datos_table(request, "CLA_CARG", ClasificadorCargos, datos, None)
                else:
                    return super().get(request=request)

        return OFilterListView


# ------ FichaCostoFilas / CRUD ------
class FichaCostoFilasCRUD(CommonCRUDView):
    model = FichaCostoFilas

    namespace = 'app_index:codificadores'

    fields = [
        'fila',
        'descripcion',
        'encabezado',
        'salario',
        'vacaciones',
        'desglosado',
        'calculado',
        'filasasumar',
        'padre'
    ]

    # Hay que agregar __icontains luego del nombre del campo para que busque el contenido
    # y no distinga entre mayúsculas y minúsculas.
    # En el caso de campos relacionados hay que agregar __<nombre_campo_que_se_muestra>__icontains
    search_fields = [
        'descripcion__icontains',
        'encabezado',
        'salario',
        'vacaciones',
        'desglosado',
        'calculado',
        'filasasumar__fila__contains',
    ]

    add_form = FichaCostoFilasForm
    update_form = FichaCostoFilasForm

    list_fields = fields

    filter_fields = fields

    filterset_class = FichaCostoFilasFilter

    # Table settings
    table_class = FichaCostoFilasTable

    def get_filter_list_view(self):
        view = super().get_filter_list_view()

        class OFilterListView(view):
            def get_context_data(self, *, object_list=None, **kwargs):
                context = super().get_context_data(**kwargs)
                context.update({
                    'row_nodelete': ['1', '1.1', '1.2'],
                    'url_importar': 'app_index:importar:filafichacosto_importar',
                    'url_exportar': 'app_index:exportar:filafichacosto_exportar',
                })
                return context

        return OFilterListView

    def get_create_view(self):
        view = super().get_create_view()

        class OCreateView(view):

            def get_form_kwargs(self):
                form_kwargs = super().get_form_kwargs()
                padre = self.request.GET.get('padre', None)
                form_kwargs.update(
                    {
                        "padre": padre,
                    }
                )
                return form_kwargs

        return OCreateView


def fila_encabezado(request):
    encabezado = False if not request.GET.get('encabezado') else True
    fila = request.GET.get('fila')
    obj = FichaCostoFilas.objects.filter(fila=fila).first()
    encabezado = True if not obj else obj.encabezado
    padre = request.GET.get('padre')
    if padre and int(padre) > 0 and request.GET.get('encabezado') and request.GET.get('encabezado') == 'on':
        encabezado = True
    elif int(padre) > 0:
        encabezado = False

    calculado = False if not request.GET.get('calculado') else True
    show_desglosado = not encabezado
    show_calculado = encabezado
    value_desglosado = obj.desglosado if obj and show_desglosado else False
    value_calculado = False
    desglose_disabled = fila in ['1.1', '1.2']
    if show_calculado:
        pk_padre = padre  # if padre and padre != '0' else obj.parent.pk
        filasasumar = FichaCostoFilas.objects.filter(encabezado=True, parent=None).exclude(fila=fila).exclude(pk=pk_padre).all()
        show_calculado = False if not filasasumar else show_calculado
        value_calculado = obj.calculado if obj and show_calculado else False

    context = {
        'show_desglosado': show_desglosado,
        'show_calculado': show_calculado,
        'value_desglosado': value_desglosado,
        'value_calculado': value_calculado,
        'desglose_disabled': desglose_disabled,
        'padre': request.GET.get('padre'),
    }
    return render(request, 'app_index/partials/filasfichacostoencabezado.html', context)


def fila_desglosado(request):
    desglosado = True if request.GET.get('desglosado') and request.GET.get('desglosado') == 'on' else False

    fila = request.GET.get('fila')
    obj = FichaCostoFilas.objects.filter(fila=fila).first()
    encabezado = True if not obj else True
    if request.GET.get('padre') and int(request.GET.get('padre')) > 0 and request.GET.get('encabezado') and request.GET.get('encabezado') == 'on':
        encabezado = True
    elif int(request.GET.get('padre')) > 0:
        encabezado = False
    show_salario = desglosado and not fila in ['1.1', '1.2']
    show_vacaciones = not desglosado and not encabezado
    value_salario = show_salario

    context = {
        'show_salario': show_salario,
        'value_salario': value_salario,
        'show_vacaciones': show_vacaciones,
        'padre': request.GET.get('padre'),
    }
    return render(request, 'app_index/partials/filasfichacostodesglosado.html', context)


def fila_calculado(request):
    calculado = False if not request.GET.get('calculado') else True
    fila = request.GET.get('fila')
    padre = request.GET.get('padre')
    obj = FichaCostoFilas.objects.filter(fila=fila).first()
    show_filasasumar = calculado
    filasasumar = []
    filasasumarselecc = []
    pk_padre = padre  # if padre and padre!='0' else obj.parent.pk
    filasasumar = FichaCostoFilas.objects.filter(encabezado=True, parent=None).exclude(fila=fila).exclude(pk=pk_padre).all()
    show_filasasumar = calculado
    selecc = obj.filasasumar.all() if obj else []
    filasumarselecc = [x.pk for x in selecc]

    context = {
        'show_filasasumar': show_filasasumar,
        'filasasumar': filasasumar,
        'filasumarselecc': filasumarselecc,
    }
    return render(request, 'app_index/partials/filasfichacostocalculado.html', context)
