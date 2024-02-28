from django.shortcuts import redirect
from rest_framework.views import APIView

from app_versat.general.general import GenUnidadcontable
from codificadores.models import UnidadContable
from cruds_adminlte3.utils import crud_url_name
from .serializers import GenUnidadcontableSerializer


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
