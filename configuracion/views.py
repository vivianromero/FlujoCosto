from app_index.views import CommonCRUDView
from .filters import *
from .forms import *
from .tables import *

class ConexionBaseDatoCRUD(CommonCRUDView):
    model = ConexionBaseDato

    namespace = 'app_index:configuracion'

    fields = [
        'sistema',
        'database_name',
        'host',
        'port',
        'database_user',
        'password',
        'unidadcontable',
    ]

    # Hay que agregar __icontains luego del nombre del campo para que busque el contenido
    # y no distinga entre mayúsculas y minúsculas.
    # En el caso de campos relacionados hay que agregar __<nombre_campo_que_se_muestra>__icontains
    search_fields = [
        'sistema__icontains',
        'database_name__icontains',
        'unidadcontable__codigo__icontains',
        'unidadcontable__unidadcontable__icontains',
    ]

    add_form = ConexionBaseDatoForm
    update_form = ConexionBaseDatoForm

    list_fields = fields

    filter_fields = fields

    filterset_class = ConexionBaseDatoFilter

    # Table settings
    table_class = ConexionBaseDatoTable

    def get_filter_list_view(self):
        view = super().get_filter_list_view()

        class OFilterListView(view):
            def get_queryset(self):
                qset = super().get_queryset()
                user = self.request.user
                if not user.is_superuser:
                    qset = qset.filter(unidadcontable=user.ueb)
                return qset
        return OFilterListView
