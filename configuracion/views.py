from app_index.views import CommonCRUDView
from .filters import *
from .forms import *
from .tables import *


# Create your views here.
# class UebCRUD(CommonCRUDView):
#     model = Ueb
#
#     namespace = 'app_index:configuracion'
#
#     fields = [
#         'idunidadcontable',
#     ]
#
#     # Hay que agregar __icontains luego del nombre del campo para que busque el contenido
#     # y no distinga entre mayúsculas y minúsculas.
#     # En el caso de campos relacionados hay que agregar __<nombre_campo_que_se_muestra>__icontains
#     search_fields = [
#         'idunidadcontable__nombre__contains',
#     ]
#
#     # search_method = hecho_extraordinario_search_queryset
#
#     add_form = UebForm
#     update_form = UebForm
#
#     list_fields = [
#         'idunidadcontable',
#     ]
#
#     filter_fields = [
#         'idunidadcontable',
#     ]
#
#     filterset_class = UebFilter
#
#     # Table settings
#     table_class = UebTable


class UserUebCRUD(CommonCRUDView):
    model = UserUeb

    namespace = 'app_index:configuracion'

    fields = [
        'ueb',
        'user',
    ]

    # Hay que agregar __icontains luego del nombre del campo para que busque el contenido
    # y no distinga entre mayúsculas y minúsculas.
    # En el caso de campos relacionados hay que agregar __<nombre_campo_que_se_muestra>__icontains
    search_fields = [
        'ueb__idunidadcontable__nombre__icontains',
        'user__username__icontains',
    ]

    add_form = UserUebForm
    update_form = UserUebForm

    list_fields = fields

    filter_fields = fields

    filterset_class = UserUebFilter

    # Table settings
    table_class = UserUebTable
    aa=1
