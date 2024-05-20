from django.urls import path, include
from . import views
from app_versat.views import *


documento_crud = views.DocumentoCRUD()
app_name = 'flujo'

urlpatterns = [
    path('', include(documento_crud.get_urls())),
]