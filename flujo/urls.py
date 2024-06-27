from django.urls import path, include
from . import views
from app_versat.views import *

documento_crud = views.DocumentoCRUD()
app_name = 'flujo'

urlpatterns = [
    path('', include(documento_crud.get_urls())),
    path(r"^(?P<pk>\d+)/confirm_doc/$", views.confirmar_documento, name='flujo_documento_confirm'),
    path(r"^(?P<pk>\d+)/inicializar_dep/$", views.inicializar_departamento, name='codificadores_departamento_inicializar'),
]
