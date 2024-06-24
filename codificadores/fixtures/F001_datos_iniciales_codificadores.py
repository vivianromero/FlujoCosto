from codificadores.models import *

modulo = "codificadores"


def init_data(apps, schema_editor):
    act_model_tipo_poducto = apps.get_model(modulo, "TipoProducto")
    act_model_clasemateriaprima = apps.get_model(modulo, "ClaseMateriaPrima")
    act_model_categoriavitola = apps.get_model(modulo, "CategoriaVitola")
    act_model_motivoajuste = apps.get_model(modulo, "MotivoAjuste")
    act_model_tipodocumento = apps.get_model(modulo, "TipoDocumento")
    # act_model_numeraciondocumentos = apps.get_model(modulo, "NumeracionDocumentos")
    act_model_unidadcontable = apps.get_model(modulo, "UnidadContable")
    act_model_confcentroselementosotros = apps.get_model(modulo, "ConfCentrosElementosOtros")
    act_model_confcentroselementosotrosdetalle = apps.get_model(modulo, "ConfCentrosElementosOtrosDetalle")
    act_model_grupo_escala = apps.get_model(modulo, "GrupoEscalaCargo")

    tipo_poducto = [
        TipoProducto(pk=ChoiceTiposProd.PESADA,
                     descripcion=ChoiceTiposProd.CHOICE_TIPOS_PROD[ChoiceTiposProd.PESADA], orden=4),
        TipoProducto(pk=ChoiceTiposProd.MATERIAPRIMA,
                     descripcion=ChoiceTiposProd.CHOICE_TIPOS_PROD[ChoiceTiposProd.MATERIAPRIMA], orden=1),
        TipoProducto(pk=ChoiceTiposProd.HABILITACIONES,
                     descripcion=ChoiceTiposProd.CHOICE_TIPOS_PROD[ChoiceTiposProd.HABILITACIONES], orden=3),
        TipoProducto(pk=ChoiceTiposProd.LINEASALIDA,
                     descripcion=ChoiceTiposProd.CHOICE_TIPOS_PROD[ChoiceTiposProd.LINEASALIDA], orden=5),
        TipoProducto(pk=ChoiceTiposProd.VITOLA,
                     descripcion=ChoiceTiposProd.CHOICE_TIPOS_PROD[ChoiceTiposProd.VITOLA], orden=6),
        TipoProducto(pk=ChoiceTiposProd.SUBPRODUCTO,
                     descripcion=ChoiceTiposProd.CHOICE_TIPOS_PROD[ChoiceTiposProd.SUBPRODUCTO], orden=2),
        TipoProducto(pk=ChoiceTiposProd.LINEASINTERMINAR,
                     descripcion=ChoiceTiposProd.CHOICE_TIPOS_PROD[ChoiceTiposProd.LINEASINTERMINAR], orden=7),
    ]
    act_model_tipo_poducto.objects.bulk_create(tipo_poducto)

    clasemp = [
        ClaseMateriaPrima(pk=ChoiceClasesMatPrima.CAPOTE,
                          descripcion=ChoiceClasesMatPrima.CHOICE_CLASES[ChoiceClasesMatPrima.CAPOTE],
                          capote_fortaleza='C'),
        ClaseMateriaPrima(pk=ChoiceClasesMatPrima.F1,
                          descripcion=ChoiceClasesMatPrima.CHOICE_CLASES[ChoiceClasesMatPrima.F1],
                          capote_fortaleza='F'),
        ClaseMateriaPrima(pk=ChoiceClasesMatPrima.F2,
                          descripcion=ChoiceClasesMatPrima.CHOICE_CLASES[ChoiceClasesMatPrima.F2],
                          capote_fortaleza='F'),
        ClaseMateriaPrima(pk=ChoiceClasesMatPrima.F3,
                          descripcion=ChoiceClasesMatPrima.CHOICE_CLASES[ChoiceClasesMatPrima.F3],
                          capote_fortaleza='F'),
        ClaseMateriaPrima(pk=ChoiceClasesMatPrima.CAPACLASIFICADA,
                          descripcion=ChoiceClasesMatPrima.CHOICE_CLASES[ChoiceClasesMatPrima.CAPACLASIFICADA],
                          capote_fortaleza='P'),
        ClaseMateriaPrima(pk=ChoiceClasesMatPrima.CAPASINCLASIFICAR,
                          descripcion=ChoiceClasesMatPrima.CHOICE_CLASES[ChoiceClasesMatPrima.CAPASINCLASIFICAR],
                          capote_fortaleza='P'),
        ClaseMateriaPrima(pk=ChoiceClasesMatPrima.F4,
                          descripcion=ChoiceClasesMatPrima.CHOICE_CLASES[ChoiceClasesMatPrima.F4],
                          capote_fortaleza='F'),
    ]
    act_model_clasemateriaprima.objects.bulk_create(clasemp)

    categvit = [
        CategoriaVitola(pk=ChoiceCategoriasVit.IX,
                        descripcion=ChoiceCategoriasVit.CHOICE_CATEGORIAS[ChoiceCategoriasVit.IX], orden=5),
        CategoriaVitola(pk=ChoiceCategoriasVit.V,
                        descripcion=ChoiceCategoriasVit.CHOICE_CATEGORIAS[ChoiceCategoriasVit.V], orden=1),
        CategoriaVitola(pk=ChoiceCategoriasVit.VI,
                        descripcion=ChoiceCategoriasVit.CHOICE_CATEGORIAS[ChoiceCategoriasVit.VI], orden=2),
        CategoriaVitola(pk=ChoiceCategoriasVit.VII,
                        descripcion=ChoiceCategoriasVit.CHOICE_CATEGORIAS[ChoiceCategoriasVit.VII], orden=3),
        CategoriaVitola(pk=ChoiceCategoriasVit.VIII,
                        descripcion=ChoiceCategoriasVit.CHOICE_CATEGORIAS[ChoiceCategoriasVit.VIII], orden=4),
    ]
    act_model_categoriavitola.objects.bulk_create(categvit)

    motivoajuste = [
        MotivoAjuste(pk=ChoiceMotivosAjuste.MERMA,
                     descripcion=ChoiceMotivosAjuste.CHOICE_MOTIVOS_AJUSTE[ChoiceMotivosAjuste.MERMA], aumento=False,
                     activo=True),
        MotivoAjuste(pk=ChoiceMotivosAjuste.ROTURA,
                     descripcion=ChoiceMotivosAjuste.CHOICE_MOTIVOS_AJUSTE[ChoiceMotivosAjuste.ROTURA], aumento=False,
                     activo=True),
        MotivoAjuste(pk=ChoiceMotivosAjuste.PROMOCION,
                     descripcion=ChoiceMotivosAjuste.CHOICE_MOTIVOS_AJUSTE[ChoiceMotivosAjuste.PROMOCION],
                     aumento=False, activo=True),
        MotivoAjuste(pk=ChoiceMotivosAjuste.SUBPRODUCTOS,
                     descripcion=ChoiceMotivosAjuste.CHOICE_MOTIVOS_AJUSTE[ChoiceMotivosAjuste.SUBPRODUCTOS],
                     aumento=False, activo=True),
    ]
    act_model_motivoajuste.objects.bulk_create(motivoajuste)

    tipodoc = [
        TipoDocumento(pk=ChoiceTiposDoc.ENTRADA_DESDE_VERSAT,
                      descripcion=ChoiceTiposDoc.CHOICE_TIPOS_DOC[ChoiceTiposDoc.ENTRADA_DESDE_VERSAT], operacion='E',
                      generado=True),
        TipoDocumento(pk=ChoiceTiposDoc.SALIDA_HACIA_VERSAT,
                      descripcion=ChoiceTiposDoc.CHOICE_TIPOS_DOC[ChoiceTiposDoc.SALIDA_HACIA_VERSAT], operacion='S',
                      generado=True),
        TipoDocumento(pk=ChoiceTiposDoc.TRANSF_HACIA_DPTO,
                      descripcion=ChoiceTiposDoc.CHOICE_TIPOS_DOC[ChoiceTiposDoc.TRANSF_HACIA_DPTO], operacion='S',
                      generado=False),
        TipoDocumento(pk=ChoiceTiposDoc.TRANSF_DESDE_DPTO,
                      descripcion=ChoiceTiposDoc.CHOICE_TIPOS_DOC[ChoiceTiposDoc.TRANSF_DESDE_DPTO], operacion='E',
                      generado=True),
        TipoDocumento(pk=ChoiceTiposDoc.AJUSTE_AUMENTO,
                      descripcion=ChoiceTiposDoc.CHOICE_TIPOS_DOC[ChoiceTiposDoc.AJUSTE_AUMENTO], operacion='E',
                      generado=False),
        TipoDocumento(pk=ChoiceTiposDoc.AJUSTE_DISMINUCION,
                      descripcion=ChoiceTiposDoc.CHOICE_TIPOS_DOC[ChoiceTiposDoc.AJUSTE_DISMINUCION], operacion='S',
                      generado=False),
        TipoDocumento(pk=ChoiceTiposDoc.RECEPCION_PRODUCCION_REPROCESO,
                      descripcion=ChoiceTiposDoc.CHOICE_TIPOS_DOC[ChoiceTiposDoc.RECEPCION_PRODUCCION_REPROCESO],
                      operacion='E', generado=False),
        TipoDocumento(pk=ChoiceTiposDoc.RECEPCION_PRODUCCION,
                      descripcion=ChoiceTiposDoc.CHOICE_TIPOS_DOC[ChoiceTiposDoc.RECEPCION_PRODUCCION], operacion='E',
                      generado=False),
        TipoDocumento(pk=ChoiceTiposDoc.DEVOLUCION,
                      descripcion=ChoiceTiposDoc.CHOICE_TIPOS_DOC[ChoiceTiposDoc.DEVOLUCION], operacion='S',
                      generado=False),
        TipoDocumento(pk=ChoiceTiposDoc.SOBRANTE_SUJETO_INVESTIGACION,
                      descripcion=ChoiceTiposDoc.CHOICE_TIPOS_DOC[ChoiceTiposDoc.SOBRANTE_SUJETO_INVESTIGACION],
                      operacion='E', generado=False),
        TipoDocumento(pk=ChoiceTiposDoc.RECEPCION_RECHAZO,
                      descripcion=ChoiceTiposDoc.CHOICE_TIPOS_DOC[ChoiceTiposDoc.RECEPCION_RECHAZO], operacion='E',
                      generado=False),
        TipoDocumento(pk=ChoiceTiposDoc.CARGA_INICIAL,
                      descripcion=ChoiceTiposDoc.CHOICE_TIPOS_DOC[ChoiceTiposDoc.CARGA_INICIAL], operacion='E',
                      generado=False),
        TipoDocumento(pk=ChoiceTiposDoc.DEVOLUCION_RECIBIDA,
                      descripcion=ChoiceTiposDoc.CHOICE_TIPOS_DOC[ChoiceTiposDoc.DEVOLUCION_RECIBIDA], operacion='E',
                      generado=True),
        TipoDocumento(pk=ChoiceTiposDoc.CAMBIO_ESTADO,
                      descripcion=ChoiceTiposDoc.CHOICE_TIPOS_DOC[ChoiceTiposDoc.CAMBIO_ESTADO], operacion='S',
                      generado=False),
        TipoDocumento(pk=ChoiceTiposDoc.TRANSFERENCIA_EXTERNA,
                      descripcion=ChoiceTiposDoc.CHOICE_TIPOS_DOC[ChoiceTiposDoc.TRANSFERENCIA_EXTERNA], operacion='S',
                      generado=False),
        TipoDocumento(pk=ChoiceTiposDoc.RECIBIR_TRANS_EXTERNA,
                      descripcion=ChoiceTiposDoc.CHOICE_TIPOS_DOC[ChoiceTiposDoc.RECIBIR_TRANS_EXTERNA], operacion='E',
                      generado=False),
        TipoDocumento(pk=ChoiceTiposDoc.VENTA_TRABAJADORES,
                      descripcion=ChoiceTiposDoc.CHOICE_TIPOS_DOC[ChoiceTiposDoc.VENTA_TRABAJADORES], operacion='S',
                      generado=False),
        TipoDocumento(pk=ChoiceTiposDoc.REPORTE_SUBPRODUCTOS,
                      descripcion=ChoiceTiposDoc.CHOICE_TIPOS_DOC[ChoiceTiposDoc.REPORTE_SUBPRODUCTOS], operacion='E',
                      generado=False),
        TipoDocumento(pk=ChoiceTiposDoc.CAMBIO_PRODUCTO,
                      descripcion=ChoiceTiposDoc.CHOICE_TIPOS_DOC[ChoiceTiposDoc.CAMBIO_PRODUCTO], operacion='S',
                      generado=False),
    ]
    act_model_tipodocumento.objects.bulk_create(tipodoc)

    NumeracionDocumentos.objects.create(pk=TipoNumeroDoc.NUMERO_CONSECUTIVO, sistema=False, departamento=True,
                                        tipo_documento=True, prefijo=False)
    NumeracionDocumentos.objects.create(pk=TipoNumeroDoc.NUMERO_CONTROL, sistema=True, departamento=True,
                                        tipo_documento=True, prefijo=False)

    ucontab = [
        UnidadContable(pk="000603fa-af2d-4713-b0e5-c2991a289f4b", codigo="01", nombre="UEB SANTA CLARA"),
        UnidadContable(pk="003820bb-9dc1-4cbb-b8cf-93f28322c697", codigo="02", nombre="UEB TT PLACETAS EXPORTACION"),
        UnidadContable(pk="003dec56-d3ac-452d-a2be-9c07539be90f", codigo="03", nombre="UEB CAMAJUANí"),
        UnidadContable(pk="009bfd05-0357-4614-ba5b-c9876272a460", codigo="04", nombre="UEB BAEZ"),
        UnidadContable(pk="009c9e8f-4064-4214-a051-a1f78ea26b65", codigo="05", nombre="UEB QUEMADO"),
        UnidadContable(pk="009c9e9f-4064-4214-a051-a1f78ea26b65", codigo="06", nombre="UEB MANICARAGUA"),
        UnidadContable(pk="009d9e9f-4064-4214-a051-a1f78ea26b85", codigo="07", nombre="UEB ESPERANZA"),
        UnidadContable(pk="109d9e9f-4064-4214-a051-a1f78ea28b65", codigo="08", nombre="UEB RANCHUELO"),
        UnidadContable(pk="209d9e9f-4064-4214-a051-a1f99ea26b65", codigo="09", nombre="UEB REMEDIOS"),
        UnidadContable(pk="309d9e9f-4064-4214-a051-a1f78ea66b65", codigo="10", nombre="UEB VUELTAS"),
        UnidadContable(pk="400d9e9f-4084-4214-a051-a1f78ea26b65", codigo="13", nombre="UEB SAGUA"),
        UnidadContable(pk="409f9e9f-4064-4214-a051-a1f78ea26b66", codigo="14", nombre="UEB ENCRUCIJADA"),
        UnidadContable(pk="26915d79-cf24-4374-b053-4fbeca66c96e", codigo="16", nombre="UEB CENTRO PROCESO DE CAPA"),
        UnidadContable(pk="409d9e9f-4064-4214-a051-a1f78ea36b65", codigo="19", nombre="UEB COMERCIALIZADORA",
                       is_comercializadora=True),
        UnidadContable(pk="809d9e9f-4064-4214-a051-a1f78ea26b65", codigo="21", nombre="DIRECCION DE EMPRESA",
                       is_empresa=True),
        UnidadContable(pk="889d9e9f-4064-4214-a051-a1f78ea26b65", codigo="22", nombre="UEB SANTO DOMINGO"),
        UnidadContable(pk="879d9e9f-4064-4214-a051-a1f78ea26b65", codigo="23", nombre="UEB JICOTEA"),
        UnidadContable(pk="57042ce6-b154-4663-88dd-507d79701504", codigo="24", nombre="UEB SERVICIOS",
                       activo=False),
    ]
    act_model_unidadcontable.objects.bulk_create(ucontab)

    confccelem = [
        ConfCentrosElementosOtros(pk=ChoiceConfCentrosElementosOtros.CENTROSCOSTO,
                                  clave=ChoiceConfCentrosElementosOtros.CHOICE_CONF_CC_ELEM_OTROS[
                                      ChoiceConfCentrosElementosOtros.CENTROSCOSTO]),
        ConfCentrosElementosOtros(pk=ChoiceConfCentrosElementosOtros.ELEMENTOSGASTO,
                                  clave=ChoiceConfCentrosElementosOtros.CHOICE_CONF_CC_ELEM_OTROS[
                                      ChoiceConfCentrosElementosOtros.ELEMENTOSGASTO]),
    ]
    act_model_confcentroselementosotros.objects.bulk_create(confccelem)
    act_model_confccelem_cc = ConfCentrosElementosOtros.objects.get(pk=ChoiceConfCentrosElementosOtros.CENTROSCOSTO)
    act_model_confccelem_eg = ConfCentrosElementosOtros.objects.get(pk=ChoiceConfCentrosElementosOtros.ELEMENTOSGASTO)
    confccelemdetalles = [
        ConfCentrosElementosOtrosDetalle(pk=1, clave=act_model_confccelem_cc, descripcion='Subproductos'),
        ConfCentrosElementosOtrosDetalle(pk=2, clave=act_model_confccelem_cc, descripcion='Defectuosos'),
        ConfCentrosElementosOtrosDetalle(pk=3, clave=act_model_confccelem_cc, descripcion='Rechazo'),
        ConfCentrosElementosOtrosDetalle(pk=4, clave=act_model_confccelem_cc, descripcion='Calidad'),
        ConfCentrosElementosOtrosDetalle(pk=5, clave=act_model_confccelem_cc, descripcion='Administración'),
        ConfCentrosElementosOtrosDetalle(pk=6, clave=act_model_confccelem_eg, descripcion='Traspasos de la Producción'),
        ConfCentrosElementosOtrosDetalle(pk=7, clave=act_model_confccelem_eg, descripcion='Traspasos de Rechazos'),
        ConfCentrosElementosOtrosDetalle(pk=8, clave=act_model_confccelem_eg, descripcion='Traspasos de Defectuosos'),
        ConfCentrosElementosOtrosDetalle(pk=9, clave=act_model_confccelem_eg,
                                         descripcion='Traspasos de Costos de Calidad'),
    ]
    act_model_confcentroselementosotrosdetalle.objects.bulk_create(confccelemdetalles)

    grupo_escala = [
        GrupoEscalaCargo(pk=1, grupo="I", salario=2100.00),
        GrupoEscalaCargo(pk=2, grupo="II", salario=2200.00),
        GrupoEscalaCargo(pk=3, grupo="III", salario=2300.00),
        GrupoEscalaCargo(pk=4, grupo="IV", salario=2420.00),
        GrupoEscalaCargo(pk=5, grupo="V", salario=2540.00),
        GrupoEscalaCargo(pk=6, grupo="VI", salario=2660.00),
        GrupoEscalaCargo(pk=7, grupo="VII", salario=2810.00),
        GrupoEscalaCargo(pk=8, grupo="VIII", salario=2960.00),
        GrupoEscalaCargo(pk=9, grupo="IX", salario=3110.00),
        GrupoEscalaCargo(pk=10, grupo="X", salario=3260.00),
        GrupoEscalaCargo(pk=11, grupo="XI", salario=3410.00),
        GrupoEscalaCargo(pk=12, grupo="XII", salario=3610.00),
        GrupoEscalaCargo(pk=13, grupo="XIII", salario=3810.00),
        GrupoEscalaCargo(pk=14, grupo="XIV", salario=4010.00),
        GrupoEscalaCargo(pk=15, grupo="XV", salario=4210.00),
        GrupoEscalaCargo(pk=16, grupo="XVI", salario=4410.00),
        GrupoEscalaCargo(pk=17, grupo="XVII", salario=4610.00),
        GrupoEscalaCargo(pk=18, grupo="XVIII", salario=4810.00),
        GrupoEscalaCargo(pk=19, grupo="XIX", salario=5060.00),
        GrupoEscalaCargo(pk=20, grupo="XX", salario=5310.00),
        GrupoEscalaCargo(pk=21, grupo="XXI", salario=5560.00),
        GrupoEscalaCargo(pk=22, grupo="XXII", salario=5810.00),
        GrupoEscalaCargo(pk=23, grupo="XXIII", salario=6060.00),
        GrupoEscalaCargo(pk=24, grupo="XXIV", salario=6310.00),
        GrupoEscalaCargo(pk=25, grupo="XXV", salario=6610.00),
        GrupoEscalaCargo(pk=26, grupo="XXVI", salario=6960.00),
        GrupoEscalaCargo(pk=27, grupo="XXVII", salario=7310.00),
        GrupoEscalaCargo(pk=28, grupo="XXVIII", salario=7660.00),
        GrupoEscalaCargo(pk=29, grupo="XXIX", salario=8010.00),
        GrupoEscalaCargo(pk=30, grupo="XXX", salario=8510.00),
        GrupoEscalaCargo(pk=31, grupo="XXXI", salario=9010.00),
        GrupoEscalaCargo(pk=32, grupo="XXXII", salario=9510.00),
    ]
    act_model_grupo_escala.objects.bulk_create(grupo_escala)

    parent = FichaCostoFilas.objects.create(fila='1', descripcion="Gasto Material", encabezado=True)
    FichaCostoFilas.objects.create(fila='1.1', descripcion="Materia Prima y Materiales", parent=parent,
                                   desglosado=True)
    FichaCostoFilas.objects.create(fila='1.2', descripcion="Gastos Materia Prima Tabaco", parent=parent,
                                   desglosado=True)
