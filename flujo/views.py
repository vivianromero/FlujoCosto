from django.shortcuts import render
from datetime import datetime
from django.db.models import F
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from app_apiversat.functionapi import getAPI
from app_index.views import CommonCRUDView
from codificadores.models import Departamento
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
import datetime
from .forms import DepartamentoDocumentosForm
from .models import DocumentoOrigenVersat, DocumentoVersatRechazado
from app_apiversat.functionapi import getAPI

from .models import *
from .utils import ids_documentos_versat_procesados


# Create your views here.

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

    def get_filter_list_view(self):
        view = super().get_filter_list_view()

        class OFilterListView(view):
            def get_context_data(self, *, object_list=None, **kwargs):
                context = super().get_context_data(**kwargs)
                dep_queryset = context['form'].fields['departamento'].queryset
                dep_queryset = dep_queryset.filter(unidadcontable=self.request.user.ueb)
                context['form'].fields['departamento'].queryset = dep_queryset

                tableversat = None
                if self.dep:
                    datostableversat = dame_documentos_versat(self.request, self.dep)
                    tableversat = DocumentosVersatTable(datostableversat)

                context.update({
                    'filter': False,
                    'select_period': True,
                    'period_form': DepartamentoDocumentosForm(initial={'departamento': self.dep}),
                    'url_docversat': reverse_lazy(
                        crud_url_name(Documento, 'list', 'app_index:flujo:')) if self.dep else None,
                    'tableversat': tableversat if tableversat else None,
                    "hx_get": reverse_lazy(crud_url_name(Documento, 'list', 'app_index:flujo:')),
                    "hx_target": '#main_content_swap',
                })
                return context

            def get_queryset(self):
                queryset = super().get_queryset()
                formating = '%d/%m/%Y'
                self.dep = self.request.GET.get('departamento', None)
                fecha = self.request.GET.get('fecha', None)
                if self.request.htmx and self.request.htmx.current_url_abs_path.split('?').__len__() > 1:
                    depx = [i for i in self.request.htmx.current_url_abs_path.split('?')[1].split('&') if i != '']
                else:
                    depx = []
                if self.dep is not None:
                    queryset = queryset.filter(departamento=self.dep)
                if fecha is not None:
                    fechas = fecha.strip().split('-')
                    queryset = queryset.filter(
                        fecha__gte=datetime.datetime.strptime(fechas[0].strip(), formating).date(),
                        fecha__lte=datetime.datetime.strptime(fechas[1].strip(), formating).date()
                    )
                if self.dep is None or fecha is None:
                    if len(depx) > 0:
                        depxs = depx[0].split('=')
                        if depxs[0] == 'departamento':
                            queryset = queryset.filter(departamento=depxs[1])
                            self.dep = depxs[1]
                        elif depxs[0] == 'fecha':
                            fechas = depxs[1].strip().split('-')
                            fechas[0] = fechas[0].replace('%20', '').replace('%2F', '/')
                            fechas[1] = fechas[1].replace('%20', '').replace('%2F', '/')
                            queryset = queryset.filter(
                                fecha__gte=datetime.datetime.strptime(fechas[0].strip(), formating).date(),
                                fecha__lte=datetime.datetime.strptime(fechas[1].strip(), formating).date()
                            )
                else:
                    queryset = queryset.none()
                return queryset

        return OFilterListView


def dame_documentos_versat(request, dpto):
    unidadcontable = request.user.ueb

    title_error = _("Couldn't update")
    text_error = _('Connection error')

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
        message_error(request=request, title=title_error, text=text_error)
        return redirect(crud_url_name(Documento, 'list', 'app_index:flujo:'))
