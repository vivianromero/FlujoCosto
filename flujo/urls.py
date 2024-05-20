from django.urls import path, include
from . import views
from app_versat.views import *


documento_crud = views.DocumentoCRUD()
app_name = 'flujo'

urlpatterns = [
    # path('movimientos/', views.movimientos, name='movimientos'),
    path('', include(documento_crud.get_urls())),
    # path('dame_documentos_versat/', views.dame_documentos_versat, name='dame_documentos_versat'),
]