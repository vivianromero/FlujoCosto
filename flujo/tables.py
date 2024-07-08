from crispy_forms.layout import HTML
from django.template.loader import get_template, render_to_string
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from cruds_adminlte3.tables import CommonColumnShiftTableBootstrap4ResponsiveActions
from cruds_adminlte3.utils import attrs_center_center
from flujo.models import *
from app_versat.inventario import InvDocumento, InvDocumentogasto
from codificadores.models import CentroCosto
import django_tables2 as tables
from django.utils.translation import gettext as _


# ------ Documento / Table ------
class DocumentoTable(CommonColumnShiftTableBootstrap4ResponsiveActions):
    class Meta(CommonColumnShiftTableBootstrap4ResponsiveActions.Meta):
        model = Documento

        fields = (
            'numeroconsecutivo',
            'tipodocumento',
            'numerocontrol',
            'estado',
            'fecha',
            'tipodocumento__operacion',
            # 'departamento',
            # 'ueb',
        )

    actions = tables.TemplateColumn(
        template_name='cruds/actions/hx_actions_documentos_template.html',
        verbose_name=_('Actions'),
        exclude_from_export=True,
        orderable=False,
        attrs=attrs_center_center
    )

    @staticmethod
    def render_estado(value):
        if value == 'Edición':
            return render_to_string('app_index/table_icons/edicion_icon.html')
        elif value == 'Confirmado':
            return render_to_string('app_index/table_icons/confirmado_icon.html')
        elif value == 'Rechazado':
            return render_to_string('app_index/table_icons/rechazado_icon.html')
        elif value == 'Cancelado':
            return render_to_string('app_index/table_icons/cancelado_icon.html')

    @staticmethod
    def value_estado(value):
        return value


# ------ DocumentoDetalle / Table ------
class DocumentoDetalleTable(CommonColumnShiftTableBootstrap4ResponsiveActions):
    class Meta(CommonColumnShiftTableBootstrap4ResponsiveActions.Meta):
        model = DocumentoDetalle

        fields = (
            'producto',
            'estado',
            'cantidad',
            'precio',
            'importe',
            'existencia',
        )


# ------ Documentos Versat / Table ------
class DocumentosVersatTable(CommonColumnShiftTableBootstrap4ResponsiveActions):
    iddocumento = tables.Column(verbose_name='Id',
                                visible=False)
    iddocumento_numero = tables.Column(verbose_name='Número')
    iddocumento_numctrl = tables.Column(verbose_name='Número Ctrl')
    iddocumento_fecha = tables.Column(verbose_name='Fecha')
    iddocumento_concepto = tables.Column(verbose_name='Concepto')
    iddocumento_almacen = tables.Column(verbose_name='Almacén')
    iddocumento_sumaimporte = tables.Column(verbose_name='Importe')
    iddocumento_detalle = tables.JSONColumn(verbose_name='Detalles', visible=False)

    actions = tables.TemplateColumn(
        template_name='cruds/actions/hx_actions_documentosversat_template.html',
        verbose_name=_('Actions'),
        exclude_from_export=True,
        orderable=False,
        attrs={"th": {'style': 'text-align: center;'},
               "td": {'style': 'text-align: center;'},
               }
    )

    class Meta(CommonColumnShiftTableBootstrap4ResponsiveActions.Meta):
        attrs = {
            "class": 'table display table-sm table-bordered table-striped table-hover',
            "style": 'line-height: 1;',
            "td": {
                "class": "align-middle",
                "style": 'padding: 0px;',
            },
            'th': {
                "style": 'position: sticky; top: 0;'
            }
        }
        sequence = (
            'iddocumento',
            'iddocumento_numero',
            'iddocumento_numctrl',
            'iddocumento_fecha',
            'iddocumento_concepto',
            'iddocumento_almacen',
            'iddocumento_sumaimporte',
            'iddocumento_detalle',
            'actions',
        )


# ------ Documentos Versat / Table ------
class DocumentosVersatDetalleTable(CommonColumnShiftTableBootstrap4ResponsiveActions):
    idmovimiento = tables.Column(verbose_name='Id Movimiento', orderable=False, visible=False)
    iddocumento = tables.Column(verbose_name='Id Documento', orderable=False, visible=False)
    idproducto = tables.Column(verbose_name='Id Producto', orderable=False, visible=False)
    producto_codigo = tables.Column(verbose_name='Código')
    producto_descripcion = tables.Column(verbose_name='Descripción')
    idmedida = tables.Column(verbose_name='Id Medida', orderable=False, visible=False)
    medida_clave = tables.Column(verbose_name='Clave Medida', orderable=False, visible=False)
    medida_descripcion = tables.Column(verbose_name='Medida')
    cantidad = tables.Column(verbose_name='Cantidad')
    precio = tables.Column(verbose_name='Precio')
    importe = tables.Column(verbose_name='Importe')

    actions = tables.TemplateColumn(
        template_name='cruds/actions/hx_actions_documentosversat_detalle_template.html',
        verbose_name=_('Actions'),
        exclude_from_export=True,
        orderable=False,
        attrs={"th": {'style': 'text-align: center;'},
               "td": {'style': 'text-align: center;'},
               }
    )

    class Meta(CommonColumnShiftTableBootstrap4ResponsiveActions.Meta):
        attrs = {
            "class": 'table display table-sm table-bordered table-striped table-hover',
            "style": 'line-height: 1;',
            "td": {
                "class": "align-middle",
                "style": 'padding: 0px;',
            },
            'th': {
                "style": 'position: sticky; top: 0;'
            }
        }
        sequence = (
            'idmovimiento',
            'iddocumento',
            'idproducto',
            'producto_codigo',
            'producto_descripcion',
            'idmedida',
            'medida_clave',
            'medida_descripcion',
            'cantidad',
            'precio',
            'importe',
            'actions',
        )
