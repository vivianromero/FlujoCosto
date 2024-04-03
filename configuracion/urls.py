from django.urls import path, include
from . import views

database_connection_crud = views.ConexionBaseDatoCRUD()

app_name = 'configuracion'

urlpatterns = [
    path("", include(database_connection_crud.get_urls())),
]
