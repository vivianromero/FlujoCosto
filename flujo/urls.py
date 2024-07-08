from django.urls import path, include
from . import views
from app_versat.views import *

documento_crud = views.DocumentoCRUD()
app_name = 'flujo'

urlpatterns = [
    path('', include(documento_crud.get_urls())),
    path(r"^(?P<pk>\d+)/confirm_doc/$", views.confirmar_documento, name='flujo_documento_confirm'),
    path(r"^(?P<pk>\d+)/inicializar_dep/$", views.inicializar_departamento, name='codificadores_departamento_inicializar'),
    path("obtener_documento_versat/", views.ObtenerDocumentoVersatModalFormView.as_view(), name='obtener_documento_versat'),
    path("aceptar_doc_versat/<iddocumento>/<detalles>/<departamento>/", views.aceptar_documento_versat, name='flujo_documento_versat_aceptar'),
    path("rechazar_doc_versat/<iddocumento>/", views.rechazar_documento_versat, name='flujo_documento_versat_rechazar'),
    path('precioproducto/', views.precioproducto, name='precioproducto'),
    # path("traer_producto_versat/", views.TraerProductoVersatModalFormView.as_view(), name='traer_producto_versat'),
    # path("crear_producto_versat/<str:tipoproducto>/<str:clase_mat_prima>/<str:producto_codigo>/<str:producto_descripcion>/<str:medida_clave>/<str:cantidad>/<str:precio>/", views.crear_producto_versat, name='crear_producto_versat'),
]
