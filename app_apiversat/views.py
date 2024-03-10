from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _

from codificadores.models import UnidadContable
from cruds_adminlte3.utils import crud_url_name
from utiles.decorators import adminempresa_required
from utiles.utils import message_error, message_success
from .functionapi import getAPI


@adminempresa_required
def UC_Versat(request):
    try:
        title_error = _("Couldn't update")
        text_error = _('Connection error')
        response = getAPI('unidad')
        if response and response.status_code == 200:
            data_json = response.json()  # Assuming the response is in JSON format
            datos = [UnidadContable(codigo=item['codigo'], nombre=item['nombre'], activo=item['activo']) for item in data_json]
            UnidadContable.objects.bulk_update_or_create(datos, ['nombre','activo'], match_field='codigo')
            message_success(request=request, title=_("Success"), text=_('Data importation was successful'))
        else:
            message_error(request=request, title=title_error, text=text_error)
    except Exception as e:
        message_error(request=request, title=title_error, text=text_error)

    return redirect(crud_url_name(UnidadContable, 'list', 'app_index:codificadores:'))


