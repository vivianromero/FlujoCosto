from django.shortcuts import redirect
from rest_framework.views import APIView

from codificadores.models import UnidadContable, Medida
from cruds_adminlte3.utils import crud_url_name
from .serializers import *
from rest_framework.response import Response

class GenUnidadMedidaList(APIView):
    """
    Devuelve las unidades de medida
    """

    def get(self, request, format=None):
        try:
            medida = GenMedida.objects.all()
            serializer = GenUnidadMedidaSerializer(medida, many=True)
            data = serializer.data
            datos = [Medida(clave=item['clave'].strip(), descripcion=item['descripcion']) for item in data]
            Medida.objects.bulk_update_or_create(datos, ['descripcion'], match_field='clave')
        except Exception as e:
            message_error(request=request, title=_("Couldn't update"), text=_('Data error'))
        return redirect(crud_url_name(Medida, 'list', 'app_index:codificadores:'))

class GenUnidadContableList(APIView):
    """
    Devuelve las unidades de medida
    """

    def get(self, request, format=None):
        try:
            medida = GenUnidadcontable.objects.all()
            serializer = GenUnidadcontableSerializer(medida, many=True)
            data = serializer.data
            datos = [UnidadContable(codigo=item['codigo'], nombre=item['nombre'], activo=item['activo']) for item in
                     data_json]
            UnidadContable.objects.bulk_update_or_create(datos, ['nombre', 'activo'], match_field='codigo')
        except Exception as e:
            message_error(request=request, title=_("Couldn't update"), text=_('Data error'))
        return redirect(crud_url_name(UnidadContable, 'list', 'app_index:codificadores:'))
