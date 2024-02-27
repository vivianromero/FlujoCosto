from dynamic_db_router.router import THREAD_LOCAL
from app_versat.general.general import GenUnidadcontable
from django.db import connections
from app_versat.middleware import DatabaseConectionMiddleware
from configuracion.models import UserUeb

def get_ucontables(request):
    # with connections['database_name_read'].cursor() as cursor:
    #     cursor.execute("SELECT * FROM gen_unidadcontable")
    try:
        DatabaseConectionMiddleware.header_name
        external_db = getattr(THREAD_LOCAL, 'DB_FOR_WRITE_OVERRIDE', ['default'])[-1]
        unidades = GenUnidadcontable.objects.all()
    except e:
        return Response({"error": "El sevicio no existe"},
                        status=status.HTTP_404_NOT_FOUND)
    return unidades
