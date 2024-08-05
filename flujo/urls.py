from django.urls import path, include
from . import views
from app_versat.views import *

documento_crud = views.DocumentoCRUD()
app_name = 'flujo'

urlpatterns = [
    path('', include(documento_crud.get_urls())),
    path('<uuid:pk>/confirm_doc/', views.confirmar_documento, name='flujo_documento_confirm'),
    path('<uuid:pk>/refused_doc/', views.rechazar_documento, name='flujo_documento_refused'),
    path(r"^(?P<pk>\d+)/inicializar_dep/$", views.inicializar_departamento, name='codificadores_departamento_inicializar'),
    path("obtener_documento_versat/", views.ObtenerDocumentoVersatModalFormView.as_view(), name='obtener_documento_versat'),
    path('precioproducto/', views.precioproducto, name='precioproducto'),
    path('departamentosueb/', views.departamentosueb, name='departamentosueb'),
    path('productosdestino/', views.productosdestino, name='productosdestino'),
    path('estadodestino/', views.estadodestino, name='estadodestino'),
    path('obtener_fecha/', views.DameFechaModalFormView.as_view(), name='obtener_fecha'),
    path('obtener_fecha_procesamiento/', views.obtener_fecha_procesamiento, name='obtener_fecha_procesamiento'),
]
