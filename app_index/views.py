from __future__ import unicode_literals

from django.db.models import Sum, Count
from django.views.generic import TemplateView
from django_tables2 import RequestConfig

from cruds_adminlte3.crud import CRUDView, MyTableExport
from cruds_adminlte3.config import CONFIG


class Index(TemplateView):
    template_name = 'app_index/adminlte/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context.update(CONFIG)
        return context


class Underconstruction(TemplateView):
    template_name = 'app_index/adminlte/underconstruction.html'


class Dashboard(TemplateView):
    template_name = 'app_index/adminlte/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        return context

    def get_template_names(self):
        if self.request.htmx:
            template_name = "app_index/partials/partial_dashboard.html"
        else:
            template_name = "app_index/adminlte/dashboard.html"

        return template_name


class CommonCRUDView(CRUDView):
    model = None  # Must be filled in descendant classes

    namespace = None  # Must be filled in descendant classes

    template_father = 'app_index/cruds/base.html'

    template_name_base = 'app_index/cruds'

    partial_template_name_base = 'app_index/partials'

    views_available = [
        'create',
        'list',
        'delete',
        'update',
    ]

    fields = None  # Must be filled in descendant classes

    # Hay que agregar __icontains luego del nombre del campo para que busque el contenido
    # y no distinga entre mayúsculas y minúsculas.
    # En el caso de campos relacionados hay que agregar __<nombre_campo_que_se_muestra>__icontains
    search_fields = None  # Must be filled in descendant classes

    # search_method = hecho_extraordinario_search_queryset

    add_form = None  # Must be filled in descendant classes

    update_form = None  # Must be filled in descendant classes

    check_login = True
    check_perms = True

    list_fields = None  # Must be filled in descendant classes

    filter_fields = None  # Must be filled in descendant classes

    filterset_class = None  # Must be filled in descendant classes

    page_length = 10

    page_length_menu = [5, 10, 15, 20]

    # Table settings
    table_class = None  # Must be filled in descendant classes
    template_name = "app_index/cruds/list_table.html"
    paginate_by = 10
    exclude_columns = ("actions",)

    def get_filter_list_view(self):
        view = super().get_filter_list_view()

        class OFilterListView(view):
            def get_context_data(self, *, object_list=None, **kwargs):
                context = super().get_context_data(**kwargs)
                col_vis = ",".join(self.col_vis)
                context.update({'col_vis': col_vis})
                return context

            def get_template_names(self):
                if self.table_class is None:
                    template = 'list.html'
                    template_partial = 'list_partial.html'
                else:
                    template = 'list_table.html'
                    template_partial = 'list_table_partial.html'
                if self.request.htmx:
                    template_name = "%s/%s" % (
                        self.partial_template_name_base, template_partial
                    )
                else:
                    template_name = "%s/%s" % (
                        self.template_name_base, template
                    )

                return template_name

            def get(self, request, *args, **kwargs):
                table = self.get_table(**self.get_table_kwargs())
                table_columns = table.columns.columns
                col = request.GET.get("vis", None)
                visibility = request.GET.get("set_visibility_value", None)
                if col is not None and visibility is None and col not in self.col_vis:
                    self.col_vis.append(col)
                if col is not None and visibility == 'on' and col in self.col_vis:
                    self.col_vis.remove(col)
                self.table_class.col_vis = self.col_vis
                self.table_class.getparams = self.getparams
                RequestConfig(request).configure(table)
                export_format = request.GET.get("_export", None)
                if MyTableExport.is_valid_format(export_format):
                    footer = []
                    for column in table.columns.columns:
                        if (column not in self.col_vis) and (not table.base_columns[column].exclude_from_export):
                            footer.append(table_columns[column].footer)
                    exporter = MyTableExport(
                        export_format,
                        table,
                        exclude_columns=self.request.GET.get('excluded_columns').split(','),
                        dataset_kwargs={'footer': footer}
                    )
                    return exporter.response(f"table.{export_format}")
                else:
                    return super().get(request=request)

        return OFilterListView

    def get_update_view(self):
        view = super().get_update_view()

        class OEditView(view):

            def get_template_names(self):
                if self.request.htmx:
                    template_name = "cruds/partial_update.html"
                else:
                    template_name = "cruds/update.html"

                return template_name

            def get_form_kwargs(self):
                form_kwargs = super().get_form_kwargs()
                form_kwargs.update(
                    {
                        "user": self.request.user,
                        "post": self.request.POST,
                    }
                )
                return form_kwargs

        return OEditView

    def get_create_view(self):
        view = super().get_create_view()

        class OCreateView(view):

            def get_template_names(self):
                if self.request.htmx:
                    template_name = "cruds/partial_create.html"
                else:
                    template_name = "app_index/cruds/create.html"

                return template_name

            def get_form_kwargs(self):
                form_kwargs = super().get_form_kwargs()
                form_kwargs.update(
                    {
                        "user": self.request.user,
                    }
                )
                return form_kwargs

        return OCreateView


class Noauthorized(TemplateView):
    template_name = 'app_index/cruds/403.html'
