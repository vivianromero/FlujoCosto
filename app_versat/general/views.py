from django.shortcuts import redirect
from rest_framework.views import APIView

from codificadores.models import UnidadContable, Medida
from cruds_adminlte3.utils import crud_url_name
from .serializers import *

class GenUnidadcontableList(APIView):
    """
    Devuelve las unidades contables
    """

    def get(self, request, format=None):
        unidad = GenUnidadcontable.objects.all()
        serializer = GenUnidadcontableSerializer(unidad, many=True)
        data = serializer.data
        datos = [UnidadContable(codigo=item['codigo'], nombre=item['nombre'], activo=item['activo']) for item in data]
        UnidadContable.objects.bulk_update_or_create(datos, ['nombre', 'activo'], match_field='codigo')
        return redirect(crud_url_name(UnidadContable, 'list', 'app_index:codificadores:'))

class GenUnidadMedidaList(APIView):
    """
    Devuelve las unidades de medida
    """

    def get(self, request, format=None):
        medida = GenMedida.objects.all()
        serializer = GenUnidadMedidaSerializer(medida, many=True)
        data = serializer.data
        datos = [Medida(clave=item['clave'], descripcion=item['descripcion']) for item in data]
        Medida.objects.bulk_update_or_create(datos, ['descripcion'], match_field='clave')
        return redirect(crud_url_name(Medida, 'list', 'app_index:codificadores:'))
