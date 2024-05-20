from cruds_adminlte3.tables import CommonColumnShiftTableBootstrap4ResponsiveActions
from flujo.models import Documento
from app_versat.inventario import InvDocumento, InvDocumentogasto
from codificadores.models import CentroCosto
import django_tables2 as tables



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

# ------ Documentos Versat / Table ------
class DocumentosVersatTable(tables.Table):
    iddocumento = tables.Column(verbose_name='Id',
        visible=True,
        orderable=True)
    iddocumento_fecha = tables.Column(verbose_name='Fecha')
    iddocumento_numero = tables.Column(verbose_name='Número')
    iddocumento_sumaimporte = tables.Column(verbose_name='Importe')
