import django_tables2 as tables
from django.utils.translation import gettext as _
from django.contrib.auth.models import User

from codificadores.models import *
from cruds_adminlte3.tables import CommonColumnShiftTableBootstrap4ResponsiveActions


# ------ Departamento / Table ------
class DepartamentoTable(CommonColumnShiftTableBootstrap4ResponsiveActions):
    class Meta(CommonColumnShiftTableBootstrap4ResponsiveActions.Meta):
        model = Departamento

        fields = (
            'codigo',
            'descripcion',
            'idcentrocosto',
            'idunidadcontable',
        )


# ------ DepartamentoRelacion / Table ------
# class DepartamentoRelacionTable(CommonColumnShiftTableBootstrap4ResponsiveActions):
#     class Meta(CommonColumnShiftTableBootstrap4ResponsiveActions.Meta):
#         model = DepartamentoRelacion
#
#         fields = (
#             'iddepartamentoo',
#             'iddepartamentod',
#         )


# ------ UnidadContable / Table ------
class UnidadContableTable(CommonColumnShiftTableBootstrap4ResponsiveActions):
    class Meta(CommonColumnShiftTableBootstrap4ResponsiveActions.Meta):
        model = UnidadContable

        fields = (
            'codigo',
            'nombre',
            'activo',
            'is_empresa',
            'is_comercializadora',
        )


# ------ Medida / Table ------
class MedidaTable(CommonColumnShiftTableBootstrap4ResponsiveActions):
    class Meta(CommonColumnShiftTableBootstrap4ResponsiveActions.Meta):
        model = Medida

        fields = (
            'clave',
            'descripcion',
        )


# ------ MedidaConversion / Table ------
class MedidaConversionTable(CommonColumnShiftTableBootstrap4ResponsiveActions):
    class Meta(CommonColumnShiftTableBootstrap4ResponsiveActions.Meta):
        model = Medida

        fields = (
            'factor_conversion',
            'medidao',
            'medidad',
        )


# ------ Cuenta / Table ------
class CuentaTable(CommonColumnShiftTableBootstrap4ResponsiveActions):
    descripcion = tables.TemplateColumn(template_name='cruds/tables/tree_node.html')

    class Meta(CommonColumnShiftTableBootstrap4ResponsiveActions.Meta):
        model = Cuenta

        fields = (
            # 'long_niv',
            # 'posicion',
            'clave',
            'descripcion',
            # 'activa',
            # 'parent',
        )


# ------ CentroCosto / Table ------
class CentroCostoTable(CommonColumnShiftTableBootstrap4ResponsiveActions):
    class Meta(CommonColumnShiftTableBootstrap4ResponsiveActions.Meta):
        model = CentroCosto

        fields = (
            'clave',
            'clavenivel',
            'descripcion',
            'activo',
        )


# ------ TipoProducto / Table ------
class TipoProductoTable(CommonColumnShiftTableBootstrap4ResponsiveActions):
    class Meta(CommonColumnShiftTableBootstrap4ResponsiveActions.Meta):
        model = TipoProducto

        fields = (
            'id',
            'descripcion',
        )


# ------ EstadoProducto / Table ------
class EstadoProductoTable(TipoProductoTable):
    class Meta(TipoProductoTable.Meta):
        model = EstadoProducto


# ------ ClaseMateriaPrima / Table ------
class ClaseMateriaPrimaTable(CommonColumnShiftTableBootstrap4ResponsiveActions):
    class Meta(CommonColumnShiftTableBootstrap4ResponsiveActions.Meta):
        model = ClaseMateriaPrima

        fields = (
            'id',
            'descripcion',
            'capote_fortaleza',
        )


# ------ ProductoFlujo / Table ------
class ProductoFlujoTable(CommonColumnShiftTableBootstrap4ResponsiveActions):
    class Meta(CommonColumnShiftTableBootstrap4ResponsiveActions.Meta):
        model = ProductoFlujo

        fields = (
            'id',
            'codigo',
            'descripcion',
            'activo',
            'idmedida',
            'idtipoproducto',
        )


# ------ ProductoFlujoClase / Table ------
class ProductoFlujoClaseTable(CommonColumnShiftTableBootstrap4ResponsiveActions):
    class Meta(CommonColumnShiftTableBootstrap4ResponsiveActions.Meta):
        model = ProductoFlujoClase

        fields = (
            'id',
            'idclasemateriaprima',
            'idproducto',
        )


# ------ ProductoFlujoDestino / Table ------
class ProductoFlujoDestinoTable(CommonColumnShiftTableBootstrap4ResponsiveActions):
    class Meta(CommonColumnShiftTableBootstrap4ResponsiveActions.Meta):
        model = ProductoFlujoDestino

        fields = (
            'id',
            'destino',
            'idproducto',
        )


# ------ ProductoFlujoCuenta / Table ------
class ProductoFlujoCuentaTable(CommonColumnShiftTableBootstrap4ResponsiveActions):
    class Meta(CommonColumnShiftTableBootstrap4ResponsiveActions.Meta):
        model = ProductoFlujoCuenta

        fields = (
            'id',
            'idcuenta',
            'idproducto',
        )


# ------ CategoriaVitola / Table ------
class CategoriaVitolaTable(CommonColumnShiftTableBootstrap4ResponsiveActions):
    class Meta(CommonColumnShiftTableBootstrap4ResponsiveActions.Meta):
        model = CategoriaVitola

        fields = (
            'id',
            'descripcion',
            'orden',
        )


# ------ TipoVitola / Table ------
class TipoVitolaTable(CommonColumnShiftTableBootstrap4ResponsiveActions):
    class Meta(CommonColumnShiftTableBootstrap4ResponsiveActions.Meta):
        model = TipoVitola

        fields = (
            'id',
            'descripcion',
        )
