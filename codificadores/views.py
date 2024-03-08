from app_index.views import CommonCRUDView
from codificadores.filters import *
from codificadores.forms import *
from codificadores.tables import *


# Create your views here.
# ------ DepartamentoRelacion / Ajax CRUD ------
# class DepartamentoRelacionAjaxCRUD(InlineAjaxCRUD):
#     model = DepartamentoRelacion
#     base_model = Departamento
#     inline_field = 'iddepartamentoo'
#     add_form = DepartamentoRelacionForm
#     update_form = DepartamentoRelacionForm
#     fields = ['iddepartamentod']
#     title = "Relaciones"


# ------ Departamento / CRUD ------
class DepartamentoCRUD(CommonCRUDView):
    model = Departamento

    namespace = 'app_index:codificadores'

    fields = [
        'codigo',
        'descripcion',
        'idcentrocosto',
        'idunidadcontable',
    ]

    # Hay que agregar __icontains luego del nombre del campo para que busque el contenido
    # y no distinga entre mayúsculas y minúsculas.
    # En el caso de campos relacionados hay que agregar __<nombre_campo_que_se_muestra>__icontains
    search_fields = [
        'codigo__contains',
        'descripcion__icontains',
        'idcentrocosto__contains',
        'idunidadcontable__contains',

    ]

    # search_method = hecho_extraordinario_search_queryset

    add_form = DepartamentoForm
    update_form = DepartamentoForm

    list_fields = fields

    filter_fields = fields

    filterset_class = DepartamentoFilter

    # Table settings
    table_class = DepartamentoTable

    # inlines = [DepartamentoRelacionInline]

    form_class = DepartamentoForm


# ------ DepartamentoRelacion / CRUD ------
# class DepartamentoRelacionCRUD(CommonCRUDView):
#     model = DepartamentoRelacion
#
#     namespace = 'app_index:codificadores'
#
#     fields = [
#         'iddepartamentoo',
#         'iddepartamentod',
#     ]
#
#     # Hay que agregar __icontains luego del nombre del campo para que busque el contenido
#     # y no distinga entre mayúsculas y minúsculas.
#     # En el caso de campos relacionados hay que agregar __<nombre_campo_que_se_muestra>__icontains
#     search_fields = [
#         'iddepartamentoo__descripcion__icontains',
#         'iddepartamentod__descripcion__icontains',
#     ]
#
#     # search_method = hecho_extraordinario_search_queryset
#
#     add_form = DepartamentoRelacionForm
#     update_form = DepartamentoRelacionForm
#
#     list_fields = [
#         'iddepartamentoo',
#         'iddepartamentod',
#     ]
#
#     filter_fields = [
#         'iddepartamentoo',
#         'iddepartamentod',
#     ]
#     filterset_class = DepartamentoRelacionFilter
#
#     # Table settings
#     table_class = DepartamentoRelacionTable


# ------ UnidadContable / CRUD ------
class UnidadContableCRUD(CommonCRUDView):
    model = UnidadContable

    namespace = 'app_index:codificadores'

    template_name_base = 'codificadores/unidadcontable/cruds'

    partial_template_name_base = 'codificadores/unidadcontable/partials'

    fields = [
        'codigo',
        'nombre',
        'activo',
        'is_empresa',
        'is_comercializadora',
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

    # search_method = hecho_extraordinario_search_queryset

    add_form = UnidadContableForm
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
    filterset_class = UnidadContableFilter

    # Table settings
    table_class = UnidadContableTable

    # def get_delete_view(self):
    #     view = self.get_delete_view_class()
    #
    #     class ODeleteView(view):
    #
    #         def post(self, request, *args, **kwargs):
    #             self.object = self.get_object()
    #             try:
    #                 self.object.delete()
    #             except ProtectedError:
    #                 messages.error(self.request, 'No se puede eliminar, está siendo utilizado.')
    #                 return HttpResponseRedirect(self.get_success_url())
    #             self.object.delete()
    #             if self.success_message:
    #                 messages.success(self.request, self.success_message)
    #             return HttpResponseRedirect(self.get_success_url())
    #
    #     return ODeleteView


# ------ Medida / CRUD ------
class MedidaCRUD(CommonCRUDView):
    model = Medida

    namespace = 'app_index:codificadores'

    template_name_base = 'codificadores/medida/cruds'

    fields = [
        'clave',
        'descripcion',
    ]

    # Hay que agregar __icontains luego del nombre del campo para que busque el contenido
    # y no distinga entre mayúsculas y minúsculas.
    # En el caso de campos relacionados hay que agregar __<nombre_campo_que_se_muestra>__icontains
    search_fields = [
        'clave__icontains',
        'descripcion__icontains',
    ]

    # search_method = hecho_extraordinario_search_queryset

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
    filterset_class = MedidaFilter

    # Table settings
    table_class = MedidaTable


# ------ MedidaConversion / CRUD ------
class MedidaConversionCRUD(CommonCRUDView):
    model = MedidaConversion

    namespace = 'app_index:codificadores'

    template_name_base = 'codificadores/medidaconversion/cruds'

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

    # search_method = hecho_extraordinario_search_queryset

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

    # search_method = hecho_extraordinario_search_queryset

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
    filterset_class = CuentaFilter

    # Table settings
    table_class = CuentaTable


# ------ CentroCosto / CRUD ------
class CentroCostoCRUD(CommonCRUDView):
    model = CentroCosto

    namespace = 'app_index:codificadores'

    fields = [
        'clave',
        'clavenivel',
        'descripcion',
        'activo',
    ]

    # Hay que agregar __icontains luego del nombre del campo para que busque el contenido
    # y no distinga entre mayúsculas y minúsculas.
    # En el caso de campos relacionados hay que agregar __<nombre_campo_que_se_muestra>__icontains
    search_fields = [
        'clave__icontains',
        'clavenivel__icontains',
        'descripcion__icontains',
        'activo',
    ]

    # search_method = hecho_extraordinario_search_queryset

    add_form = CentroCostoForm
    update_form = CentroCostoForm

    list_fields = [
        'clave',
        'clavenivel',
        'descripcion',
        'activo',
    ]

    filter_fields = [
        'clave',
        'clavenivel',
        'descripcion',
        'activo',
    ]
    filterset_class = CentroCostoFilter

    # Table settings
    table_class = CentroCostoTable


# ------ TipoProducto / CRUD ------
class TipoProductoCRUD(CommonCRUDView):
    model = TipoProducto

    namespace = 'app_index:codificadores'

    fields = [
        'id',
        'descripcion',
    ]

    # Hay que agregar __icontains luego del nombre del campo para que busque el contenido
    # y no distinga entre mayúsculas y minúsculas.
    # En el caso de campos relacionados hay que agregar __<nombre_campo_que_se_muestra>__icontains
    search_fields = [
        'id__contains',
        'descripcion__icontains',
    ]

    # search_method = hecho_extraordinario_search_queryset

    add_form = TipoProductoForm
    update_form = TipoProductoForm

    list_fields = fields

    filter_fields = fields

    filterset_class = TipoProductoFilter

    # Table settings
    table_class = TipoProductoTable


# ------ EstadoProducto / CRUD ------
class EstadoProductoCRUD(TipoProductoCRUD):
    model = EstadoProducto

    add_form = EstadoProductoForm
    update_form = EstadoProductoForm

    filterset_class = EstadoProductoFilter

    # Table settings
    table_class = EstadoProductoTable


# ------ ClaseMateriaPrima / CRUD ------
class ClaseMateriaPrimaCRUD(CommonCRUDView):
    model = ClaseMateriaPrima

    namespace = 'app_index:codificadores'

    fields = [
        'id',
        'descripcion',
        'capote_fortaleza',
    ]

    # Hay que agregar __icontains luego del nombre del campo para que busque el contenido
    # y no distinga entre mayúsculas y minúsculas.
    # En el caso de campos relacionados hay que agregar __<nombre_campo_que_se_muestra>__icontains
    search_fields = [
        'id__contains',
        'descripcion__icontains',
        'capote_fortaleza__icontains',
    ]

    # search_method = hecho_extraordinario_search_queryset

    add_form = ClaseMateriaPrimaForm
    update_form = ClaseMateriaPrimaForm

    list_fields = fields

    filter_fields = fields

    filterset_class = ClaseMateriaPrimaFilter

    # Table settings
    table_class = ClaseMateriaPrimaTable


# ------ ProductoFlujo / CRUD ------
class ProductoFlujoCRUD(CommonCRUDView):
    model = ProductoFlujo

    namespace = 'app_index:codificadores'

    fields = [
        'id',
        'codigo',
        'descripcion',
        'activo',
        'idmedida',
        'idtipoproducto',
    ]

    # Hay que agregar __icontains luego del nombre del campo para que busque el contenido
    # y no distinga entre mayúsculas y minúsculas.
    # En el caso de campos relacionados hay que agregar __<nombre_campo_que_se_muestra>__icontains
    search_fields = [
        'id__contains',
        'codigo__icontains',
        'id__contains',
        'descripcion__icontains',
        'activo',
        'idmedida__descripcion__icontains',
        'idtipoproducto__descripcion__icontains',
    ]

    # search_method = hecho_extraordinario_search_queryset

    add_form = ProductoFlujoForm
    update_form = ProductoFlujoForm

    list_fields = fields

    filter_fields = fields

    filterset_class = ProductoFlujoFilter

    # Table settings
    table_class = ProductoFlujoTable


# ------ ProductoFlujoClase / CRUD ------
class ProductoFlujoClaseCRUD(CommonCRUDView):
    model = ProductoFlujoClase

    namespace = 'app_index:codificadores'

    fields = [
        'id',
        'idclasemateriaprima',
        'idproducto',
    ]

    # Hay que agregar __icontains luego del nombre del campo para que busque el contenido
    # y no distinga entre mayúsculas y minúsculas.
    # En el caso de campos relacionados hay que agregar __<nombre_campo_que_se_muestra>__icontains
    search_fields = [
        'id__contains',
        'idclasemateriaprima__descripcion__icontains',
        'idproducto__descripcion__icontains',
    ]

    # search_method = hecho_extraordinario_search_queryset

    add_form = ProductoFlujoClaseForm
    update_form = ProductoFlujoClaseForm

    list_fields = fields

    filter_fields = fields

    filterset_class = ProductoFlujoClaseFilter

    # Table settings
    table_class = ProductoFlujoClaseTable


# ------ ProductoFlujoDestino / CRUD ------
class ProductoFlujoDestinoCRUD(CommonCRUDView):
    model = ProductoFlujoDestino

    namespace = 'app_index:codificadores'

    fields = [
        'id',
        'destino',
        'idproducto',
    ]

    # Hay que agregar __icontains luego del nombre del campo para que busque el contenido
    # y no distinga entre mayúsculas y minúsculas.
    # En el caso de campos relacionados hay que agregar __<nombre_campo_que_se_muestra>__icontains
    search_fields = [
        'id__contains',
        'destino_icontains',
        'idproducto__descripcion__icontains',
    ]

    # search_method = hecho_extraordinario_search_queryset

    add_form = ProductoFlujoDestinoForm
    update_form = ProductoFlujoDestinoForm

    list_fields = fields

    filter_fields = fields

    filterset_class = ProductoFlujoDestinoFilter

    # Table settings
    table_class = ProductoFlujoDestinoTable


# ------ ProductoFlujoCuenta / CRUD ------
class ProductoFlujoCuentaCRUD(CommonCRUDView):
    model = ProductoFlujoCuenta

    namespace = 'app_index:codificadores'

    fields = [
        'id',
        'idcuenta',
        'idproducto',
    ]

    # Hay que agregar __icontains luego del nombre del campo para que busque el contenido
    # y no distinga entre mayúsculas y minúsculas.
    # En el caso de campos relacionados hay que agregar __<nombre_campo_que_se_muestra>__icontains
    search_fields = [
        'id__contains',
        'idcuenta__descripcion__icontains',
        'idproducto__descripcion__icontains',
    ]

    # search_method = hecho_extraordinario_search_queryset

    add_form = ProductoFlujoCuentaForm
    update_form = ProductoFlujoCuentaForm

    list_fields = fields

    filter_fields = fields

    filterset_class = ProductoFlujoCuentaFilter

    # Table settings
    table_class = ProductoFlujoCuentaTable


# ------ CategoriaVitola / CRUD ------
class CategoriaVitolaCRUD(CommonCRUDView):
    model = CategoriaVitola

    namespace = 'app_index:codificadores'

    fields = [
        'id',
        'descripcion',
        'orden',
    ]

    # Hay que agregar __icontains luego del nombre del campo para que busque el contenido
    # y no distinga entre mayúsculas y minúsculas.
    # En el caso de campos relacionados hay que agregar __<nombre_campo_que_se_muestra>__icontains
    search_fields = [
        'id__contains',
        'descripcion__icontains',
        'orden__contains',
    ]

    # search_method = hecho_extraordinario_search_queryset

    add_form = CategoriaVitolaForm
    update_form = CategoriaVitolaForm

    list_fields = fields

    filter_fields = fields

    filterset_class = CategoriaVitolaFilter

    # Table settings
    table_class = CategoriaVitolaTable


# ------ TipoVitola / CRUD ------
class TipoVitolaCRUD(CommonCRUDView):
    model = TipoVitola

    namespace = 'app_index:codificadores'

    fields = [
        'id',
        'descripcion',
    ]

    # Hay que agregar __icontains luego del nombre del campo para que busque el contenido
    # y no distinga entre mayúsculas y minúsculas.
    # En el caso de campos relacionados hay que agregar __<nombre_campo_que_se_muestra>__icontains
    search_fields = [
        'id__contains',
        'descripcion__icontains',
    ]

    # search_method = hecho_extraordinario_search_queryset

    add_form = TipoVitolaForm
    update_form = TipoVitolaForm

    list_fields = fields

    filter_fields = fields

    filterset_class = TipoVitolaFilter

    # Table settings
    table_class = TipoVitolaTable


# ------ Vitola / CRUD ------
class VitolaCRUD(CommonCRUDView):
    model = Vitola

    namespace = 'app_index:codificadores'

    template_name_base = 'codificadores/vitola/cruds'

    fields = [
        'diametro',
        'longitud',
        'destino',
        'cepo',
        'idcategoriavitola',
        'idproducto',
        'idtipovitola',
    ]

    # Hay que agregar __icontains luego del nombre del campo para que busque el contenido
    # y no distinga entre mayúsculas y minúsculas.
    # En el caso de campos relacionados hay que agregar __<nombre_campo_que_se_muestra>__icontains
    search_fields = [
        'diametro__contains',
        'longitud__contains',
        'destino__icontains',
        'cepo__contains',
        'idcategoriavitola__descripcion__icontains',
        'idproducto__descripcion__icontains',
        'idtipovitola__descripcion__icontains',
    ]

    # search_method = hecho_extraordinario_search_queryset

    add_form = VitolaForm
    update_form = VitolaForm

    list_fields = fields

    filter_fields = fields

    filterset_class = VitolaFilter

    # Table settings
    table_class = VitolaTable


# ------ MarcaSalida / CRUD ------
class MarcaSalidaCRUD(CommonCRUDView):
    model = MarcaSalida

    namespace = 'app_index:codificadores'

    template_name_base = 'codificadores/marcasalida/cruds'

    fields = [
        'codigo',
        'descripcion',
    ]

    # Hay que agregar __icontains luego del nombre del campo para que busque el contenido
    # y no distinga entre mayúsculas y minúsculas.
    # En el caso de campos relacionados hay que agregar __<nombre_campo_que_se_muestra>__icontains
    search_fields = [
        'codigo__icontains',
        'descripcion__icontains',
    ]

    # search_method = hecho_extraordinario_search_queryset

    add_form = MarcaSalidaForm
    update_form = MarcaSalidaForm

    list_fields = fields

    filter_fields = fields

    filterset_class = MarcaSalidaFilter

    # Table settings
    table_class = MarcaSalidaTable
