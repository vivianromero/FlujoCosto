class ChoiceTiposProd:
    PESADA = 1
    MATERIAPRIMA = 2
    HABILITACIONES = 3
    LINEASALIDA = 4
    VITOLA = 5
    SUBPRODUCTO = 6
    LINEASINTERMINAR = 7

    CHOICE_TIPOS_PROD = {
        PESADA: "Pesada",
        MATERIAPRIMA: "Materia Prima",
        HABILITACIONES: "Habilitación",
        LINEASALIDA: "Línea de Salida",
        VITOLA: "Vitola",
        SUBPRODUCTO: "Subproducto",
        LINEASINTERMINAR: "Línea sin Terminar",
    }

class ChoiceEstadosProd:
    BUENO = 1
    DEFICIENTE = 2
    RECHAZO = 3
    CHOICE_ESTADOS = {
        BUENO: 'Bueno',
        DEFICIENTE: 'Deficiente',
        RECHAZO: 'Rechazo',
    }

class ChoiceClasesMatPrima:
    CAPOTE = 1
    F1 = 2
    F2 = 3
    F3 = 4
    F4 = 7
    CAPACLASIFICADA = 5
    CAPASINCLASIFICAR = 6

    CHOICE_CLASES = {
        CAPOTE: 'Capote',
        F1: 'F1',
        F2: 'F2',
        F3: 'F3',
        F4: 'F4',
        CAPACLASIFICADA: 'Capa Clasificada',
        CAPASINCLASIFICAR: 'Capa sin Clasificar',
    }

class ChoiceDestinos:
    CONSUMONACIONAL = 'C'
    EXPORTACION = 'E'

    CHOICE_DESTINOS = {CONSUMONACIONAL: 'Consumo Nacional',
                       EXPORTACION: 'Exportación'}

class ChoiceCategoriasVit:
    V = 7
    VI = 8
    VII = 9
    VIII = 10
    IX = 5

    CHOICE_CATEGORIAS = {
        V: 'V',
        VI: 'VI',
        VII: 'VII',
        VIII: 'VIII',
        IX: 'IX',
    }

class ChoiceTiposVitola:
    PICADURA = 1
    HOJA = 2

    CHOICE_TIPOS_VITOLA = {
        1: 'Picadura',
        2: 'Hoja',
    }

class ChoiceTiposNormas:
    PESADA = 1
    MATERIAPRIMA = 2
    LINEASALIDA = 4
    VITOLA = 5
    HABILITADOS = 7

    CHOICE_TIPOS_NORMAS = {
        PESADA: 'Pesada',
        MATERIAPRIMA: 'Materia Prima',
        LINEASALIDA: 'Línea de Salida',
        VITOLA: 'Vitola',
        HABILITADOS: 'Habilitados'
    }

class ChoiceMotivosAjuste:
    MERMA = 1
    ROTURA = 2
    PROMOCION = 3
    SUBPRODUCTOS = 4

    CHOICE_MOTIVOS_AJUSTE = {
        MERMA: 'Merma',
        ROTURA: 'Rotura',
        PROMOCION: 'Promoción',
        SUBPRODUCTOS: 'SubProductos',
    }

class ChoiceTiposDoc:
    ENTRADA_DESDE_VERSAT = 1
    SALIDA_HACIA_VERSAT = 2
    TRANSF_HACIA_DPTO = 3
    TRANSF_DESDE_DPTO = 4
    AJUSTE_AUMENTO = 5
    AJUSTE_DISMINUCION = 6
    RECEPCION_PRODUCCION_REPROCESO = 7
    RECEPCION_PRODUCCION = 8
    DEVOLUCION = 9
    SOBRANTE_SUJETO_INVESTIGACION = 10
    RECEPCION_RECHAZO = 11
    CARGA_INICIAL = 12
    DEVOLUCION_RECIBIDA = 13
    CAMBIO_ESTADO = 14
    TRANSFERENCIA_EXTERNA = 15
    RECIBIR_TRANS_EXTERNA = 16
    VENTA_TRABAJADORES = 17
    REPORTE_SUBPRODUCTOS = 18
    CAMBIO_PRODUCTO = 19

    CHOICE_TIPOS_DOC = {
        ENTRADA_DESDE_VERSAT: 'Entrada Desde Versat',
        SALIDA_HACIA_VERSAT: 'Salida Hacia Versat',
        TRANSF_HACIA_DPTO: 'Transferencia Hacia Departamento',
        TRANSF_DESDE_DPTO: 'Transferencia Desde Departamento',
        AJUSTE_AUMENTO: 'Ajuste de Aumento',
        AJUSTE_DISMINUCION: 'Ajuste de Disminución',
        RECEPCION_PRODUCCION_REPROCESO: 'Recepción de Producción de Reproceso',
        RECEPCION_PRODUCCION: 'Recepción de Producción',
        DEVOLUCION: 'Devolución',
        SOBRANTE_SUJETO_INVESTIGACION: 'Sobrante Sujeto a Investigación',
        RECEPCION_RECHAZO: 'Recepción de Rechazo',
        CARGA_INICIAL: 'Carga Inicial',
        DEVOLUCION_RECIBIDA: 'Devolución Recibida',
        CAMBIO_ESTADO: 'Cambio de Estado',
        TRANSFERENCIA_EXTERNA: 'Transferencia Externa',
        RECIBIR_TRANS_EXTERNA: 'Recibir Transferencia Externa',
        VENTA_TRABAJADORES: 'Venta a Trabajadores',
        REPORTE_SUBPRODUCTOS: 'Reporte de SubProductos',
        CAMBIO_PRODUCTO: 'Cambio de Producto',
    }

class ChoiceTipoNumeroDoc:
    NUMERO_CONSECUTIVO = 1
    NUMERO_CONTROL = 2

    CHOICE_TIPO_NUMERO_DOC = {
        NUMERO_CONSECUTIVO: 'Número Consecutivo',
        NUMERO_CONTROL: 'Número de Control',
    }