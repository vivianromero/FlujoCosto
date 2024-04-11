import uuid

from django.db import models
from django.db.models.functions import Now
from mptt.managers import TreeManager
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.translation import gettext_lazy as _
from bulk_update_or_create import BulkUpdateOrCreateQuerySet
from django.core.validators import MinValueValidator


class ObjectsManagerAbstract(models.Model):
    objects = BulkUpdateOrCreateQuerySet.as_manager()

    class Meta:
        abstract = True


# todas las unidades contables de la empresa
class UnidadContable(ObjectsManagerAbstract):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    codigo = models.CharField(unique=True, max_length=10, verbose_name=_("Code"))
    nombre = models.CharField(unique=True, max_length=30, verbose_name=_("Name"))
    activo = models.BooleanField(default=True, verbose_name=_("Active"))
    is_empresa = models.BooleanField(default=False, verbose_name=_("Is Company"))
    is_comercializadora = models.BooleanField(default=False, verbose_name=_("Is Commercial"))

    class Meta:
        db_table = 'cla_unidadcontable'
        indexes = [
            models.Index(
                fields=[
                    'codigo',
                ]
            ),
        ]
        ordering = ['codigo']
        verbose_name_plural = _('UEBs')
        verbose_name = _('UEB')

    def __str__(self):
        return "%s | %s" % (self.codigo, self.nombre)


class Medida(ObjectsManagerAbstract):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    clave = models.CharField(unique=True, max_length=6, verbose_name=_("Key"))
    descripcion = models.CharField(unique=True, max_length=50, verbose_name=_("Description"))
    activa = models.BooleanField(default=True, verbose_name=_("Active"))

    class Meta:
        db_table = 'cla_medida'
        indexes = [
            models.Index(
                fields=[
                    'clave',
                    'descripcion',
                ]
            ),
        ]
        ordering = ['clave', 'descripcion']
        verbose_name_plural = _('Measurement units')
        verbose_name = _('Unit of measurement')

    def __str__(self):
        return "%s | %s" % (self.clave, self.descripcion)


class MedidaConversion(ObjectsManagerAbstract):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    factor_conversion = models.DecimalField(max_digits=10, decimal_places=6, db_comment='Factor de conversión',
                                            verbose_name=_("Convertion Factor"),
                                            validators=[MinValueValidator(0.000001, message=_(
                                                'The value must be greater than 0'))])
    medidao = models.ForeignKey(Medida, on_delete=models.CASCADE, related_name='medidaconversion_origen',
                                db_comment='Medida origen de la conversión',
                                verbose_name=_("Origin Measure"))
    medidad = models.ForeignKey(Medida, on_delete=models.CASCADE, related_name='medidaconversion_destino',
                                db_comment='Medida destino de la conversión',
                                verbose_name=_("Destination Measure"))

    class Meta:
        db_table = 'cla_medidaconversion'
        indexes = [
            models.Index(
                fields=[
                    'medidao',
                    'medidad',
                ]
            ),
        ]
        unique_together = (('medidao', 'medidad'),)
        ordering = ['medidao__descripcion']
        verbose_name_plural = _('Convert measurement units')
        verbose_name = _('Convert unit of measurement')

    def __str__(self):
        return "%s | %s" % (self.medidao, self.medidad)


class Cuenta(MPTTModel, ObjectsManagerAbstract):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    long_niv = models.IntegerField()
    posicion = models.IntegerField()
    clave = models.CharField(unique=True, max_length=100)
    clavenivel = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=1000, verbose_name=_("Description"))
    activa = models.BooleanField(default=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    objects = models.Manager()
    tree = TreeManager()

    class Meta:
        db_table = 'cla_cuenta'
        indexes = [
            models.Index(
                fields=[
                    'clave',
                ]
            ),
        ]
        ordering = ['clave', 'posicion']
        verbose_name_plural = _('Accounts')
        verbose_name = _('Account')

    def __str__(self):
        return self.descripcion


class CentroCosto(ObjectsManagerAbstract):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    clave = models.CharField(unique=True, max_length=50, verbose_name=_("Code"))
    descripcion = models.CharField(unique=True, max_length=255,
                                   verbose_name=_("Description"))
    activo = models.BooleanField(default=True, verbose_name=_("Active"))

    class Meta:
        db_table = 'cla_centrocosto'
        indexes = [
            models.Index(
                fields=[
                    'clave','descripcion'
                ]
            ),
        ]
        ordering = ['descripcion', 'clave']
        verbose_name_plural = _('Centers of cost')
        verbose_name = _('Cost center')

    def __str__(self):
        return "%s | %s" % (self.clave, self.descripcion)


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

    id = models.AutoField(primary_key=True, choices=CHOICE_TIPOS_PROD, editable=False, )
    descripcion = models.CharField(unique=True, max_length=80)

    class Meta:
        db_table = 'cla_tipoproducto'

    def __str__(self):
        return self.CHOICE_TIPOS_PROD[self.id]


class EstadoProducto(models.Model):
    CHOICE_ESTADOS = {
        1: 'Bueno',
        2: 'Deficiente',
        3: 'Rechazo',
    }
    id = models.AutoField(primary_key=True, choices=CHOICE_ESTADOS, editable=False, )
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
        7: 'F4',
    }
    id = models.AutoField(primary_key=True, choices=CHOICE_CLASES, editable=False, )
    descripcion = models.CharField(unique=True, max_length=80)
    capote_fortaleza = models.CharField(max_length=1)

    class Meta:
        db_table = 'cla_clasemateriaprima'
        ordering = ['descripcion']

    def __str__(self):
        return self.descripcion


class ProductoFlujo(ObjectsManagerAbstract):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    codigo = models.CharField(unique=True, max_length=125, verbose_name=_("Code"))
    descripcion = models.CharField(unique=True, max_length=125, verbose_name=_("Description"))
    activo = models.BooleanField(default=True, verbose_name=_("Active"))
    medida = models.ForeignKey(Medida, on_delete=models.PROTECT, related_name='productoflujo_medida',
                                 verbose_name="U.M")
    tipoproducto = models.ForeignKey(TipoProducto, on_delete=models.PROTECT, related_name='productoflujo_tipo',
                                       verbose_name=_("Product Type"))

    class Meta:
        db_table = 'cla_productoflujo'
        ordering = ['tipoproducto', 'descripcion']

    @property
    def get_clasemateriaprima(self):
        return None if self.tipoproducto.pk != 2 else self.productoflujoclase_producto.get().clasemateriaprima


class ProductoFlujoClase(ObjectsManagerAbstract):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    clasemateriaprima = models.ForeignKey(ClaseMateriaPrima, on_delete=models.PROTECT,
                                            related_name='productosflujoclase_clasemateriaprima')
    producto = models.ForeignKey(ProductoFlujo, on_delete=models.CASCADE, related_name='productoflujoclase_producto')

    class Meta:
        db_table = 'cla_productoflujoclase'


class ProductoFlujoVitola(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    producto = models.ForeignKey(ProductoFlujo, on_delete=models.CASCADE, related_name='productoflujovitola_producto')
    vitola = models.ForeignKey(ProductoFlujo, on_delete=models.CASCADE, related_name='productoflujovitola_vitola')

    class Meta:
        db_table = 'cla_productoflujovitola'


class ProductoFlujoDestino(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    destino = models.CharField(max_length=1, choices={'C': 'Consumo Nacional', 'E': 'Exportación'},
                               verbose_name=_("Destination"))
    producto = models.ForeignKey(ProductoFlujo, on_delete=models.CASCADE,
                                   related_name='productoflujodestino_producto')

    class Meta:
        db_table = 'cla_productoflujodestino'


class ProductoFlujoCuenta(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cuenta = models.ForeignKey(Cuenta, on_delete=models.PROTECT, related_name='productoflujocuenta_cuenta')
    producto = models.ForeignKey(ProductoFlujo, on_delete=models.CASCADE, related_name='productoflujocuenta_producto')

    class Meta:
        db_table = 'cla_productoflujocuenta'


class CategoriaVitola(models.Model):
    CHOICE_CATEGORIAS = {
        5: 'IX',
        6: 'ND',
        7: 'V',
        8: 'VI',
        9: 'VII',
        10: 'VIII',
    }

    id = models.AutoField(primary_key=True, choices=CHOICE_CATEGORIAS, editable=False, )
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

    id = models.AutoField(primary_key=True, choices=CHOICE_TIPOS_VITOLA, editable=False, )
    descripcion = models.CharField(unique=True, max_length=50)

    class Meta:
        db_table = 'cla_tipovitola'


class Vitola(ObjectsManagerAbstract):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    diametro = models.DecimalField(max_digits=10, decimal_places=2, default=0.00,
                                   verbose_name=_("Diameter"))
    longitud = models.IntegerField(default=0, verbose_name=_("Length"))
    destino = models.CharField(max_length=1, choices={'C': 'Consumo Nacional', 'E': 'Exportación'},
                               verbose_name=_("Destination"))
    cepo = models.IntegerField(default=0)
    categoriavitola = models.ForeignKey(CategoriaVitola, on_delete=models.PROTECT, related_name='vitola_categotia')
    producto = models.ForeignKey(ProductoFlujo, on_delete=models.CASCADE, related_name='vitola_producto')
    tipovitola = models.ForeignKey(TipoVitola, on_delete=models.PROTECT, related_name='vitola_tipo',
                                     verbose_name=_("Type"))

    class Meta:
        db_table = 'cla_vitola'


class MarcaSalida(ObjectsManagerAbstract):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    codigo = models.CharField(unique=True, max_length=5, verbose_name=_("Code"))
    descripcion = models.CharField(unique=True, max_length=128, verbose_name=_("Description"))
    activa = models.BooleanField(default=True, verbose_name=_("Active"))

    class Meta:
        db_table = 'cla_marcasalida'
        ordering = ['descripcion']


class LineaSalida(ObjectsManagerAbstract):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    envase = models.IntegerField(default=0, verbose_name=_("Package"))
    norma_embalaje = models.IntegerField(default=0,
                                         verbose_name=_("Packaging Standard"))
    vol_cajam3 = models.DecimalField(max_digits=10, decimal_places=6, default=0.00,
                                     verbose_name=_("Box Volume M3"))
    peso_bruto = models.DecimalField(max_digits=10, decimal_places=6, default=0.00,
                                     verbose_name=_("Gross Weight"))
    peso_neto = models.DecimalField(max_digits=10, decimal_places=6, default=0.00,
                                    verbose_name=_("Net Weight"))
    peso_legal = models.DecimalField(max_digits=10, decimal_places=6, default=0.00,
                                     verbose_name=_("Legal Weight"))
    marcasalida = models.ForeignKey(MarcaSalida, on_delete=models.PROTECT, related_name='lineasalida_marcasalida',
                                      verbose_name=_("Starting Mark"))
    producto = models.ForeignKey(ProductoFlujo, on_delete=models.CASCADE, related_name='lineasalida_producto')
    vitola = models.ForeignKey(ProductoFlujo, on_delete=models.PROTECT, related_name='lineasalida_vitola',
                                 verbose_name="Vitola")

    class Meta:
        db_table = 'cla_lineasalida'


class Departamento(ObjectsManagerAbstract):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    codigo = models.CharField(unique=True, max_length=125, verbose_name=_("Code"))
    descripcion = models.CharField(unique=True, max_length=125, verbose_name=_("Description"))
    inicializado = models.BooleanField(default=False)
    centrocosto = models.ForeignKey(CentroCosto, on_delete=models.PROTECT, related_name='departamento_centrocosto',
                                      verbose_name=_("Cost Center"))
    unidadcontable = models.ManyToManyField(UnidadContable, related_name='departamento_unidadcontable',
                                              verbose_name="UEB")

    relaciondepartamento = models.ManyToManyField('self',
                                                  blank=True, null=True,
                                                  related_name='departamentorelacion_destino',
                                                  verbose_name=_("Destination Department"))
    departamentoproducto = models.ManyToManyField(TipoProducto,
                                                  blank=True, null=True,
                                                  related_name='departamentoproductosalida_producto',
                                                  verbose_name=_("Output Product"))

    class Meta:
        db_table = 'cla_departamento'
        ordering = ('codigo',)
        indexes = [
            models.Index(
                fields=[
                    'codigo',
                    'descripcion',
                    'centrocosto'
                ]
            ),
        ]
        ordering = ['codigo']
        verbose_name_plural = _('Departments')
        verbose_name = _('Department')

    def __str__(self):
        return self.descripcion


class NormaConsumo(ObjectsManagerAbstract):
    CHOICE_TIPOS_NORMAS = {
        1: 'Pesada',
        2: 'Materia Prima',
        4: 'Línea de Salida',
        5: 'Vitola',
        7: 'Habilitados'
    }
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tipo = models.IntegerField(choices=CHOICE_TIPOS_NORMAS, editable=False, verbose_name=_("Type"))
    cantidad = models.DecimalField(max_digits=18, decimal_places=6, default=0.00,
                                   verbose_name=_("Quantity"))
    activa = models.BooleanField(default=True, verbose_name=_("Active"))
    fecha_creacion = models.DateTimeField(db_default=Now(), verbose_name=_("Crate at"))
    fecha = models.DateField(verbose_name=_("Date"))
    medida = models.ForeignKey(Medida, on_delete=models.PROTECT, related_name='normaconsumo_medida',
                                 verbose_name="U.M")
    producto = models.ForeignKey(ProductoFlujo, models.PROTECT, related_name='normaconsumo_producto',
                                   verbose_name=_("Product"))

    class Meta:
        db_table = 'cla_normaconsumo'
        ordering = ['tipo', 'producto__descripcion']


class NormaconsumoDetalle(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    norma_ramal = models.DecimalField(max_digits=18, decimal_places=6, default=0.00,
                                      verbose_name=_("Ramal Norm"))
    norma_empresarial = models.DecimalField(max_digits=18, decimal_places=6, default=0.00,
                                            verbose_name=_("Enterprise Norm"))
    operativo = models.BooleanField(default=False, db_comment='Si el producto es operativo o no',
                                    verbose_name=_("Operational"))
    normaconsumo = models.ForeignKey(NormaConsumo, on_delete=models.CASCADE,
                                       related_name='normaconsumodetalle_normaconsumo')
    producto = models.ForeignKey(ProductoFlujo, on_delete=models.PROTECT, related_name='normaconsumodetalle_producto',
                                   verbose_name=_("Product"))
    medida = models.ForeignKey(Medida, on_delete=models.PROTECT, related_name='normaconsumodetalle_medida',
                                 verbose_name="U.M")

    class Meta:
        db_table = 'cla_normaconsumodetalle'


class MotivoAjuste(ObjectsManagerAbstract):
    CHOICE_MOTIVOS = {
        1: 'Merma',
        2: 'Rotura',
        3: 'Promoción',
        4: 'SubProductos',
    }
    id = models.AutoField(primary_key=True, choices=CHOICE_MOTIVOS, editable=False, )
    descripcion = models.CharField(unique=True, max_length=128, verbose_name=_("Description"))
    aumento = models.BooleanField(default=False, db_comment='Ajuste de aumento True en otro caso False',
                                  verbose_name=_("Increase"))
    activo = models.BooleanField(default=True, verbose_name=_("Active"))

    class Meta:
        db_table = 'cla_motivoajuste'
        ordering = ['aumento', 'descripcion']


class TipoDocumento(models.Model):
    CHOICE_TIPOS_DOC = {
        1: 'Entrada Desde Versat',
        2: 'Salida Hacia Versat',
        3: 'Transferencia Hacia Departamento',
        4: 'Transferencia Desde Departamento',
        5: 'Ajuste de Aumento',
        6: 'Ajuste de Disminución',
        7: 'Recepción de Producción de Reproceso',
        8: 'Recepción de Producción',
        9: 'Devolución',
        10: 'Sobrante Sujeto a Investigación',
        11: 'Recepción de Rechazo',
        12: 'Carga Inicial',
        13: 'Devolución Recibida',
        14: 'Cambio de Estado',
        15: 'Transferencia Externa',
        16: 'Recibir Transferencia Externa',
        17: 'Venta a Trabajadores',
        18: 'Reporte de SubProductos',
        19: 'Cambio de Producto',
    }

    id = models.AutoField(primary_key=True, choices=CHOICE_TIPOS_DOC, editable=False, )
    descripcion = models.CharField(unique=True, max_length=128)
    operacion = models.CharField(max_length=1, db_comment='Operación de Entrada (E) o Salida (S)')
    generado = models.BooleanField(default=False, db_comment='Si se genera automáticamente',
                                   verbose_name=_("Generado"))

    class Meta:
        db_table = 'cla_tipodocumento'
        ordering = ['operacion', 'descripcion']


class NumeracionDocumentos(ObjectsManagerAbstract):
    CHOICE_TIPO_NUMERO = {
        1: 'Número Consecutivo',
        2: 'Número de Control',
    }

    tiponumeracion = models.CharField(unique=True, max_length=150, choices=CHOICE_TIPO_NUMERO,
                                      verbose_name=_("Enumeration Type"))
    sistema = models.BooleanField(default=False, db_comment='Si es controlado por el sistema',
                                  verbose_name=_("System"))
    departamento = models.BooleanField(default=False, db_comment='Si el número es por departamento',
                                       verbose_name=_("Department"))
    tipo_documento = models.BooleanField(default=False, db_comment='Si el número es por tipo de documento',
                                         verbose_name=_("Document Type"))
    prefijo = models.CharField(max_length=3, blank=True, null=True,
                               db_comment='Si el número de documento va a contener un prefijo',
                               verbose_name=_("Prefix"))

    class Meta:
        db_table = 'cla_numeraciondocumentos'


# Documento que se va a configurar la cuenta para su contabilizacion
class TipoDocumentoCuentaAbstract(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    documento = models.ForeignKey(TipoDocumento, on_delete=models.CASCADE,
                                    verbose_name=_("Document Type"))

    class Meta:
        abstract = True


# Se configura la cuenta de los documentos que la llevan,
# Venta a Trabajadores
# Ajuste de Disminución
# Tranf entre departamentos
class TipoDocumentoCuenta(TipoDocumentoCuentaAbstract):
    cuenta_debe_exp = models.ForeignKey(Cuenta, on_delete=models.CASCADE,
                                          related_name='tipodocumentocuenta_cuenta_debe_exp',
                                          verbose_name=_("Debit Count Exp"))
    cuenta_debe_cn = models.ForeignKey(Cuenta, on_delete=models.CASCADE,
                                         related_name='tipodocumentocuenta_cuenta_debe_cn',
                                         verbose_name=_("Debit Count CN"))
    cuenta_haber_exp = models.ForeignKey(Cuenta, on_delete=models.CASCADE,
                                           related_name='tipodocumentocuenta_cuenta_haber_exp',
                                           verbose_name=_("Credit Count Exp"))
    cuenta_haber_cn = models.ForeignKey(Cuenta, on_delete=models.CASCADE,
                                          related_name='tipodocumentocuenta_cuenta_haber_cn',
                                          verbose_name=_("Credit Count CN"))

    class Meta:
        db_table = 'cla_tipodocumentocuenta'


# Se va a configurar por unidad contable y los departamentos de la unidad contable
class TipoDocumentoCuentaTransfExterna(TipoDocumentoCuentaAbstract):
    unidadcontable = models.ForeignKey(UnidadContable, on_delete=models.PROTECT,
                                         related_name='tipodocumentocuentatransfexterna_unidadcontable',
                                         db_comment='Esta es la unidad contable para la que se va a configurar el documento',
                                         verbose_name="UEB")
    departamento = models.ForeignKey(Departamento, on_delete=models.PROTECT,
                                       db_comment='Dpto de la unidad contable para la que se va a configurar el documento',
                                       related_name='tipodocumentocuentatransfexterna_departamento',
                                       verbose_name=_("Department"))

    class Meta:
        db_table = 'cla_tipodocumentocuentatransfexterna'

# se configura la cuenta por unidad contable que realiza o recibe la transf.
# en dependencia del tipo de documento
class TipoDocumentoCuentaTransfExternaUEB(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    idtipodocumentocuentatransfexterna = models.ForeignKey(TipoDocumentoCuentaTransfExterna, on_delete=models.CASCADE,
                                                           related_name='tipodocumentocuentatransfexternadpto_ipodocumentocuentatransfexterna')
    unidadcontable = models.ForeignKey(UnidadContable, on_delete=models.PROTECT,
                                         related_name='tipodocumentocuentatransfexternadpto_unidadcontable',
                                         db_comment='Unidad contab que recibe o envía la transf, según el tipo de documento')
    cuenta_debe_exp = models.ForeignKey(Cuenta, on_delete=models.CASCADE,
                                          related_name='tipodocumentocuentatransfexternadpto_cuenta_debe_exp')
    cuenta_debe_cn = models.ForeignKey(Cuenta, on_delete=models.CASCADE,
                                         related_name='tipodocumentocuentatransfexternadpto_cuenta_debe_cn')
    cuenta_haber_exp = models.ForeignKey(Cuenta, on_delete=models.CASCADE,
                                           related_name='tipodocumentocuentatransfexternadpto_cuenta_haber_exp')
    cuenta_haber_cn = models.ForeignKey(Cuenta, on_delete=models.CASCADE,
                                          related_name='tipodocumentocuentatransfexternadpto_cuenta_haber_cn')

    class Meta:
        db_table = 'cla_tipodocumentocuentatransfexternaueb'


# Formato del versat para las cuentas y código de los productos
class FormatoCuentaProducto(ObjectsManagerAbstract):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=30)
    separador = models.CharField(max_length=1)
    posicion = models.IntegerField()
    longitud = models.IntegerField()
    enuso = models.BooleanField(default=True)


class Meta:
    db_table = 'cla_formatocuentaproducto'
    ordering = ['nombre', 'posicion']


class CambioProducto(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    productoo = models.ForeignKey(ProductoFlujo, on_delete=models.CASCADE, related_name='productoflujo_origen',
                                  verbose_name=_("Origin Product"))
    productod = models.ForeignKey(ProductoFlujo, on_delete=models.CASCADE, related_name='productoflujo_destino',
                                  verbose_name=_("Destination Product"))

    class Meta:
        db_table = 'cla_cambioproducto'
        unique_together = (('productoo', 'productod'),)
        ordering = ['productoo__descripcion']
