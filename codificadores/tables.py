import django_tables2 as tables
from django.template.loader import render_to_string

from codificadores.models import *
from cruds_adminlte3.tables import CommonColumnShiftTableBootstrap4ResponsiveActions, \
    ColumnShiftTableBootstrap4Responsive
from cruds_adminlte3.utils import attrs_center_center
from django.utils.translation import gettext as _


# ------ Departamento / Table ------
class DepartamentoTable(CommonColumnShiftTableBootstrap4ResponsiveActions):
    class Meta(CommonColumnShiftTableBootstrap4ResponsiveActions.Meta):
        model = Departamento

        fields = (
            'codigo',
            'descripcion',
            'centrocosto',
            'unidadcontable',
        )


# ------ NormaConsumo / Table ------
class NormaConsumoTable(CommonColumnShiftTableBootstrap4ResponsiveActions):
    actions = tables.TemplateColumn(
        template_name='cruds/actions/hx_actions_normasconsumo_template.html',
        verbose_name=_('Actions'),
        exclude_from_export=True,
        orderable=False,
        attrs=attrs_center_center
    )

    class Meta(CommonColumnShiftTableBootstrap4ResponsiveActions.Meta):
        model = NormaConsumo

        fields = (
            'fecha',
            # 'tipo',
            'producto',
            'cantidad',
            'medida',
            'confirmada',
            'activa',
        )

    # ------ NormaConsumo / Table ------


class NormaConsumoDetalleTable(CommonColumnShiftTableBootstrap4ResponsiveActions):
    class Meta(CommonColumnShiftTableBootstrap4ResponsiveActions.Meta):
        model = NormaconsumoDetalle

        fields = (
            'norma_ramal',
            'norma_empresarial',
            'operativo',
            # 'normaconsumo',
            'producto',
            'medida'
        )

    hx_target = "#id_normaconsumodetalle_myList"
    hx_swap = "innerHTML"
    # hx_replace_url = "true"

    actions = tables.TemplateColumn(
        template_name='cruds/actions/hx_actions_normaconsumo_detalles_template.html',
        verbose_name=_('Actions'),
        exclude_from_export=True,
        orderable=False,
        attrs=attrs_center_center
    )

    @staticmethod
    def render_operativo(value):
        if value:
            return render_to_string('app_index/table_icons/true_icon.html')
        else:
            return render_to_string('app_index/table_icons/false_icon.html')


# ------ NormaConsumoGrouped / Table ------
class NormaConsumoGroupedTable(CommonColumnShiftTableBootstrap4ResponsiveActions):
    actions = tables.TemplateColumn(
        template_name='cruds/actions/hx_actions_normaconsumogrouped_template.html',
        verbose_name=_('Actions'),
        exclude_from_export=True,
        orderable=False,
        attrs=attrs_center_center
    )

    class Meta(CommonColumnShiftTableBootstrap4ResponsiveActions.Meta):
        model = NormaConsumoGrouped

        fields = (
            'Producto',
            'Tipo',
            'Cantidad_Normas',
        )


# ------ UnidadContable / Table ------
class UnidadContableTable(CommonColumnShiftTableBootstrap4ResponsiveActions):
    class Meta(CommonColumnShiftTableBootstrap4ResponsiveActions.Meta):
        model = UnidadContable

        fields = (
            'codigo',
            'nombre',
            'is_empresa',
            'is_comercializadora',
            'activo',
        )


# ------ Medida / Table ------
class MedidaTable(CommonColumnShiftTableBootstrap4ResponsiveActions):
    class Meta(CommonColumnShiftTableBootstrap4ResponsiveActions.Meta):
        model = Medida

        fields = (
            'clave',
            'descripcion',
            'activa',
        )


# ------ MedidaConversion / Table ------
class MedidaConversionTable(CommonColumnShiftTableBootstrap4ResponsiveActions):
    class Meta(CommonColumnShiftTableBootstrap4ResponsiveActions.Meta):
        model = Medida

        fields = (
            'medidao',
            'medidad',
            'factor_conversion',
        )


# ------ Cuenta / Table ------
class CuentaTable(CommonColumnShiftTableBootstrap4ResponsiveActions):
    # shifter_template = "cruds/django_tables2_column_shifter/my-tree-hx-bootstrap4-responsive.html"

    descripcion = tables.TemplateColumn(template_name='cruds/tables/tree_node.html')
    clave = tables.TemplateColumn(template_name='cruds/tables/tree_node_clave.html')

    class Meta(CommonColumnShiftTableBootstrap4ResponsiveActions.Meta):
        model = Cuenta

        fields = (
            'clave',
            'descripcion',
            'activa',
        )


# ------ CentroCosto / Table ------
class CentroCostoTable(CommonColumnShiftTableBootstrap4ResponsiveActions):
    class Meta(CommonColumnShiftTableBootstrap4ResponsiveActions.Meta):
        model = CentroCosto

        fields = (
            'clave',
            'descripcion',
            'activo',
        )


# ------ ProductoFlujo / Table ------
class ProductoFlujoTable(CommonColumnShiftTableBootstrap4ResponsiveActions):
    get_clasemateriaprima = tables.Column(verbose_name='Clase Materia Prima')

    class Meta(CommonColumnShiftTableBootstrap4ResponsiveActions.Meta):
        model = ProductoFlujo

        fields = (
            'codigo',
            'descripcion',
            'medida',
            'tipoproducto',
            'get_clasemateriaprima',
            'activo',
        )


# ------ ProductoFlujoCuenta / Table ------
class ProductoFlujoCuentaTable(CommonColumnShiftTableBootstrap4ResponsiveActions):
    class Meta(CommonColumnShiftTableBootstrap4ResponsiveActions.Meta):
        model = ProductoFlujoCuenta

        fields = (
            'id',
            'cuenta',
            'producto',
        )


class VitolaTable(CommonColumnShiftTableBootstrap4ResponsiveActions):
    class Meta(CommonColumnShiftTableBootstrap4ResponsiveActions.Meta):
        model = Vitola

        fields = (
            'producto__codigo',
            'producto__descripcion',
            'producto__medida__clave',
            'destino',
            'categoriavitola',
            'tipovitola',
            'diametro',
            'longitud',
            'cepo',
            'producto__activo'
        )


# ------ MarcaSalida / Table ------
class MarcaSalidaTable(CommonColumnShiftTableBootstrap4ResponsiveActions):
    class Meta(CommonColumnShiftTableBootstrap4ResponsiveActions.Meta):
        model = MarcaSalida

        fields = (
            'codigo',
            'descripcion',
            'activa',
        )


# ------ MotivoAjuste / Table ------
class MotivoAjusteTable(CommonColumnShiftTableBootstrap4ResponsiveActions):
    class Meta(CommonColumnShiftTableBootstrap4ResponsiveActions.Meta):
        model = MotivoAjuste

        fields = (
            'descripcion',
            'aumento',
            'activo',
        )


# ------ Cambio Producto / Table ------
class CambioProductoTable(CommonColumnShiftTableBootstrap4ResponsiveActions):
    class Meta(CommonColumnShiftTableBootstrap4ResponsiveActions.Meta):
        model = CambioProducto

        fields = (
            'productoo',
            'productod',
        )


class LineaSalidaTable(CommonColumnShiftTableBootstrap4ResponsiveActions):
    class Meta(CommonColumnShiftTableBootstrap4ResponsiveActions.Meta):
        model = LineaSalida

        fields = (
            'producto__codigo',
            'producto__descripcion',
            'producto__medida__clave',
            'envase',
            'vol_cajam3',
            'peso_bruto',
            'peso_neto',
            'peso_legal',
            'marcasalida',
            'vitola',
            'producto__activo'
        )


# ------ NumeracionDocumentos / Table ------
class NumeracionDocumentosTable(CommonColumnShiftTableBootstrap4ResponsiveActions):
    class Meta(CommonColumnShiftTableBootstrap4ResponsiveActions.Meta):
        model = NumeracionDocumentos

        fields = (
            'id',
            'sistema',
            'departamento',
            'tipo_documento',
            'prefijo'
        )


class ConfCentrosElementosOtrosDetalleTable(CommonColumnShiftTableBootstrap4ResponsiveActions):
    class Meta(CommonColumnShiftTableBootstrap4ResponsiveActions.Meta):
        model = ConfCentrosElementosOtrosDetalle

        fields = (
            'descripcion',
            'valor',
        )


# ------ ProductsCapasClaPesadas / Table ------
class ProductsCapasClaPesadasTable(CommonColumnShiftTableBootstrap4ResponsiveActions):
    class Meta(CommonColumnShiftTableBootstrap4ResponsiveActions.Meta):
        model = ProductsCapasClaPesadas

        fields = (
            'codigo',
            'descripcion',
            'medida',
            'tipoproducto',
            'activo',
        )

    actions = None


class ConfCentrosElementosOtrosDetalleGroupedTable(CommonColumnShiftTableBootstrap4ResponsiveActions):
    actions = tables.TemplateColumn(
        template_name='cruds/actions/hx_actions_confcentroselementos_template.html',
        verbose_name=_('Actions'),
        exclude_from_export=True,
        orderable=False,
        attrs=attrs_center_center
    )

    class Meta(CommonColumnShiftTableBootstrap4ResponsiveActions.Meta):
        model = ConfCentrosElementosOtrosDetalleGrouped

        fields = (
            'Clave',
            'Elementos',
        )


# ------ TipoDocumento / Table ------
class TipoDocumentoTable(CommonColumnShiftTableBootstrap4ResponsiveActions):
    class Meta(CommonColumnShiftTableBootstrap4ResponsiveActions.Meta):
        model = TipoDocumento

        fields = (
            'descripcion',
            'operacion',
            'generado',
            'prefijo',
        )


# ------ ClasificadorCargos / Table ------
class ClasificadorCargosTable(CommonColumnShiftTableBootstrap4ResponsiveActions):
    class Meta(CommonColumnShiftTableBootstrap4ResponsiveActions.Meta):
        model = ClasificadorCargos

        fields = (
            'codigo',
            'descripcion',
            'grupo__grupo',
            'grupo__salario',
            'actividad',
            'vinculo_produccion',
            'activo',
            'unidadcontable',
        )


# ------ FichaCostoFilas / Table ------
class FichaCostoFilasTable(CommonColumnShiftTableBootstrap4ResponsiveActions):
    descripcion = tables.TemplateColumn(template_name='cruds/tables/tree_node_ficha.html')
    fila = tables.TemplateColumn(template_name='cruds/tables/tree_node_fila.html')

    actions = tables.TemplateColumn(
        template_name='cruds/actions/hx_actions_filasfichacosto_template.html',
        verbose_name=_('Actions'),
        exclude_from_export=True,
        orderable=False,
        attrs=attrs_center_center
    )

    class Meta(CommonColumnShiftTableBootstrap4ResponsiveActions.Meta):
        model = FichaCostoFilas

        fields = (
            'fila',
            'descripcion',
            'encabezado',
            'salario',
            'vacaciones',
            'desglosado',
            'calculado',
            'filasasumar',
        )
