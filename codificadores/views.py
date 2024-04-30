from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django_htmx.http import HttpResponseLocation
from extra_views import CreateWithInlinesView

from app_index.views import CommonCRUDView
from codificadores.filters import *
from codificadores.forms import *
from codificadores.tables import *
from cruds_adminlte3.inline_crud import InlineAjaxCRUD
from exportar.views import crear_export_datos_table
from . import ChoiceTiposProd
from .inlines import NormaconsumoDetalleInline


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
        'departamentoproducto',
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
    title = "Detalles de normas de consumo"
    table_class = NormaConsumoDetalleTable


# ------ NormaConsumo / CRUD ------
class NormaConsumoCRUD(CommonCRUDView):
    model = NormaConsumo

    namespace = 'app_index:codificadores'

    fields = [
        'tipo',
        'cantidad',
        'activa',
        'fecha',
        'medida',
        'producto',
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

    filterset_class = NormaConsumoFilter

    # Table settings
    table_class = NormaConsumoTable

    inlines = [NormaConsumoDetalleAjaxCRUD]

    inline_tables = [NormaConsumoDetalleTable(NormaconsumoDetalle.objects.all())]

    def get_filter_list_view(self):
        view = super().get_filter_list_view()

        class OFilterListView(view):
            def get_context_data(self, *, object_list=None, **kwargs):
                context = super().get_context_data(**kwargs)
                return_url = reverse_lazy(crud_url_name(NormaConsumoGrouped, 'list', 'app_index:codificadores:'))
                table = NormaConsumoDetalleTable(NormaconsumoDetalle.objects.all())
                context.update({
                    # 'url_importar': 'app_index:importar:dpto_importar',
                    # 'url_exportar': 'app_index:exportar:dpto_exportar',
                    'url_list_normaconsumo': True,
                    'return_url': return_url,
                    'inline_tables': [table]
                })
                return context

            def get_queryset(self):
                queryset = super(OFilterListView, self).get_queryset()
                qfilter = {}
                producto = self.request.GET.get('Producto', None)
                tipo = self.request.GET.get('Tipo', None)
                if producto is not None:
                    p = producto.split(' | ')
                    qfilter.update({
                        'producto__codigo': p[0],
                        'producto__descripcion': p[1]
                         })
                    queryset = queryset.filter(**qfilter)
                if tipo is not None:
                    qfilter.update({
                        'tipo': tipo
                    })
                    queryset = queryset.filter(**qfilter)
                return queryset

        return OFilterListView

    def get_update_view(self):
        view = super().get_update_view()

        class OEditView(view):

            def get_context_data(self, **kwargs):
                ctx = super().get_context_data()
                if 'pk' in self.kwargs:
                    inline_object_list = NormaconsumoDetalle.objects.filter(normaconsumo__id=self.kwargs['pk'])
                else:
                    inline_object_list = NormaconsumoDetalle.objects.all()
                table = self.inlines[0].table_class(inline_object_list)
                self.inlines[0].table = table
                ctx.update({
                    'inline_tables': [table],
                    'table': table,
                    'inline_object_list': inline_object_list,
                    'inline_object': NormaconsumoDetalle,
                    'inline_url_list': reverse_lazy(
                        crud_url_name(NormaconsumoDetalle, 'list', 'app_index:codificadores:')
                    ),
                    "add_button_href": 'app_index:codificadores:obtener_normaconsumodetalle_datos',
                    "add_button_hx_get": reverse_lazy('app_index:codificadores:obtener_normaconsumodetalle_datos'),
                    "add_button_hx_target": '#dialog_form',
                })
                return ctx

        return OEditView


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
        'Cantidad_Normas',
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
                context.update({
                    # 'url_importar': 'app_index:importar:dpto_importar',
                    # 'url_exportar': 'app_index:exportar:dpto_exportar',
                    'url_list_normaconsumo': True,
                    'object2': self.env['normaconsumo'],
                    'return_url': None,
                })
                return context

            def get_queryset(self):
                queryset = super().get_queryset()
                return queryset

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

    views_available = ['list', 'update']
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
    update_form = ProductoFlujoForm

    list_fields = fields

    filter_fields = fields

    views_available = ['list', 'update', 'create', 'delete']
    view_type = ['list', 'update', 'create', 'delete']

    filterset_class = ProductoFlujoFilter

    # Table settings
    paginate_by = 15

    table_class = ProductoFlujoTable

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
                    "hx_target": '#dialog',
                })
                return context

            def get_queryset(self):
                qset = super().get_queryset()
                qset = qset.filter(tipoproducto__in=[ChoiceTiposProd.MATERIAPRIMA, ChoiceTiposProd.SUBPRODUCTO]).exclude(
                    productoflujoclase_producto__clasemateriaprima=ChoiceClasesMatPrima.CAPACLASIFICADA)
                return qset

            def get(self, request, *args, **kwargs):
                myexport = request.GET.get("_export", None)
                if myexport and myexport == 'sisgest':
                    table = self.get_table(**self.get_table_kwargs())
                    datos = table.data.data
                    datos2 = [dat.productoflujoclase_producto.get() if dat.tipoproducto.pk == ChoiceTiposProd.MATERIAPRIMA else None for dat in datos]
                    datos2.remove(None)
                    return crear_export_datos_table(request, "PROD", ProductoFlujo, datos, datos2)
                else:
                    return super().get(request=request)

        return OFilterListView


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
                    # messages.error(self.request, 'No se puede eliminar, está siendo utilizado.')
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
                    'url_importar': 'app_index:importar:ms_importar',
                    'url_exportar': 'app_index:exportar:ms_exportar',
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
        'tiponumeracion',
        'sistema',
        'departamento',
        'tipo_documento',
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


# ------ ConfCentrosElementosOtros / CRUD ------
class ConfCentrosElementosOtrosCRUD(CommonCRUDView):
    model = ConfCentrosElementosOtros

    namespace = 'app_index:codificadores'

    fields = [
        'clave'
    ]

    add_form = ConfCentrosElementosOtrosForm
    update_form = ConfCentrosElementosOtrosForm

    list_fields = fields

    filter_fields = fields

    views_available = ['update', 'list']
    view_type = ['update', 'list']

    # Table settings
    paginate_by = 5
    table_class = ConfCentrosElementosOtrosTable

    def get_filter_list_view(self):
        view = super().get_filter_list_view()

        class OFilterListView(view):

            def get_context_data(self, *, object_list=None, **kwargs):
                context = super().get_context_data(**kwargs)
                context.update({
                    'url_importar': 'app_index:importar:confccelemg_importar',
                    'filter': False,
                    'filtrar': True,
                    'url_exportar': True,
                })
                return context

            def get(self, request, *args, **kwargs):
                myexport = request.GET.get("_export", None)
                if myexport and myexport == 'sisgest':
                    table = self.get_table(**self.get_table_kwargs())
                    datos = table.data.data
                    datos2 = ConfCentrosElementosOtrosDetalle.objects.all()
                    return crear_export_datos_table(request, "ConfCCEleG", ConfCentrosElementosOtros, datos, datos2)
                else:
                    return super().get(request=request)

        return OFilterListView

class ObtenrDatosModalFormView(FormView):
    template_name = 'app_index/modals/modal_form.html'
    form_class = ObtenerDatosModalForm

    def form_valid(self, form):
        if form.is_valid():
            valor_inicial = form.cleaned_data['valor_inicial']
            clase_mat_prima = form.cleaned_data['clase_mat_prima']
            self.success_url = reverse_lazy(
                'app_index:appversat:prod_appversat',
                kwargs={
                    'valor_inicial': valor_inicial,
                    'clase_mat_prima': clase_mat_prima,
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
