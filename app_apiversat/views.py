from django.shortcuts import redirect
from .functionapi import getAPI
from cruds_adminlte3.utils import crud_url_name
from codificadores.models import UnidadContable
from utiles.decorators import adminempresa_required

@adminempresa_required
def UC_Versat(request):
    response = getAPI('unidad')
    if response.status_code == 200:
        data_json = response.json()  # Assuming the response is in JSON format
        datos = [UnidadContable(codigo=item['codigo'], nombre=item['nombre'], activo=item['activo']) for item in data_json]
        UnidadContable.objects.bulk_update_or_create(datos, ['nombre','activo'], match_field='codigo')
        return redirect(crud_url_name(UnidadContable, 'list', 'app_index:codificadores:'))
    else:
        print(f"Request failed with status code {response.status_code}")
        print(response.text)


