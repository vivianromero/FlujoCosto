from django.urls import path

from . import views

app_name = 'importar'
urlpatterns = [
    path('uc_importar/', views.uc_importar, name='uc_importar'),
    path('um_importar/', views.um_importar, name='um_importar'),
    path('umc_importar/', views.umc_importar, name='umc_importar'),
    # path('ms_importar/', views.ms_importar, name='ms_importar'),
]

