from django.urls import path

from . import views

app_name = 'importar'
urlpatterns = [
    path('uc_importar/', views.uc_importar, name='uc_importar'),
    path('um_importar/', views.um_importar, name='um_importar'),
    path('umc_importar/', views.umc_importar, name='umc_importar'),
    path('ms_importar/', views.ms_importar, name='ms_importar'),
    path('ma_importar/', views.ma_importar, name='ma_importar'),
    path('cc_importar/', views.cc_importar, name='cc_importar'),
    path('ccta_importar/', views.ccta_importar, name='ccta_importar'),
    path('dpto_importar/', views.dpto_importar, name='dpto_importar'),
    path('prod_importar/', views.prod_importar, name='prod_importar'),
    path('cprod_importar/', views.cprod_importar, name='cprod_importar'),
    path('vit_importar/', views.vit_importar, name='vit_importar'),
    path('ls_importar/', views.ls_importar, name='ls_importar'),
    path('numdoc_importar/', views.numdoc_importar, name='numdoc_importar'),
    path('confccelemg_importar/', views.confccelemg_importar, name='confccelemg_importar'),
    path('all_conf_importar/', views.all_conf_importar, name='all_conf_importar'),
    path('nc_importar/', views.nc_importar, name='nc_importar'),
    path('clacargos_importar/', views.clacargos_importar, name='clacargos_importar'),
    path('filafichacosto_importar/', views.filafichacosto_importar, name='filafichacosto_importar'),
    path('configuracionesgen_importar/', views.configuracionesgen_importar, name='configuracionesgen_importar'),
]

