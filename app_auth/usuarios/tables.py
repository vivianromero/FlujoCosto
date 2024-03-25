import django_tables2 as tables
from django.utils.translation import gettext_lazy as _
# from django.contrib.auth.models import User

from cruds_adminlte3.tables import ColumnShiftTableBootstrap4Responsive
from cruds_adminlte3.utils import attrs_center_center
from configuracion.models import UserUeb
from .forms_usuario_permissions import User_Permissions


class UserTable(ColumnShiftTableBootstrap4Responsive):
    shifter_template = "cruds/django_tables2_column_shifter/my-hx-bootstrap4-responsive.html"
    button_above_table = False

    nav_link = True

    button_shift_class_container = "shift-container"

    col_vis = []  # lista usada para gestionar el visionado de columnas de la tabla

    getparams = None

    actions = tables.TemplateColumn(
        template_name='cruds/actions/hx_actions_template.html',
        verbose_name=_('Actions'),
        exclude_from_export=True,
        orderable=False,
        attrs=attrs_center_center
    )

    class Meta:

        attrs = {
            "class": 'table display table-sm table-bordered table-striped table-hover',
            "style": 'line-height: 1;',
            "td": {
                "class": "align-middle",
                "style": 'padding: 0px;',
            },
        }
        model = UserUeb

        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
            'groups',
            'last_login',
            'is_active',
        )
        template_name = "django_tables2/bootstrap4.html"
        table_pagination = {
            "per_page": 10
        }

    def before_render(self, request):
        """
        Método para gestionar el visionado de columnas.
        Si la columna aparece en la lista 'col_vis' entonces se ocultará dicha columna
        """
        if request.htmx:
            for col in self.col_vis:
                self.columns.hide(col)

# class UserPermissionsTable(ColumnShiftTableBootstrap4Responsive):
#     shifter_template = "cruds/django_tables2_column_shifter/my-hx-bootstrap4-responsive.html"
#
#     button_above_table = False
#
#     nav_link = True
#
#     button_shift_class_container = "shift-container"
#
#     col_vis = []  # lista usada para gestionar el visionado de columnas de la tabla
#
#     getparams = None
#
#     actions = tables.TemplateColumn(
#         template_name='cruds/actions/actions_template.html',
#         verbose_name=_('Actions'),
#         exclude_from_export=True,
#         orderable=False,
#         attrs=attrs_center_center
#     )
#
#     class Meta:
#         attrs = {
#             "class": 'table display table-sm table-bordered table-striped table-hover',
#             "style": 'line-height: 1;',
#             "td": {
#                 "class": "align-middle",
#                 "style": 'padding: 0px;',
#             },
#         }
#         model = User_Permissions
#
#         fields = (
#             'user',
#             'permission',
#         )
#         template_name = "django_tables2/bootstrap4.html"
#         table_pagination = {
#             "per_page": 10
#         }
#
#     def before_render(self, request):
#         """
#         Método para gestionar el visionado de columnas.
#         Si la columna aparece en la lista 'col_vis' entonces se ocultará dicha columna
#         """
#         if request.htmx:
#             for col in self.col_vis:
#                 self.columns.hide(col)
