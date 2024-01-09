from __future__ import unicode_literals

from django.db.models import Sum, Count
from django.views.generic import TemplateView
from django_tables2 import RequestConfig

from cruds_adminlte3.crud import CRUDView, MyTableExport
from cruds_adminlte3.config import CONFIG


class Index(TemplateView):
    template_name = 'he_index/adminlte/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context.update(CONFIG)
        return context


class Underconstruction(TemplateView):
    template_name = 'app_index/adminlte/underconstruction.html'


class Dashboard(TemplateView):
    template_name = 'he_index/adminlte/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        hechos = HechoExtraordinario.objects.all()
        # total de hechos
        hechos_count = HechoExtraordinario.objects.filter(
            fecha_ocurrencia__year=2023
        ).count()
        # total de pérdidas en CUP
        valor_perdido_cup = HechoExtraordinario.objects.filter(
            fecha_ocurrencia__year=2023
        ).aggregate(
            Sum('perdidas_cup')
        )['perdidas_cup__sum']
        # total valor recuperado en CUP
        valor_recuperado_cup = HechoExtraordinario.objects.filter(
            fecha_ocurrencia__year=2023
        ).aggregate(
            Sum('recuperado_cup')
        )['recuperado_cup__sum']
        porciento_recuperado = (valor_recuperado_cup / valor_perdido_cup) * 100
        tipos_he = HechoExtraordinario.objects.filter(
            fecha_ocurrencia__year=2023
        ).values(
            'tipo_hecho__nombre'
        ).order_by(
            'tipo_hecho__nombre'
        ).annotate(
            count=Count('tipo_hecho__nombre'),
            percent=Count('tipo_hecho__nombre') * 100 / hechos_count
        )
        cerradas = HechoExtraordinario.objects.filter(sin_cerrar=0).count()
        cerradas_x100 = cerradas / hechos_count * 100
        sin_cerrar = HechoExtraordinario.objects.filter(sin_cerrar=1).count()
        sin_cerrar_x100 = sin_cerrar / hechos_count * 100
        mas_30_dias = HechoExtraordinario.objects.filter(mas_30_dias=1).count()
        mas_30_dias_x100 = mas_30_dias / hechos_count * 100
        cant_relev = HechoExtraordinario.objects.filter(relevancia=1).count()
        cant_corrup = HechoExtraordinario.objects.filter(relevancia=2).count()
        chart_cuba = chart_cuba_map(request=self.request)
        chart_empresas = chart_empresas_x_provincias(request=self.request)
        context.update(CONFIG)
        context.update(
            {
                'view_type': 'Dashboard',
                'hechos': hechos,
                'hechos_count': hechos_count,
                'valor_perdido_cup': valor_perdido_cup,
                'valor_recuperado_cup': valor_recuperado_cup,
                'porciento_recuperado': '{:,.2f}'.format(porciento_recuperado),
                'tipos_he': tipos_he,
                'cerradas': cerradas,
                'sin_cerrar': sin_cerrar,
                'mas_30_dias': mas_30_dias,
                'cant_relev': cant_relev,
                'cant_corrup': cant_corrup,
                'cerradas_x100': '{:,.2f}'.format(cerradas_x100),
                'sin_cerrar_x100': '{:,.2f}'.format(sin_cerrar_x100),
                'mas_30_dias_x100': '{:,.2f}'.format(mas_30_dias_x100),
                'chart_cuba': chart_cuba,
                'chart_empresas': chart_empresas,
            }
        )
        return context

    def get_template_names(self):
        if self.request.htmx:
            template_name = "he_index/partials/partial_dashboard.html"
        else:
            template_name = "he_index/adminlte/dashboard.html"

        return template_name

class CommonCRUDView(CRUDView):

    def get_filter_list_view(self):
        view = super().get_filter_list_view()

        class OFilterListView(view):
            def get_context_data(self, *, object_list=None, **kwargs):
                context = super().get_context_data(**kwargs)
                col_vis = ",".join(self.col_vis)
                context.update({'col_vis': col_vis})
                return context

            def get_template_names(self):
                if self.request.htmx:
                    template_name = "he_index/partials/list_table_partial.html"
                else:
                    template_name = "he_index/cruds/list_table.html"

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

        return OEditView

    def get_create_view(self):
        view = super().get_create_view()

        class OCreateView(view):

            def get_template_names(self):
                if self.request.htmx:
                    template_name = "cruds/partial_create.html"
                else:
                    template_name = "he_index/cruds/create.html"

                return template_name

        return OCreateView
