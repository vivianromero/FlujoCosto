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
confcentroselementosotrosdetalle_crud = views.ConfCentrosElementosOtrosDetalleCRUD()
confcentroselementosotrosdetallegrouped_crud = views.ConfCentrosElementosOtrosDetalleGroupedCRUD()
producto_capas_pesadas_crud = views.ProductsCapasClaPesadasCRUD()
tipodocumento_crud = views.TipoDocumentoCRUD()
clasificadorcargos_crud = views.ClasificadorCargosCRUD()
filasfichacosto_crud = views.FichaCostoFilasCRUD()
configuraciones_gen_crud = views.ConfiguracionesGenCRUD()

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
    path("", include(confcentroselementosotrosdetallegrouped_crud.get_urls())),
    path("", include(confcentroselementosotrosdetalle_crud.get_urls())),
    path("", include(producto_capas_pesadas_crud.get_urls())),
    path("", include(clasificadorcargos_crud.get_urls())),
    path("", include(filasfichacosto_crud.get_urls())),
    path('classmatprima/', views.classmatprima, name='classmatprima'),
    path("", include(tipodocumento_crud.get_urls())),
    path(r"^(?P<pk>\d+)/confirm_nc/$", views.confirm_nc, name='codificadores_normaconsumo_confirm'),
    path(r"^(?P<pk>\d+)/activar_nc/$", views.activar_nc, name='codificadores_normaconsumo_activar'),
    path('productmedida/', views.productmedida, name='productmedida'),
    path('productmedidadetalle/', views.productmedidadetalle, name='productmedidadetalle'),
    path('rendimientocapa/', views.rendimientocapa, name='rendimientocapa'),
    path('precio_lop/', views.precio_lop, name='precio_lop'),
    path('vitolas/', views.vitolas, name='vitolas'),
    path('cargonorma/', views.cargonorma, name='cargonorma'),
    path('calcula_nt/', views.calcula_nt, name='calcula_nt'),
    path('fila_encabezado/', views.fila_encabezado, name='fila_encabezado'),
    path('fila_calculado/', views.fila_calculado, name='fila_calculado'),
    path('fila_desglosado/', views.fila_desglosado, name='fila_desglosado'),
    path("", include(configuraciones_gen_crud.get_urls())),
]
