from django.urls import path, include
from . import views

departamento_crud = views.DepartamentoCRUD()
# departamento_relacion_crud = views.DepartamentoRelacionCRUD()
unidad_contable_crud = views.UnidadContableCRUD()
centro_costo_crud = views.CentroCostoCRUD()
medida_crud = views.MedidaCRUD()
medida_conversion_crud = views.MedidaConversionCRUD()
cuenta_crud = views.CuentaCRUD()
tipo_producto_crud = views.TipoProductoCRUD()
estado_producto_crud = views.EstadoProductoCRUD()
clase_materia_prima_crud = views.ClaseMateriaPrimaCRUD()
producto_flujo_crud = views.ProductoFlujoCRUD()
producto_flujo_clase_crud = views.ProductoFlujoClaseCRUD()
producto_flujo_destino_crud = views.ProductoFlujoDestinoCRUD()
producto_flujo_cuenta_crud = views.ProductoFlujoCuentaCRUD()
categoria_vitola_crud = views.CategoriaVitolaCRUD()
tipo_vitola_crud = views.TipoVitolaCRUD()
marcasalida_crud = views.MarcaSalidaCRUD()
vitola_crud = views.VitolaCRUD()

app_name = 'codificadores'

urlpatterns = [
    path("", include(departamento_crud.get_urls())),
    # path("", include(departamento_relacion_crud.get_urls())),
    path("", include(unidad_contable_crud.get_urls())),
    path("", include(centro_costo_crud.get_urls())),
    path("", include(medida_crud.get_urls())),
    path("", include(medida_conversion_crud.get_urls())),
    path("", include(cuenta_crud.get_urls())),
    path("", include(tipo_producto_crud.get_urls())),
    path("", include(estado_producto_crud.get_urls())),
    path("", include(clase_materia_prima_crud.get_urls())),
    path("", include(producto_flujo_crud.get_urls())),
    path("", include(producto_flujo_clase_crud.get_urls())),
    path("", include(producto_flujo_destino_crud.get_urls())),
    path("", include(producto_flujo_cuenta_crud.get_urls())),
    path("", include(categoria_vitola_crud.get_urls())),
    path("", include(tipo_vitola_crud.get_urls())),
    path("", include(marcasalida_crud.get_urls())),
    path("", include(vitola_crud.get_urls())),
]

