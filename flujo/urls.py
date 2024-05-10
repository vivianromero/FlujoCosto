from django.urls import path, include
from . import views


documento_crud = views.DocumentoCRUD()
app_name = 'flujo'

urlpatterns = [
    path('movimientos/', views.movimientos, name='movimientos'),
    path('', include(documento_crud.get_urls())),
]