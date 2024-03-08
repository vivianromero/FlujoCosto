from django.http import HttpResponse
from django.urls import resolve
from django.utils.translation import gettext_lazy as _
from django.shortcuts import redirect
from dynamic_db_router import in_database
from django.db import connections

from configuracion.models import ConexionBaseDato
from utiles.utils import message_error
from codificadores.models import UnidadContable, Medida
from cruds_adminlte3.utils import crud_url_name


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
        try:
            match = resolve(request.path)
            if not user.is_authenticated or not 'appversat' in match.namespaces:
                return self.get_response(request)
            if not user.is_adminempresa:
                return redirect('app_index:noauthorized')
            url_name = match.url_name
            object = None
            match url_name:
                case 'um_appversat':
                    object=Medida
                # case 'uc_appversat':
                #     object=UnidadContable
                # case _:
                #     action - default
            try:
                conection = ConexionBaseDato.objects.get(idunidadcontable=user.idueb, sistema='VersatSarasola1')

                external_db = {
                    'ENGINE': 'mssql',
                    'NAME': 'conection.database_name',
                    'USER': conection.database_user,
                    'PASSWORD': conection.password,
                    'HOST': conection.host,
                    'PORT': '',
                    'ATOMIC_REQUESTS': True,
                    'CONN_REQUESTS': True,
                    'TIME_ZONE': None,
                    'CONN_HEALTH_CHECKS': False,
                    'CONN_MAX_AGE': 0,
                    'AUTOCOMMIT': True,
                    'OPTIONS': {
                        'driver': 'ODBC Driver 17 for SQL Server',
                        'connect_timeout': 5,
                    },
                }
                with in_database(external_db, read=True, write=True):
                    response = self.get_response(request)
                return response if response.status_code==200 else redirect(crud_url_name(object, 'list', 'app_index:codificadores:'))

            except ConexionBaseDato.DoesNotExist:
                message_error(request=request, title=_("Couldn't connect"), text=_('Database connect for Versat Sarasola not define'))
                return redirect(crud_url_name(object, 'list', 'app_index:codificadores:'))
            except Exception as e:
                message_error(request=request, title=_("Couldn't connect"), text=_('Connection error'))
                return redirect(crud_url_name(object, 'list', 'app_index:codificadores:'))
        except KeyError:
            message_error(request=request, title=_("Couldn't connect"), text=_('Connection error'))
            return redirect(crud_url_name(object, 'list', 'app_index:codificadores:'))
