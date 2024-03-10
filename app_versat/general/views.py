from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from rest_framework.views import APIView

from codificadores.models import UnidadContable, Medida
from cruds_adminlte3.utils import crud_url_name
from utiles.utils import message_success, message_error
from .serializers import *


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
            # messages.success(self.request, _('Data importation was successful'))
            message_success(request=request, title=_("Success"), text=_('Data importation was successful'))
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
            message_success(request=request, title=_("Success"), text=_('Data importation was successful'))
        except Exception as e:
            message_error(request=request, title=_("Couldn't update"), text=_('Data error'))
        return redirect(crud_url_name(UnidadContable, 'list', 'app_index:codificadores:'))
