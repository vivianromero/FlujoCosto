from django.db.models import F
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from rest_framework.views import APIView

from codificadores.models import UnidadContable, Medida, MarcaSalida, Cuenta
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


class MPMarcaList(APIView):
    """
    Devuelve las MARCAS DE SALIDA desde SisGestMP
    """

    def get(self, request, format=None):
        try:
            marca = MPMarca.objects.all()
            serializer = MPMarcaSerializer(marca, many=True)
            data = serializer.data
            datos = [MarcaSalida(codigo=item['codigoMarca'].strip(), descripcion=item['descripcion']) for item in data]
            MarcaSalida.objects.bulk_update_or_create(datos, ['descripcion'], match_field='codigo')
            message_success(request=request, title=_("Success"), text=_('Data importation was successful'))
        except Exception as e:
            message_error(request=request, title=_("Couldn't update"), text=_('Data error'))
        return redirect(crud_url_name(MarcaSalida, 'list', 'app_index:codificadores:'))


class ConCuentanatList(APIView):
    """
    Devuelve las unidades de medida
    """

    def get(self, request, format=None):
        try:
            cuentanat = ConCuentanat.objects.select_related().values(
                long_niv=F('idcuenta__idapertura__idmascara__longitud'),
                posicion=F('idcuenta__idapertura__idmascara__posicion'),
                clave_cta=F('idcuenta__clave'),
                descripcion_cta=F('descripcion'),
                naturaleza_cta=F('naturaleza'),
                clavenivel=F('clave'),
                activa=F('idcuenta__activa'),
                ).order_by('clave_cta', 'posicion').all()
            # Llenar las cuentas
            dicc_pk_posicion = {}
            for c in cuentanat:
                posicion = c['posicion']
                clavenivel = c['clavenivel']
                descripcion = c['descripcion_cta']
                long_niv = c['long_niv']
                parent = Cuenta.objects.get(pk=dicc_pk_posicion[posicion - 1]['pk_ant']) if posicion > 1 else None
                clave = dicc_pk_posicion[posicion - 1]['clave_ant'] + '-' + clavenivel.ljust(
                    long_niv) if posicion > 1 else c[
                    'clavenivel']
                cta = Cuenta.objects.update_or_create(clave=clave, defaults={"long_niv": long_niv, "posicion": posicion,
                                                                             "clave": clave, "clavenivel": clavenivel,
                                                                             "descripcion": descripcion,
                                                                             "parent": parent}
                                                      )
                dicc_pk_posicion[posicion] = {'pk_ant': cta[0].pk, 'clave_ant': clave}

            message_success(request=request, title=_("Success"), text=_('Data importation was successful'))
        except Exception as e:
            message_error(request=request, title=_("Couldn't update"), text=_('Data error'))
        return redirect(crud_url_name(Medida, 'list', 'app_index:codificadores:'))
