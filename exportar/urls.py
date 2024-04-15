from django.urls import path

from . import views

app_name = 'exportar'
urlpatterns = [
    path('uc_exportar/', views.uc_exportar, name='uc_exportar'),
    path('um_exportar/', views.um_exportar, name='um_exportar'),
    path('umc_exportar/', views.umc_exportar, name='umc_exportar'),
    path('ms_exportar/', views.ms_exportar, name='ms_exportar'),
    path('cc_exportar/', views.cc_exportar, name='cc_exportar'),
    path('ccta_exportar/', views.ccta_exportar, name='ccta_exportar'),
    path('dpto_exportar/', views.dpto_exportar, name='dpto_exportar'),
    path('prod_exportar/', views.prod_exportar, name='prod_exportar'),
    path('cprod_exportar/', views.cprod_exportar, name='cprod_exportar'),
    path('vit_exportar/', views.vit_exportar, name='vit_exportar'),
]

