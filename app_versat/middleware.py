from django.http import HttpResponse
from django.urls import reverse
from dynamic_db_router import in_database

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
        try:
            path = request.path
            # noHeaderRequired = path.startswith(reverse('admin:index')) | path.startswith(reverse('schema', current_app='drf_spectacular')) | (path == '/')
            # if noHeaderRequired:
            #     return self.get_response(request)

            token_conection = request.META[self.header]
            try:
                conection = ConectionDatabase.objects.get(id=token_conection)

                external_db = {
                    'ENGINE': 'mssql',
                    'NAME': conection.database_name,
                    'USER': conection.database_user,
                    'PASSWORD': conection.password,
                    'HOST': conection.host,
                    'PORT': '',
                    'OPTIONS': {
                        'driver': 'ODBC Driver 17 for SQL Server',
                        'extra_params': "app=Versat - API;",
                        'connect_timeout': 5,
                    },
                }

                with in_database(external_db, read=True, write=True):
                    response = self.get_response(request)
                    # Code to be executed for each request/response after
                    # the view is called.
                    return response

                # return self.get_response(request)
            except ConectionDatabase.DoesNotExist:
                res = HttpResponse("Invalid header %s." % self.header_name, status=401)
                res["CONNECTION_TOKEN"] = "Invalid header %s." % self.header_name
                return res
        except KeyError:
            res = HttpResponse("Header %s is  required." % self.header_name, status=401)
            res["CONNECTION_TOKEN"] = "Header %s is  required." % self.header_name
            return res

