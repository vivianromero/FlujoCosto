from django.urls import path, include
from . import views

departamento_crud = views.DepartamentoCRUD()
unidad_contable_crud = views.UnidadContableCRUD()
centro_costo_crud = views.CentroCostoCRUD()
medida_crud = views.MedidaCRUD()
medida_conversion_crud = views.MedidaConversionCRUD()
cuenta_crud = views.CuentaCRUD()
producto_flujo_crud = views.ProductoFlujoCRUD()
producto_flujo_cuenta_crud = views.ProductoFlujoCuentaCRUD()
marcasalida_crud = views.MarcaSalidaCRUD()
vitola_crud = views.VitolaCRUD()
motivoajuste_crud = views.MotivoAjusteCRUD()
centrocosto_crud = views.CentroCostoCRUD()
cambioproducto_crud = views.CambioProductoCRUD()
normaconsumo_crud = views.NormaConsumoCRUD()
normaconsumogrouped_crud = views.NormaConsumoGroupedCRUD()
lineasalida_crud = views.LineaSalidaCRUD()
numeraciondocumentos_crud = views.NumeracionDocumentosCRUD()
confcentroselementosotros_crud = views.ConfCentrosElementosOtrosCRUD()
producto_capas_pesadas_crud = views.ProductsCapasClaPesadasCRUD()

app_name = 'codificadores'

urlpatterns = [
    path("", include(departamento_crud.get_urls())),
    path("", include(unidad_contable_crud.get_urls())),
    path("", include(centro_costo_crud.get_urls())),
    path("", include(medida_crud.get_urls())),
    path("", include(medida_conversion_crud.get_urls())),
    path("", include(cuenta_crud.get_urls())),
    path("", include(producto_flujo_crud.get_urls())),
    path("", include(producto_flujo_crud.get_urls())),
    path("", include(marcasalida_crud.get_urls())),
    path("", include(vitola_crud.get_urls())),
    path("", include(motivoajuste_crud.get_urls())),
    path("", include(centrocosto_crud.get_urls())),
    path("", include(cambioproducto_crud.get_urls())),
    path("", include(normaconsumo_crud.get_urls())),
    path("", include(normaconsumogrouped_crud.get_urls())),
    path("obtener_datos", views.ObtenrDatosModalFormView.as_view(), name='obtener_datos'),
    path(
        "obtener_normaconsumodetalle_datos",
        views.NormaConsumoDetalleModalFormView.as_view(),
        name='obtener_normaconsumodetalle_datos'
    ),
    path("", include(lineasalida_crud.get_urls())),
    path("", include(numeraciondocumentos_crud.get_urls())),
    path("", include(confcentroselementosotros_crud.get_urls())),
    path("", include(producto_capas_pesadas_crud.get_urls())),
]
