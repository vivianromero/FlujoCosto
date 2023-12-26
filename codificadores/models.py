import uuid
from django.db import models
from django.db.models.functions import Now


class UnidadContable(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    codigo = models.CharField(unique=True, max_length=10)
    nombre = models.CharField(unique=True, max_length=30)
    activo = models.BooleanField(default=True)
    is_empresa = models.BooleanField(default=False)
    is_comercializadora = models.BooleanField(default=False)

    class Meta:
        db_table = 'cla_unidadcontable'
        ordering = ['codigo']

class Medida(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    clave = models.CharField(unique=True, max_length=6)
    descripcion = models.CharField(unique=True, max_length=50)

    class Meta:
        db_table = 'cla_medida'
        ordering = ['descripcion']

class MedidaConversion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    factor_conversion = models.DecimalField(max_digits=10, decimal_places=6, db_comment='Factor de conversión')
    medidao = models.ForeignKey(Medida, on_delete=models.CASCADE, related_name='medidaconversion_origen',
                                db_comment='Medida origen de la conversión')
    medidad = models.ForeignKey(Medida, on_delete=models.CASCADE, related_name='medidaconversion_destino',
                                db_comment='Medida destino de la conversión')

    class Meta:
        db_table = 'cla_medidaconversion'
        unique_together = (('medidao', 'medidad'),)
        ordering = ['medidao__descripcion']

class TipoProducto(models.Model):
    CHOICE_TIPOS_PROD = {
        1: "Pesada",
        2: "Materia Prima",
        3: "Habilitación",
        4: "Línea de Salida",
        5: "Vitola",
        6: "Subproducto",
        7: "Línea sin Terminar",
    }

    id = models.IntegerField(primary_key=True, choices=CHOICE_TIPOS_PROD, editable=False, )
    descripcion = models.CharField(unique=True, max_length=80)

    class Meta:
        db_table = 'cla_tipoproducto'

class EstadoProducto(models.Model):
    CHOICE_ESTADOS = {
        1: 'Bueno',
        2: 'Deficiente',
        3: 'Rechazo',
    }
    id = models.IntegerField(primary_key=True, choices=CHOICE_ESTADOS, editable=False, )
    descripcion = models.CharField(unique=True, max_length=80)

    class Meta:
        db_table = 'cla_estadoproducto'

class ClaseMateriaPrima(models.Model):
    CHOICE_CLASES = {
        1: 'Capote',
        2: 'F1',
        3: 'F2',
        4: 'F3',
        5: 'Capa Clasificada',
        6: 'Capa sin Clasificar',
        7: 'F3',
    }
    id = models.IntegerField(primary_key=True, choices=CHOICE_CLASES, editable=False, )
    descripcion = models.CharField(unique=True, max_length=80)
    capote_fortaleza = models.CharField(max_length=1)

    class Meta:
        db_table = 'cla_clasemateriaprima'
        ordering = ['descripcion']

class ProductoFlujo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    codigo = models.CharField(unique=True, max_length=125)
    descripcion = models.CharField(unique=True, max_length=125)
    activo = models.BooleanField(default=True)
    idmedida = models.ForeignKey(Medida, on_delete=models.PROTECT)
    idtipoproducto = models.ForeignKey(TipoProducto, on_delete=models.PROTECT, related_name='productoflujo_tipo')

    class Meta:
        db_table = 'cla_productoflujo'
        ordering = ['idtipoproducto', 'descripcion']

class ProductoFlujoClase(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    idclasemateriaprima = models.ForeignKey(ClaseMateriaPrima, on_delete=models.PROTECT)
    idproducto = models.ForeignKey(ProductoFlujo, on_delete=models.CASCADE, related_name='productoflujo_clase')

    class Meta:
        db_table = 'cla_productoflujoclase'

class CategoriaVitola(models.Model):
    CHOICE_CATEGORIAS = {
        5: 'IX',
        6: 'ND',
        7: 'V',
        8: 'VI',
        9: 'VII',
        10: 'VIII',
    }

    id = models.IntegerField(primary_key=True, choices=CHOICE_CATEGORIAS, editable=False, )
    descripcion = models.CharField(unique=True, max_length=50)
    orden = models.IntegerField(unique=True)

    class Meta:
        db_table = 'cla_categoriavitola'
        ordering = ['orden']

class TipoVitola(models.Model):
    CHOICE_TIPOS_VITOLA = {
        1: 'Picadura',
        2: 'Hoja',
    }

    id = models.IntegerField(primary_key=True, choices=CHOICE_TIPOS_VITOLA, editable=False, )
    descripcion = models.CharField(unique=True, max_length=50)

    class Meta:
        db_table = 'cla_tipovitola'

class Vitola(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    diametro = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    longitud = models.IntegerField(default=0)
    destino = models.CharField(max_length=1, choices={'C':'Consumo Nacional', 'E':'Exportación'})
    cepo = models.IntegerField(default=0)
    idcategoriavitola = models.ForeignKey(CategoriaVitola, on_delete=models.PROTECT, related_name='vitola_categotia')
    idproducto = models.ForeignKey(ProductoFlujo, on_delete=models.CASCADE)
    idtipovitola = models.ForeignKey(TipoVitola, on_delete=models.PROTECT, related_name='vitola_tipo')

    class Meta:
        db_table = 'cla_vitola'

class MarcaSalida(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    codigo = models.CharField(unique=True, max_length=5)
    descripcion = models.CharField(unique=True, max_length=128)

    class Meta:
        db_table = 'cla_marcasalida'
        ordering = ['descripcion']

class LineaSalida(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    envase = models.IntegerField(default=0)
    norma_embalaje = models.IntegerField(default=0)
    vol_cajam3 = models.DecimalField(max_digits=10, decimal_places=6, default=0.00)
    peso_bruto = models.DecimalField(max_digits=10, decimal_places=6, default=0.00)
    peso_neto = models.DecimalField(max_digits=10, decimal_places=6, default=0.00)
    peso_legal = models.DecimalField(max_digits=10, decimal_places=6, default=0.00)
    idmarcasalida = models.ForeignKey(MarcaSalida, on_delete=models.PROTECT, related_name='lineasalida_marcasalida')
    idproducto = models.ForeignKey(ProductoFlujo, on_delete=models.CASCADE, related_name='lineasalida_producto')
    idvitola = models.ForeignKey(ProductoFlujo, on_delete=models.PROTECT, related_name='lineasalida_vitola')

    class Meta:
        db_table = 'cla_lineasalida'

class CentroCosto(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    clave = models.CharField(unique=True, max_length=25)
    clavenivel = models.CharField(max_length=50)
    descripcion = models.CharField(unique=True, max_length=255)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = 'cla_centrocosto'
        ordering = ['descripcion']

class CuentaProceso(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    clave = models.CharField(unique=True, max_length=25)
    clavenivel = models.CharField(max_length=50)
    descripcion = models.CharField(unique=True, max_length=255)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = 'cla_cuentaproceso'
        ordering = ['descripcion']

class Departamento(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    codigo = models.CharField(unique=True, max_length=125)
    descripcion = models.CharField(unique=True, max_length=125)
    inicializado = models.BooleanField(default=False)
    idcentrocosto = models.ForeignKey(CentroCosto, on_delete=models.PROTECT, related_name='departamento_centrocosto')
    idunidadcontable = models.ManyToManyField(UnidadContable, related_name='departamento_unidadcontable')

    class Meta:
        db_table = 'cla_departamento'

class DepartamentoProductoSalida(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    iddepartamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)
    idtipoproducto = models.ForeignKey(TipoProducto, on_delete=models.PROTECT)

    class Meta:
        db_table = 'cla_departamentoproductosalida'

class DepartamentoRelacion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    iddepartamentoo = models.ForeignKey(Departamento, on_delete=models.CASCADE, related_name='departamento_origen')
    iddepartamentod = models.ForeignKey(Departamento, on_delete=models.CASCADE, related_name='departamento_destino')

    class Meta:
        db_table = 'cla_departamentorelacion'
        unique_together = (('iddepartamentoo', 'iddepartamentod'),)

class MotivoAjuste(models.Model):
    CHOICE_MOTIVOS = {
        1: 'Merma',
        2: 'Rotura',
        3: 'Promoción',
        4: 'SubProductos',
    }
    id = models.IntegerField(primary_key=True, choices=CHOICE_MOTIVOS, editable=False, )
    descripcion = models.CharField(unique=True, max_length=128)
    aumento = models.BooleanField(default=False, db_comment='Ajuste de aumento True en otro caso False')

    class Meta:
        db_table = 'cla_motivoajuste'
        ordering = ['aumento', 'descripcion']

class NormaConsumo(models.Model):
    CHOICE_TIPOS_NORMAS = {
        1: 'Pesada',
        2: 'Materia Prima',
        4: 'Línea de Salida',
        5: 'Vitola',
        7: 'Habilitados'
    }
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tipo = models.IntegerField(choices=CHOICE_TIPOS_NORMAS, editable=False,)
    cantidad = models.DecimalField(max_digits=18, decimal_places=6, default=0.00)
    activa = models.BooleanField(default=True)
    fecha_creada = models.DateTimeField(db_default=Now())
    fecha = models.DateField()
    idmedida = models.ForeignKey(Medida, on_delete=models.PROTECT)
    idproducto = models.ForeignKey(ProductoFlujo, models.PROTECT)

    class Meta:
        db_table = 'cla_normaconsumo'
        ordering = ['tipo', 'idproducto__descripcion']

class NormaconsumoDetalle(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    norma_ramal = models.DecimalField(max_digits=18, decimal_places=6, default=0.00)
    norma_empresarial = models.DecimalField(max_digits=18, decimal_places=6, default=0.00)
    operativo = models.BooleanField(default=False, db_comment='Si el producto es operativo o no')
    idnormaconsumo = models.ForeignKey(NormaConsumo, on_delete=models.CASCADE)
    idproducto = models.ForeignKey(ProductoFlujo, on_delete=models.PROTECT)
    idmedida = models.ForeignKey(Medida, on_delete=models.PROTECT)

    class Meta:
        db_table = 'cla_normaconsumodetalle'

class TipoDocumento(models.Model):
    CHOICE_TIPOS_DOC = {
        1: 'Entrada Desde Versat',
        2: 'Salida Hacia Versat',
        3: 'Transferencia Hacia Departamento',
        4: 'Transferencia Desde Departamento',
        5: 'Ajuste de Aumento',
        6: 'Ajuste de Disminución',
        8: 'Recepción de Producción',
        9: 'Devolución',
        10: 'Sobrante Sujeto a Investigación',
        12: 'Carga Inicial',
        13: 'Devolución Recibida',
        14: 'Cambio de Estado',
        15: 'Transferencia Externa',
        16: 'Recibir Transferencia Externa',
        17: 'Venta a Trabajadores',
        18: 'Reporte de SubProductos',
        19: 'Cambio de Producto',
    }

    id = models.IntegerField(primary_key=True, choices=CHOICE_TIPOS_DOC, editable=False, )
    descripcion = models.CharField(unique=True, max_length=128)
    operacion = models.CharField(max_length=1, db_comment='Operación de Entrada (E) o Salida (S)')

    class Meta:
        db_table = 'cla_tipodocumento'
        ordering = ['operacion', 'descripcion']

class NumeracionDocumentos(models.Model):
    tiponumeracion = models.CharField(unique=True, max_length=150)
    sistema = models.BooleanField(default=False, db_comment='Si es controlado por el sistema')
    departamento = models.BooleanField(default=False, db_comment='Si el número es por departamento')
    tipo_documento = models.BooleanField(default=False, db_comment='Si el número es por tipo de documento')

    class Meta:
        db_table = 'cla_numeraciondocumentos'

class FormatoCuentaProducto(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=30)
    separador = models.CharField(max_length=1)
    posicion = models.IntegerField()
    longitud = models.IntegerField()

    class Meta:
        db_table = 'cla_formatocuentaproducto'
