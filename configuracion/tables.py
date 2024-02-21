from cruds_adminlte3.tables import CommonColumnShiftTableBootstrap4ResponsiveActions
from .models import *


# ------ UEB / Table ------
# class UebTable(CommonColumnShiftTableBootstrap4ResponsiveActions):
#     class Meta(CommonColumnShiftTableBootstrap4ResponsiveActions.Meta):
#         model = Ueb
#
#         fields = (
#             'idunidadcontable',
#         )


# ------ User UEB / Table ------
class UserUebTable(CommonColumnShiftTableBootstrap4ResponsiveActions):
    class Meta(CommonColumnShiftTableBootstrap4ResponsiveActions.Meta):
        model = UserUeb

        fields = (
            'idueb',
            'iduser',
        )
