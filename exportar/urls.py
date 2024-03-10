from django.urls import path

from . import views

app_name = 'exportar'
urlpatterns = [
    path('uc_exportar/', views.uc_exportar, name='uc_exportar'),
    path('um_exportar/', views.um_exportar, name='um_exportar'),
    path('umc_exportar/', views.umc_exportar, name='umc_exportar'),
    path('ms_exportar/', views.ms_exportar, name='ms_exportar'),
]

