from cruds_adminlte3.tables import CommonColumnShiftTableBootstrap4ResponsiveActions
from cruds_adminlte3.utils import attrs_center_center
from flujo.models import Documento
from app_versat.inventario import InvDocumento, InvDocumentogasto
from codificadores.models import CentroCosto
import django_tables2 as tables
from django.utils.translation import gettext as _


# ------ Documento / Table ------
class DocumentoTable(CommonColumnShiftTableBootstrap4ResponsiveActions):
    class Meta(CommonColumnShiftTableBootstrap4ResponsiveActions.Meta):
        model = Documento

        fields = (
            'fecha',
            # 'numerocontrol',
            'numeroconsecutivo',
            # 'suma_importe',
            # 'observaciones',
            'estado',
            # 'reproceso',
            # 'editar_nc',
            # 'comprob',
            'departamento',
            'tipodocumento',
            'ueb',
        )

    actions = tables.TemplateColumn(
        template_name='cruds/actions/hx_actions_documentos_template.html',
        verbose_name=_('Actions'),
        exclude_from_export=True,
        orderable=False,
        attrs=attrs_center_center
    )


# ------ Documentos Versat / Table ------
class DocumentosVersatTable(CommonColumnShiftTableBootstrap4ResponsiveActions):
    iddocumento = tables.Column(verbose_name='Id',
                                visible=True,
                                orderable=True)
    iddocumento_fecha = tables.Column(verbose_name='Fecha')
    iddocumento_numero = tables.Column(verbose_name='Número')
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
            'iddocumento_fecha',
            'iddocumento_numero',
            'iddocumento_sumaimporte',
            'iddocumento_detalle',
            'actions',
        )
