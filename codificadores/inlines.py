from extra_views import InlineFormSetFactory

from cruds_adminlte3.inline_crud import InlineAjaxCRUD
from .models import *
from .forms import *


class NormaconsumoDetalleInline(InlineFormSetFactory):
    model = NormaconsumoDetalle
    form_class = NormaConsumoDetalleForm
    fields = [
        'norma_ramal',
        'norma_empresarial',
        'operativo',
        'normaconsumo',
        'producto',
        'medida'
    ]
    factory_kwargs = {"extra": 0}

