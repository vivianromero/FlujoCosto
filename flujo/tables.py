from cruds_adminlte3.tables import CommonColumnShiftTableBootstrap4ResponsiveActions
from flujo.models import *


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
