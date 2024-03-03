from django.http import HttpResponse
from django.shortcuts import redirect
from dynamic_db_router import in_database
from django.urls import resolve

from configuracion.models import ConexionBaseDato


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
            try:
                conection = ConexionBaseDato.objects.get(idunidadcontable=user.idueb, sistema='VersatSarasola')

                external_db = {
                    'ENGINE': 'mssql',
                    'NAME': conection.database_name,
                    'USER': conection.database_user,
                    'PASSWORD': conection.password,
                    'HOST': conection.host,
                    'PORT': conection.port,
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
                    # Code to be executed for each request/response after
                    # the view is called.
                    return response

                # return self.get_response(request)
            except ConexionBaseDato.DoesNotExist:
                res = HttpResponse("Invalid header %s." % self.header_name, status=401)
                res["CONNECTION_TOKEN"] = "Invalid header %s." % self.header_name
                return res
        except KeyError:
            res = HttpResponse("Header %s is  required." % self.header_name, status=401)
            res["CONNECTION_TOKEN"] = "Header %s is  required." % self.header_name
            return res
