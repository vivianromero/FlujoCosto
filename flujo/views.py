import datetime
from datetime import datetime

from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django_htmx.http import HttpResponseLocation

from app_apiversat.functionapi import getAPI
from app_index.views import CommonCRUDView
from codificadores.models import Departamento
from cruds_adminlte3.inline_crud import InlineAjaxCRUD
from cruds_adminlte3.utils import crud_url_name
from flujo.filters import DocumentoFilter
from flujo.forms import DocumentoForm
from flujo.models import Documento
from flujo.tables import DocumentoTable, DocumentosVersatTable
from utiles.utils import message_error
from django.utils.translation import gettext_lazy as _
from django.shortcuts import redirect
from cruds_adminlte3.utils import crud_url_name
from django.db import connections
from django.conf import settings
import sweetify
import datetime
from .forms import *
from .models import DocumentoOrigenVersat, DocumentoVersatRechazado
from app_apiversat.functionapi import getAPI

from .forms import DepartamentoDocumentosForm
from .models import *
from .utils import ids_documentos_versat_procesados


# Create your views here.

# ------ DocumentoDetalle / AjaxCRUD ------
class DocumentoDetalleAjaxCRUD(InlineAjaxCRUD):
    model = DocumentoDetalle
    base_model = Documento
    namespace = 'app_index:flujo'
    inline_field = 'documento'
    add_form = DocumentoDetalleForm
    update_form = DocumentoDetalleForm
    list_fields = [
        'producto',
        'cantidad',
        'precio',
        'importe',
        'existencia',
        # 'documento',
        'estado',
    ]

    views_available = [
        'list',
        'list_detail',
        'create',
        'update',
        'delete',
        'detail',
    ]

    title = "Detalles del Documento"


# ------ Documento / CRUD ------
class DocumentoCRUD(CommonCRUDView):
    model = Documento

    template_name_base = 'app_index/flujo'

    partial_template_name_base = 'app_index/flujo/partials'

    namespace = 'app_index:flujo'

    fields = [
        'fecha',
        'numerocontrol',
        'numeroconsecutivo',
        'suma_importe',
        'observaciones',
        'estado',
        'reproceso',
        'editar_nc',
        'comprob',
        'departamento',
        'tipodocumento',
        'ueb',
    ]

    add_form = DocumentoForm
    update_form = DocumentoForm

    list_fields = fields

    filter_fields = fields

    views_available = ['list', 'update', 'create']
    view_type = ['list', 'update', 'create']

    filterset_class = DocumentoFilter

    # Table settings
    paginate_by = 5
    table_class = DocumentoTable

    inlines = [DocumentoDetalleAjaxCRUD]

    def get_create_view(self):
        view = super().get_create_view()

        class OCreateView(view):

            def get_form_kwargs(self):
                form_kwargs = super().get_form_kwargs()
                departamento = self.request.GET.get('departamento', None)
                if departamento is None and 'departamento' in self.request.htmx.current_url_abs_path:
                    deps = [i for i in self.request.htmx.current_url_abs_path.split('?')[1].split('&') if i != '']
                    departamento = next((x for x in deps if 'departamento' in x), [None]).split('=')[1]
                tipo_doc = self.request.GET.get('tipo_doc', None)
                form_kwargs.update(
                    {
                        "user": self.request.user,
                        "departamento": departamento,
                        "tipo_doc": tipo_doc,
                    }
                )
                return form_kwargs

            def get_context_data(self, **kwargs):
                ctx = super().get_context_data(**kwargs)
                dep = self.request.GET.get('departamento', None)
                tipo_doc = self.request.GET.get('tipo_doc', None)
                departamento = Departamento.objects.get(pk=dep)
                tipodocumento = TipoDocumento.objects.get(pk=tipo_doc)
                title = 'Departamento: %s | Documento: %s' % (departamento, tipodocumento)
                ctx.update({
                    'modal_form_title': title,
                    "hx_target": '#table_content_documento_swap',
                    'max_width': '1250px',
                })
                return ctx

            def get_success_url(self):
                if "inline" in self.request.POST:
                    # url = reverse_lazy(crud_url_name(self.model, 'update'), kwargs={"pk": self.object.id})
                    url = self.model.get_absolute_url(self.object)
                    # return HttpResponseLocation(url, target='#dialog',)
                else:
                    url = super().get_success_url()
                return url

            # def form_valid(self, form):
            #     if "inline" in self.request.POST:
            #         url = self.model.get_absolute_url(form.instance)
            #         # return HttpResponseLocation(url, target='#dialog', )
            #         ctx = self.get_context_data()
            #         ctx['form'] = form
            #         ctx['hx_target'] = '#dialog'
            #         self.object = form.save(commit=False)
            #         self.object.save()
            #         tpl = 'app_index/flujo/partials/partial_update.html'
            #         response = render(self.request, tpl, ctx)
            #         response['HX-Retarget'] = ctx['hx_retarget']
            #         response['HX-Reswap'] = ctx['hx_reswap']
            #         return response
            #     else:
            #         return super().form_valid(form)

        return OCreateView

    def get_filter_list_view(self):
        view = super().get_filter_list_view()

        class OFilterListView(view):
            def get_context_data(self, *, object_list=None, **kwargs):
                context = super().get_context_data(**kwargs)
                dep_queryset = context['form'].fields['departamento'].queryset
                dep_queryset = dep_queryset.filter(unidadcontable=self.request.user.ueb)
                context['form'].fields['departamento'].queryset = dep_queryset
                tipo_doc_entrada = TipoDocumento.objects.filter(operacion='E')
                tipo_doc_salida = TipoDocumento.objects.filter(operacion='S')

                tableversat = None
                if self.dep:
                    dpto = self.request.GET.get('departamento', None)
                    datostableversat = dame_documentos_versat(self.request, dpto if dpto else self.dep)
                    tableversat = DocumentosVersatTable(datostableversat)

                context.update({
                    'filter': False,
                    'select_period': True,
                    'period_form': DepartamentoDocumentosForm(initial={'departamento': self.dep}),
                    'url_docversat': reverse_lazy(
                        crud_url_name(Documento, 'list', 'app_index:flujo:')) if self.dep else None,
                    'tableversat': tableversat if tableversat else None,
                    "hx_get": reverse_lazy(crud_url_name(Documento, 'list', 'app_index:flujo:')),
                    "hx_target": '#table_content_documento_swap',
                    "col_vis_hx_include": "[name='departamento'], [name='rango_fecha']",
                    'create_link_menu': True,
                    'tipo_doc_entrada': tipo_doc_entrada,
                    'tipo_doc_salida': tipo_doc_salida,
                })
                return context

            def get_queryset(self):
                qdict = {}
                queryset = super(OFilterListView, self).get_queryset()
                formating = '%d/%m/%Y'
                self.dep = self.request.GET.get('departamento', None)
                rango_fecha = self.request.GET.get('rango_fecha', None)
                # if self.request.htmx and self.request.htmx.current_url_abs_path.split('?').__len__() > 1:
                #     depx = [i for i in self.request.htmx.current_url_abs_path.split('?')[1].split('&') if i != '']
                # else:
                #     depx = []
                if self.dep is not None and self.dep != '':
                    qdict['departamento'] = self.dep
                    # queryset = queryset.filter(departamento=self.dep)
                if self.dep == '' or self.dep is None:
                    # queryset = queryset.none()
                    return self.model.objects.none()
                if rango_fecha is not None and rango_fecha != '':
                    fechas = rango_fecha.strip().split('-')
                    qdict['fecha__gte'] = datetime.datetime.strptime(fechas[0].strip(), formating).date()
                    qdict['fecha__lte'] = datetime.datetime.strptime(fechas[1].strip(), formating).date()
                    # queryset = queryset.filter(
                    #     fecha__gte=datetime.datetime.strptime(fechas[0].strip(), formating).date(),
                    #     fecha__lte=datetime.datetime.strptime(fechas[1].strip(), formating).date()
                    # )
                # if len(depx) > 0:
                #     depxs = depx[0].split('=')
                #     if self.dep is None:
                #         if depxs[0] == 'departamento':
                #             queryset = queryset.filter(departamento=depxs[1])
                #             self.dep = depxs[1]
                #     elif fecha is None:
                #         if depxs[0] == 'fecha':
                #             fechas = depxs[1].strip().split('-')
                #             fechas[0] = fechas[0].replace('%20', '').replace('%2F', '/')
                #             fechas[1] = fechas[1].replace('%20', '').replace('%2F', '/')
                #             queryset = queryset.filter(
                #                 fecha__gte=datetime.datetime.strptime(fechas[0].strip(), formating).date(),
                #                 fecha__lte=datetime.datetime.strptime(fechas[1].strip(), formating).date()
                #             )
                # else:
                #     queryset = queryset.none()
                # if qdict:
                #     return queryset.filter(**qdict)
                return queryset

        return OFilterListView

    def get_update_view(self):
        view = super().get_update_view()

        class OEditView(view):

            def get_context_data(self, **kwargs):
                ctx = super(OEditView, self).get_context_data(**kwargs)
                title = 'Departamento: %s | Documento: %s' % (self.object.departamento, self.object.tipodocumento)
                ctx.update({
                    'modal_form_title': title,
                    'max_width': '1250px',
                    'hx_target': '#table_content_documento_swap',
                })
                return ctx

        return OEditView

    def get_delete_view(self):
        view = super().get_delete_view()

        class ODeleteView(view):

            def get_context_data(self, **kwargs):
                ctx = super().get_context_data(**kwargs)
                ctx.update({
                    'hx_target': '#table_content_documento_swap',
                    'hx-swap': 'outerHTML',
                })
                return ctx

        return ODeleteView


def dame_documentos_versat(request, dpto):
    unidadcontable = request.user.ueb

    title_error = _("Couldn't connect")
    text_error = _('Connection error to Versat API')

    try:
        # TODO implemetar la funcionalidad para que devuelva la fecha de inicio de procesamiento, la fecha de procesamiento y
        # el mes de procesamiento
        fecha_inicio_procesamiento = '2023-01-18'
        fecha_procesamiento = '2023-01-25'
        fecha_mes_procesamiento = '2023-01-01'
        dpto = Departamento.objects.get(pk=dpto)
        param = {'fecha_desde': fecha_inicio_procesamiento,
                 'fecha_hasta': fecha_procesamiento,
                 'unidad': unidadcontable.codigo,
                 'centro_costo': dpto.centrocosto.clave
                 }
        response = getAPI('documentogasto', param)

        if response and response.status_code == 200:
            datos = response.json()['results']
            ids = ids_documentos_versat_procesados(fecha_mes_procesamiento, fecha_procesamiento, dpto, unidadcontable)
            datos = list(filter(lambda x: x['iddocumento'] not in ids, datos))
            return datos

    except Exception as e:
        sweetify.error(request=request, title=title_error, text=text_error)
        return redirect(crud_url_name(Documento, 'list', 'app_index:flujo:'))
