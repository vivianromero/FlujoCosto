from app_index.views import CommonCRUDView
from codificadores.filters import *
from codificadores.forms import *
from codificadores.tables import *


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


# ------ UnidadContable / CRUD ------
class UnidadContableCRUD(CommonCRUDView):
    model = UnidadContable

    namespace = 'app_index:codificadores'

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
        'id',
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
        'id__contains',
        'codigo__icontains',
        'id__contains',
        'descripcion__icontains',
        'activo',
        'medida__descripcion__icontains',
        'tipoproducto__descripcion__icontains',
    ]

    add_form = ProductoFlujoForm
    update_form = ProductoFlujoForm

    list_fields = fields

    filter_fields = fields

    filterset_class = ProductoFlujoFilter

    # Table settings
    table_class = ProductoFlujoTable

    def get_filter_list_view(self):
        view = super().get_filter_list_view()

        class OFilterListView(view):
            def get_context_data(self, *, object_list=None, **kwargs):
                context = super().get_context_data(**kwargs)
                # context.update({
                #     'url_apiversat': '',
                #     'url_importar': '',
                #     'url_exportar': '',
                # })
                # return context

        return OFilterListView


# ------ ProductoFlujoClase / CRUD ------
class ProductoFlujoClaseCRUD(CommonCRUDView):
    model = ProductoFlujoClase

    namespace = 'app_index:codificadores'

    fields = [
        'id',
        'clasemateriaprima',
        'producto',
    ]

    # Hay que agregar __icontains luego del nombre del campo para que busque el contenido
    # y no distinga entre mayúsculas y minúsculas.
    # En el caso de campos relacionados hay que agregar __<nombre_campo_que_se_muestra>__icontains
    search_fields = [
        'id__contains',
        'clasemateriaprima__descripcion__icontains',
        'producto__descripcion__icontains',
    ]

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
        'producto',
    ]

    # Hay que agregar __icontains luego del nombre del campo para que busque el contenido
    # y no distinga entre mayúsculas y minúsculas.
    # En el caso de campos relacionados hay que agregar __<nombre_campo_que_se_muestra>__icontains
    search_fields = [
        'id__contains',
        'destino_icontains',
        'producto__descripcion__icontains',
    ]

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
        'diametro',
        'longitud',
        'destino',
        'cepo',
        'categoriavitola',
        'producto',
        'tipovitola',
    ]

    # Hay que agregar __icontains luego del nombre del campo para que busque el contenido
    # y no distinga entre mayúsculas y minúsculas.
    # En el caso de campos relacionados hay que agregar __<nombre_campo_que_se_muestra>__icontains
    search_fields = [
        'diametro__contains',
        'longitud__contains',
        'destino__icontains',
        'cepo__contains',
        'categoriavitola__descripcion__icontains',
        'producto__descripcion__icontains',
        'tipovitola__descripcion__icontains',
    ]

    add_form = VitolaForm
    update_form = VitolaForm

    list_fields = fields

    filter_fields = fields

    filterset_class = VitolaFilter

    # Table settings
    table_class = VitolaTable

    def get_filter_list_view(self):
        view = super().get_filter_list_view()

        class OFilterListView(view):
            def get_context_data(self, *, object_list=None, **kwargs):
                context = super().get_context_data(**kwargs)
                # context.update({
                #     'url_apiversat': '',
                #     'url_importar': '',
                #     'url_exportar': '',
                # })
                return context

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

    views_available = ['list', 'update']
    view_type = ['list', 'update']

    filterset_class = MarcaSalidaFilter

    # Table settings
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

    views_available = ['list', 'update']
    view_type = ['list', 'update']

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
