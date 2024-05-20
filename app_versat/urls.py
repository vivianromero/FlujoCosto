from django.urls import path
from . import views

app_name = 'appversat'
urlpatterns = [
    path('um_appversat/', views.GenUnidadMedidaList.as_view(), name='um_appversat'),
    path('ms_appversat/', views.MPMarcaList.as_view(), name='ms_appversat'),
    path('ccta_appversat/', views.ConCuentanatList.as_view(), name='ccta_appversat'),
    path('prod_appversat/<str:valor_inicial>/<str:clase_mat_prima>/', views.ProductoFlujoList.as_view(), name='prod_appversat'),
    path('vit_appversat/', views.VitolaList.as_view(), name='vit_appversat'),
    path('invdoc_appversat/', views.DocumnetosInvList.as_view(), name='invdoc_appversat'),
]


