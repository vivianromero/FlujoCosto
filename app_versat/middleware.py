from django.urls import resolve
from django.shortcuts import redirect
from django.urls import resolve
from django.utils.translation import gettext_lazy as _, pgettext
from dynamic_db_router import in_database

from codificadores.models import Medida, MarcaSalida, Cuenta, ProductoFlujo, Vitola
from configuracion.models import ConexionBaseDato
from cruds_adminlte3.utils import crud_url_name
from utiles.utils import message_error
from configuracion import ChoiceSystems
from flujo.models import Documento
from app_versat.inventario import InvDocumento
from flujo.tables import DocumentosVersatTable


class DatabaseConectionMiddleware:
    header = 'HTTP_CONNECTION_TOKEN'
    header_name = 'Connection-Token'

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        user = request.user
        sistema = ChoiceSystems.VERSATSARASOLA
        try:
            match = resolve(request.path)
            if not user.is_authenticated or not 'appversat' in match.namespaces:
                if not 'invdoc_appversat' in request.path.split('/'):
                    return self.get_response(request)
            # if not user.is_adminempresa:
            #     return redirect('app_index:noauthorized')
            url_name = 'invdoc_appversat' if not match.url_name else match.url_name
            object = None
            prefix = 'app_index:codificadores:'
            match url_name:
                case 'um_appversat':
                    object = Medida
                case 'ms_appversat':
                    object = MarcaSalida
                    sistema = ChoiceSystems.SISGESTMP
                case 'ccta_appversat':
                    object = Cuenta
                case 'prod_appversat':
                    object = ProductoFlujo
                case 'vit_appversat':
                    object = Vitola
                    sistema = ChoiceSystems.SISPAX
                case 'invdoc_appversat':
                    prefix = 'app_index:flujo:'
                    object = Documento
                    # table = DocumentosVersatTable()
            try:
                conection = ConexionBaseDato.objects.get(unidadcontable=user.ueb, sistema=sistema)

                external_db = {
                    'ENGINE': 'mssql',
                    'NAME': conection.database_name,
                    'USER': conection.database_user,
                    'PASSWORD': conection.password,
                    'HOST': conection.host,
                    'PORT': '',
                    'ATOMIC_REQUESTS': True,
                    # 'CONN_REQUESTS': True,
                    'TIME_ZONE': None,
                    'CONN_HEALTH_CHECKS': True,
                    'CONN_MAX_AGE': 60,
                    'AUTOCOMMIT': True,
                    'OPTIONS': {
                        'driver': 'ODBC Driver 17 for SQL Server',
                        'connect_timeout': 5,
                    },
                }
                with in_database(external_db, read=True, write=True):
                    response = self.get_response(request)
                return response if response.status_code == 200 else redirect(
                    crud_url_name(object, 'list', prefix))


                # return redirect(crud_url_name(object, 'list', prefix), kwargs=[response.data])  if response.status_code == 200 else redirect(
                #     crud_url_name(object, 'list', prefix))
                # return Response(response)  if response.status_code == 200 else redirect(
                #     crud_url_name(object, 'list', prefix))
                # return response

            except ConexionBaseDato.DoesNotExist:
                message_error(request=request, title=_("Couldn't connect"),
                              # text=_('Database connect for Versat Sarasola not define'))
                              text=pgettext("Error conection", "Database connect for %s not define") % (sistema))
                return redirect(crud_url_name(object, 'list', prefix))
            except Exception as e:
                message_error(request=request, title=_("Couldn't connect"), text=_('Connection error'))
                return redirect(crud_url_name(object, 'list', prefix))
        except KeyError:
            message_error(request=request, title=_("Couldn't connect"), text=_('Connection error'))
            return redirect(crud_url_name(object, 'list', prefix))
