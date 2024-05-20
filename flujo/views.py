from django.shortcuts import render

from app_index.views import CommonCRUDView
from flujo.filters import DocumentoFilter
from flujo.forms import DepartamentoDocumentosForm, DocumentoForm, DocumentoFormFilter
from flujo.models import Documento
from flujo.tables import DocumentoTable, DocumentosVersatTable
from codificadores.tables import CentroCostoTable
from codificadores.models import CentroCosto, Departamento
from app_versat.inventario import InvDocumento, InvDocumentocta, InvDocumentogasto
from app_versat.serializersdata import InvDocumentoSerializer, InvDocumentogastoSerializer

from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django_htmx.http import HttpResponseLocation
import requests
from dynamic_db_router.router import THREAD_LOCAL
from dynamic_db_router import in_database
from configuracion.models import ConexionBaseDato
from configuracion import ChoiceSystems
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
                    datostableversat = dame_documentos_versat(self.request)
                    tableversat = DocumentosVersatTable(datostableversat)

                context.update({
                    'filter': True,
                    'url_docversat': reverse_lazy(crud_url_name(Documento, 'list', 'app_index:flujo:')),
                    'tableversat': tableversat if tableversat else None,
                    "hx_get": reverse_lazy(crud_url_name(Documento, 'list', 'app_index:flujo:')),
                    "hx_target": '#main_content_swap',
                })
                return context
            
            def get_queryset(self):
                queryset = super().get_queryset()
                self.dep = self.request.GET.get('departamento', None)
                if self.dep is not None:
                    queryset = queryset.filter(departamento=self.dep)
                elif self.request.htmx and self.request.htmx.current_url_abs_path.split('?').__len__() > 1:
                    depx = [i for i in self.request.htmx.current_url_abs_path.split('?')[1].split('&') if i != '']
                    if len(depx) > 0:
                        depxs = depx[0].split('=')
                        if depxs[0] == 'departamento':
                            queryset = queryset.filter(departamento=depxs[1])
                            self.dep = depxs[1]
                else:
                    queryset = queryset.none()
                return queryset

        return OFilterListView

def dame_documentos_versat(request):
    unidadcontable = request.user.ueb
    departamento = request.GET.get('departamento', None)
    title_error = _("Couldn't update")
    text_error = _('Connection error')

    try:
        response = getAPI('documentogasto', {'fecha_desde': '2023-01-18', 'fecha_hasta': '2023-01-18'})

        if response and response.status_code == 200:
            datos = response.json()['results']
            return datos
    except Exception as e:
        message_error(request=request, title=title_error, text=text_error)
        return redirect(crud_url_name(Documento, 'list', 'app_index:flujo:'))

