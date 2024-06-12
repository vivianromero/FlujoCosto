from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _

from codificadores.models import UnidadContable, CentroCosto
from cruds_adminlte3.utils import crud_url_name
from utiles.decorators import adminempresa_required
from utiles.utils import message_error, message_success
from .functionapi import getAPI

title_error = _("Couldn't connect")
text_error = _('Connection error to Versat API')

@adminempresa_required
def UC_Versat(request):
    try:
        response = getAPI('unidad')
        if response and response.status_code == 200:
            data_json_data = response.json() # Assuming the response is in JSON format
            data_json = data_json_data if isinstance(data_json_data, list) else data_json_data['results']
            datos = [UnidadContable(codigo=item['codigo'].strip(), nombre=item['nombre'].strip(), activo=item['activo']) for item in data_json]
            UnidadContable.objects.bulk_update_or_create(datos, ['nombre'], match_field='codigo')
            message_success(request=request, title=_("Success"), text=_('Data importation was successful'))
        else:
            message_error(request=request, title=title_error, text=text_error)
    except Exception as e:
        message_error(request=request, title=title_error, text=text_error)

    return redirect(crud_url_name(UnidadContable, 'list', 'app_index:codificadores:'))

@adminempresa_required
def CC_Versat(request):
    try:
        response = getAPI('costo')
        if response and response.status_code == 200:
            data_json_data = response.json()  # Assuming the response is in JSON format
            data_json = data_json_data if isinstance(data_json_data, list) else data_json_data['results'] # Assuming the response is in JSON format
            datos = [CentroCosto(clave=item['centro'].strip(), descripcion=item['descripcion'].strip()) for item in data_json]
            CentroCosto.objects.bulk_update_or_create(datos, ['clave','descripcion'], match_field='clave')
            message_success(request=request, title=_("Success"), text=_('Data importation was successful'))
        else:
            message_error(request=request, title=title_error, text=text_error)
    except Exception as e:
        message_error(request=request, title=title_error, text=text_error)

    return redirect(crud_url_name(CentroCosto, 'list', 'app_index:codificadores:'))


