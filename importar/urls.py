from django.urls import path

from . import views

app_name = 'importar'
urlpatterns = [
    path('uc_importar/', views.uc_importar, name='uc_importar'),
    path('um_importar/', views.um_importar, name='um_importar'),
    path('umc_importar/', views.umc_importar, name='umc_importar'),
    path('ms_importar/', views.ms_importar, name='ms_importar'),
    path('cc_importar/', views.cc_importar, name='cc_importar'),
    path('ccta_importar/', views.ccta_importar, name='ccta_importar'),
    path('dpto_importar/', views.dpto_importar, name='dpto_importar'),
    path('prod_importar/', views.prod_importar, name='prod_importar'),
    path('cprod_importar/', views.cprod_importar, name='cprod_importar'),
]

