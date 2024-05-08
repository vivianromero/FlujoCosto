from django.shortcuts import render

from app_index.views import CommonCRUDView
from flujo.forms import DepartamentoDocumentosForm, DocumentoForm, DocumentoFormFilter
from flujo.models import Documento
from flujo.tables import DocumentoTable


# Create your views here.

def movimientos(request):
    departamento_documentos_form = DepartamentoDocumentosForm()
    table = DocumentoTable(Documento.objects.all())
    ctx = {
        'departamento_documentos_form': departamento_documentos_form,
        'table': table,
    }
    return render(request, template_name='app_index/flujo/list_table.html', context=ctx)


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

    filterset_class = DocumentoFormFilter

    # Table settings
    paginate_by = 5
    table_class = DocumentoTable

    def get_filter_list_view(self):
        view = super().get_filter_list_view()

        class OFilterListView(view):
            def get_context_data(self, *, object_list=None, **kwargs):
                context = super().get_context_data(**kwargs)
                context.update({
                    'url_importar': 'app_index:importar:numdoc_importar',
                    'filter': False,
                    'url_exportar': 'app_index:exportar:numdoc_exportar'
                })
                return context

        return OFilterListView
