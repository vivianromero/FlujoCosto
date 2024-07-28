import uuid

from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Q
from django.db.models.functions import Now
from django.utils.translation import gettext_lazy as _
from django_choices_field import IntegerChoicesField

from codificadores.models import UnidadContable, Departamento, TipoDocumento, MotivoAjuste, EstadoProducto, \
    ProductoFlujo, ConfigNumero, ObjectsManagerAbstract, OperacionDocumento, TipoNumeroDoc
from cruds_adminlte3.utils import crud_url


class EstadosDocumentos(models.IntegerChoices):
    EDICION = 1, 'Edición'
    CONFIRMADO = 2, 'Confirmado'
    RECHAZADO = 3, 'Rechazado'
    CANCELADO = 4, 'Cancelado'
    ERRORES = 5, 'Con Errores'


class Documento(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fecha = models.DateField(verbose_name=_("Date"))
    fecha_creacion = models.DateTimeField(db_default=Now(), verbose_name=_("Create at"))
    numerocontrol = models.CharField(max_length=50, verbose_name=_("Control Number"))
    numeroconsecutivo = models.IntegerField(verbose_name=_("Consecutive Number"))
    suma_importe = models.DecimalField(max_digits=18, decimal_places=2, default=0.00, verbose_name=_("Amount"))
    observaciones = models.TextField(blank=True, null=True, verbose_name=_("Observations"))
    estado = IntegerChoicesField(choices_enum=EstadosDocumentos,
                                 db_comment="Estado del documento 1:Edición, 2:Confirmado, 3:Rechazado",
                                 verbose_name=_("Status"), default=EstadosDocumentos.EDICION)
    reproceso = models.BooleanField(default=False, verbose_name=_("Reprocessing"))
    editar_nc = models.BooleanField(default=False)
    comprob = models.CharField(max_length=150, blank=True, null=True)
    departamento = models.ForeignKey(Departamento, on_delete=models.PROTECT, related_name='documento_departamento')
    tipodocumento = models.ForeignKey(TipoDocumento, on_delete=models.PROTECT, related_name='documento_tipodocumento')
    anno = models.IntegerField(default=0)
    mes = models.IntegerField(default=0)
    confconsec = IntegerChoicesField(choices_enum=ConfigNumero,
                                     db_comment="Para guardar el tipo de conf para el consecutivo y poder establecer la constarint",
                                     default=ConfigNumero.DEPARTAMENTO)
    confcontrol = IntegerChoicesField(choices_enum=ConfigNumero,
                                      db_comment="Para guardar el tipo de conf para el numero de control y poder establecer la constarint",
                                      default=ConfigNumero.DEPARTAMENTO)
    error = models.BooleanField(default=False, verbose_name=_("Error"))
    ueb = models.ForeignKey(UnidadContable, on_delete=models.PROTECT, related_name='documento_ueb')

    class Meta:
        db_table = 'fp_documento'
        constraints = [
            models.UniqueConstraint(
                fields=['numeroconsecutivo', 'departamento', 'mes', 'anno', 'ueb'],
                condition=Q(confconsec=ConfigNumero.DEPARTAMENTO),
                name='unique_numeroconsecutivo_departamento_tipodocumento'
            ),
            models.UniqueConstraint(
                fields=['numeroconsecutivo', 'mes', 'anno', 'ueb'],
                condition=Q(confconsec=ConfigNumero.UNICO),
                name='unique_numeroconsecutivo_ueb'
            ),
            models.UniqueConstraint(
                fields=['numerocontrol', 'departamento', 'anno', 'ueb'],
                condition=Q(confcontrol=ConfigNumero.DEPARTAMENTO),
                name='unique_numerocontrol_departamento'
            ),
            models.UniqueConstraint(
                fields=['numerocontrol', 'anno', 'ueb'],
                condition=Q(confcontrol=ConfigNumero.UNICO),
                name='unique_numerocontrol_ueb'
            ),
        ]
        ordering = ['ueb', 'departamento', '-numeroconsecutivo', 'tipodocumento']

    def __str__(self):
        return self.tipodocumento.descripcion if self.numeroconsecutivo else ''

    def get_absolute_url(self):
        return crud_url(self, 'update', namespace='app_index:flujo')

    def get_numerocontrol(self):
        nros = self.numerocontrol.split('/')
        return int(nros[len(nros) - 1])

    def get_numerocontrol_prefijo(self):
        return '' if not '/' in self.numerocontrol else self.numerocontrol.split('/')[0]

    @property
    def operacion(self):
        return 1 if self.tipodocumento.operacion == OperacionDocumento.ENTRADA else -1


class DocumentoDetalle(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cantidad = models.DecimalField(max_digits=18, decimal_places=4, default=0.00,
                                   verbose_name=_("Quantity"),
                                   validators=[MinValueValidator(0.0001, message=_(
                                       'El valor debe ser >= 0'))]
                                   )
    precio = models.DecimalField(max_digits=18, decimal_places=7, default=0.00,
                                 verbose_name=_("Price"),
                                 validators=[MinValueValidator(0.0000001, message=_(
                                     'El valor debe ser >= 0'))]
                                 )
    importe = models.DecimalField(max_digits=18, decimal_places=2, default=0.00,
                                  verbose_name=_("Amount"))
    existencia = models.DecimalField(max_digits=18, decimal_places=4, default=0.00,
                                     verbose_name=_("Existence"))
    documento = models.ForeignKey(Documento, on_delete=models.CASCADE, related_name='documentodetalle_documento')
    estado = IntegerChoicesField(choices_enum=EstadoProducto, verbose_name=_("Status"))
    producto = models.ForeignKey(ProductoFlujo, on_delete=models.PROTECT, related_name='documentodetalle_producto',
                                 verbose_name=_("Product"))
    error = models.BooleanField(default=False, verbose_name=_("Error"))

    class Meta:
        db_table = 'fp_documentodetalle'

        constraints = [
            models.UniqueConstraint(
                fields=['documento', 'estado', 'producto'],
                name='unique_documentodetalle_documento_estado_producto'
            )
        ]

    def __str__(self):
        return "%s | %s" % (self.producto.codigo, self.producto.descripcion) if self.cantidad else ''


class DocumentoAjuste(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    documento = models.ForeignKey(Documento, on_delete=models.PROTECT, related_name='documentoajuste_documento')
    motivoajuste = models.ForeignKey(MotivoAjuste, on_delete=models.PROTECT, related_name='documentoajuste_motivo',
                                     verbose_name=_("Adjustment Reason"))

    class Meta:
        db_table = 'fp_documentoajuste'


class DocumentoTransfDepartamento(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    documento = models.ForeignKey(Documento, on_delete=models.CASCADE,
                                  related_name='documentotransfdepartamento_documento')
    departamento = models.ForeignKey(Departamento, on_delete=models.PROTECT,
                                     related_name='documentotransfdepartamento_departamento',
                                     verbose_name=_("Department"))

    class Meta:
        db_table = 'fp_documentotransfdepartamento'


# esto es el detalle de la transf hacia departamento PARA EL DEPARTAMENTO DE CONTROL TECNICO
# se genera la transf hacia departamento con los buenos, suma de los defectuosos y prueba sensorial
class DocumentoDetalleTransfDptoControlTecnico(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cantidad = models.DecimalField(max_digits=18, decimal_places=4, default=0.00,
                                   verbose_name=_("Quantity")
                                   )
    precio = models.DecimalField(max_digits=18, decimal_places=7, default=0.00,
                                 verbose_name=_("Price")
                                 )
    importe = models.DecimalField(max_digits=18, decimal_places=2, default=0.00,
                                  verbose_name=_("Amount"))
    existencia = models.DecimalField(max_digits=18, decimal_places=4, default=0.00,
                                     verbose_name=_("Existence"))
    documento = models.ForeignKey(Documento, on_delete=models.CASCADE,
                                  related_name='documentodetalletransfdptocontroltecnico_documento')
    producto = models.ForeignKey(ProductoFlujo, on_delete=models.PROTECT,
                                 related_name='documentodetalletransfdptocontroltecnico_producto',
                                 verbose_name=_("Product"))
    buenos = models.IntegerField(default=0, verbose_name=_("Good"))
    defectuoso_cc = models.IntegerField(default=0, verbose_name=_("Defective CC"))
    defectuoso_cien = models.IntegerField(default=0, verbose_name=_("Defective 100%"))
    sensorial = models.IntegerField(default=0, verbose_name=_("Sensory Test"))
    rotos = models.IntegerField(default=0, verbose_name=_("Broken"))

    class Meta:
        db_table = 'fp_documentodetalletransfdptocontroltecnico'


class DocumentoTransfDepartamentoRecibida(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    documento = models.ForeignKey(Documento, on_delete=models.PROTECT,
                                  related_name='documentotransfdepartamentorecibida_documento')
    documentoorigen = models.ForeignKey(Documento, on_delete=models.PROTECT,
                                        related_name='documentotransfdepartamentorecibida_documentoorigen',
                                        db_comment="Documento que originó la transferencia hacia el departamento")

    class Meta:
        db_table = 'fp_documentotransfdesdedepartamento'


class DocumentoTransfExterna(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    documento = models.ForeignKey(Documento, on_delete=models.CASCADE, related_name='documentotransfext_documento')
    # departamento_destino = models.ForeignKey(Departamento, on_delete=models.PROTECT, related_name='documentotransfext_departamento_destino', default=None)
    unidadcontable = models.ForeignKey(UnidadContable, on_delete=models.PROTECT,
                                       related_name='documentotransfext_unidadcontable')

    class Meta:
        db_table = 'fp_documentotransfexterna'


class DocumentoTransfExternaDptoDestino(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    documentotransfext = models.ForeignKey(Documento, on_delete=models.CASCADE,
                                           related_name='documentotransfextdptodest_documento')
    departamento_destino = models.ForeignKey(Departamento, on_delete=models.PROTECT,
                                             related_name='documentotransfext_departamento_destino')

    class Meta:
        db_table = 'fp_documentotransfexternadptodestino'


# transf hacia recibida desde otra unidad contable
class DocumentoTransfExternaRecibida(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    documento = models.ForeignKey(Documento, on_delete=models.CASCADE,
                                  related_name='documentotransfextrecibida_documento')
    unidadcontable = models.ForeignKey(UnidadContable, on_delete=models.PROTECT,
                                       related_name='documentotransfextrecibida_unidadcontable')

    class Meta:
        db_table = 'fp_documentotransfexternarecibida'


# ID DEL DOC QUE ORIGINO LA TRANSF
# SI LA BD NO ES UNICA EL DATO DEL ID DOCUMENTO NO EXISTE Y NO SE PUEDE DEFINIR LA UNIDAD CONTABLE ORIGEN.
class DocumentoTransfExternaRecibidaDocOrigen(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    documento = models.ForeignKey(Documento, on_delete=models.CASCADE, default=None,
                                  related_name='documentotransfextrecibidadocorigen_documento')
    documentoorigen = models.ForeignKey(Documento, on_delete=models.PROTECT, default=None,
                                        related_name='documentotransfextrecibida_documentoorigen')

    class Meta:
        db_table = 'fp_documentotransfexternarecibidadocorigen'


# Venta a trabajadores
class DocumentoDetalleVenta(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    importe = models.DecimalField(max_digits=18, decimal_places=2, default=0.00, verbose_name=_("Amount"))
    documentodetalle = models.ForeignKey(DocumentoDetalle, on_delete=models.PROTECT,
                                         related_name='documentodetalleventa_detalle')

    class Meta:
        db_table = 'fp_documentodetalleventa'


# Cambio de estado, estado destino
class DocumentoDetalleEstado(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    existencia = models.DecimalField(max_digits=18, decimal_places=6, default=0.00,
                                     verbose_name=_("Existence"))
    estado = IntegerChoicesField(choices_enum=EstadoProducto, verbose_name=_("Status"))
    documentodetalle = models.ForeignKey(DocumentoDetalle, on_delete=models.CASCADE,
                                         related_name='documentodetalleestado_detalle')
    precio = models.DecimalField(max_digits=18, decimal_places=7, default=0.00,
                                 verbose_name=_("Price"))
    cantidad = models.DecimalField(max_digits=18, decimal_places=4, default=0.00,
                                   verbose_name=_("Quantity"))
    producto = models.ForeignKey(ProductoFlujo, on_delete=models.PROTECT,
                                 related_name='documentodetalleproducto_estado',
                                 verbose_name=_("Product"), default=None)

    class Meta:
        db_table = 'fp_documentodetalleestado'


# Cambio de producto, producto destino
class DocumentoDetalleProducto(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    existencia = models.DecimalField(max_digits=18, decimal_places=6, default=0.00,
                                     verbose_name=_("Existence"))
    producto = models.ForeignKey(ProductoFlujo, on_delete=models.PROTECT,
                                 related_name='documentodetalleproducto_producto',
                                 verbose_name=_("Product"))
    estado = IntegerChoicesField(choices_enum=EstadoProducto, verbose_name=_("Status"), default=EstadoProducto.BUENO)
    documentodetalle = models.ForeignKey(DocumentoDetalle, on_delete=models.CASCADE,
                                         related_name='documentodetalleproducto_detalle')
    precio = models.DecimalField(max_digits=18, decimal_places=7, default=0.00,
                                 verbose_name=_("Price")
                                 )
    cantidad = models.DecimalField(max_digits=18, decimal_places=4, default=0.00,
                                   verbose_name=_("Quantity")
                                   )

    class Meta:
        db_table = 'fp_documentodetalleproducto'


class DocumentoDevolucion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    documento = models.ForeignKey(Documento, on_delete=models.PROTECT,
                                  related_name='documentodevolucion_documento')

    class Meta:
        db_table = 'fp_documentodevolucion'


# Devolución recibida desde otro dpto
class DocumentoDevolucionRecibida(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    documento = models.ForeignKey(Documento, on_delete=models.PROTECT,
                                  related_name='documentodevolucionrecibida_documento')
    documentoorigen = models.ForeignKey(Documento, on_delete=models.PROTECT,
                                        related_name='documentodevolucionrecibida_documentoorigen',
                                        db_comment="Documento que originó la devolucion hacia el departamento")

    class Meta:
        db_table = 'fp_documentodevolucionrecibida'


# Se guardan los documentos que se salvan o confirman y son los procedents del versat
class DocumentoOrigenVersat(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    documentoversat = models.IntegerField()
    fecha_documentoversat = models.DateTimeField(db_default=Now(), verbose_name=_("Fecha versat at"))
    documento = models.ForeignKey(Documento, on_delete=models.CASCADE, related_name='documentoorigenversat_documento')
    documento_origen = models.JSONField(blank=True, null=True, default=dict)

    class Meta:
        db_table = 'fp_documentoorigenversat'


# Los documentos del versat que son rechazados, se guarda el id de los documentos del versat que se rechazan
class DocumentoVersatRechazado(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    documentoversat = models.IntegerField()
    fecha_documentoversat = models.DateField()
    fecha_rechazo = models.DateTimeField(db_default=Now())
    documento_origen = models.JSONField(blank=True, null=True, default=dict)
    ueb = models.ForeignKey(UnidadContable, on_delete=models.PROTECT, related_name='documentoversatrechazado_ueb')

    class Meta:
        db_table = 'fp_documentoversatrechazado'


class FechaPeriodo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fecha = models.DateField(verbose_name=_("Date"))
    departamento = models.ForeignKey(Departamento, on_delete=models.PROTECT,
                                     related_name='fechaperiodo_departamento',
                                     verbose_name=_("Department"))
    ueb = models.ForeignKey(UnidadContable, on_delete=models.PROTECT,
                            related_name='fechaperiodo_ueb',
                            verbose_name="UEB")

    class Meta:
        db_table = 'fp_fechaperiodo'
        constraints = [
            models.UniqueConstraint(
                fields=['fecha', 'departamento', 'ueb'],
                name='unique_fechaperiodo_fecha_departamento_ueb'
            ),
        ]

    def to_dict(self):
        return {
            "ueb": self.ueb,
            self.departamento: {
                "fecha_procesamiento": self.fecha,
                "fecha_mes_procesamiento": self.fecha_mes_procesamiento
            }
        }

    @property
    def fecha_mes_procesamiento(self):
        return str(self.fecha.year) + '-' + str(self.fecha.month) + '-01'


class FechaCierreMes(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fecha = models.DateField(verbose_name=_("Date"))
    ueb = models.ForeignKey(UnidadContable, on_delete=models.PROTECT,
                            related_name='fechacierremes_ueb',
                            verbose_name="UEB")

    class Meta:
        db_table = 'fp_fechacierremes'
        constraints = [
            models.UniqueConstraint(
                fields=['fecha', 'ueb'],
                name='unique_fechacierremes_fecha_ueb'
            ),
        ]


class ExistenciaDpto(ObjectsManagerAbstract):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    producto = models.ForeignKey(ProductoFlujo, on_delete=models.PROTECT, related_name='existencias_producto',
                                 verbose_name=_("Product"))
    estado = IntegerChoicesField(choices_enum=EstadoProducto, verbose_name=_("Status"))
    cantidad_inicial = models.DecimalField(max_digits=18, decimal_places=4, default=0.00,
                                           verbose_name=_("Cantidad Inicial"))
    cantidad_entrada = models.DecimalField(max_digits=18, decimal_places=4, default=0.00,
                                           verbose_name=_("Entradas"))
    cantidad_salida = models.DecimalField(max_digits=18, decimal_places=4, default=0.00,
                                          verbose_name=_("Salidas"))
    cantidad_final = models.DecimalField(max_digits=18, decimal_places=4, default=0.00,
                                         verbose_name=_("Cantidad Final"))
    precio = models.DecimalField(max_digits=18, decimal_places=7, default=0.00,
                                 verbose_name=_("Price"))
    importe = models.DecimalField(max_digits=18, decimal_places=2, default=0.00,
                                  verbose_name=_("Amount"))
    departamento = models.ForeignKey(Departamento, on_delete=models.PROTECT, related_name='existencias_departamento')
    ueb = models.ForeignKey(UnidadContable, on_delete=models.PROTECT, related_name='existencias_ueb')

    class Meta:
        db_table = 'fp_existenciadpto'
        constraints = [
            models.UniqueConstraint(
                fields=['producto', 'estado', 'departamento', 'ueb'],
                name='unique_existencias_producto_estado_departamento_ueb'
            )
        ]
        indexes = [
            models.Index(
                fields=[
                    'producto',
                    'estado',
                    'departamento',
                    'ueb']
            )
        ]


class NumeroDocumentos(ObjectsManagerAbstract):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tiponumero = IntegerChoicesField(choices_enum=TipoNumeroDoc, verbose_name=_("Tipo número"),
                                     default=TipoNumeroDoc.NUMERO_CONSECUTIVO)
    departamento = models.ForeignKey(Departamento, on_delete=models.PROTECT,
                                     related_name='numdoc_departamento',
                                     verbose_name=_("Department"),
                                     blank=True, null=True)
    numero = models.IntegerField(verbose_name=_("Número"), default=0)
    ueb = models.ForeignKey(UnidadContable, on_delete=models.PROTECT,
                            related_name='numdoc_ueb',
                            verbose_name="UEB")

    class Meta:
        db_table = 'fp_numerodocumentos'
        constraints = [
            models.UniqueConstraint(
                fields=['tiponumero', 'departamento', 'ueb'],
                name='unique_numdocumentos_tiponumero_departamento_ueb'
            ),
        ]

        indexes = [
            models.Index(fields=[
                'departamento',
                'ueb'
            ]),
            models.Index(fields=[
                'ueb'
            ]
            ),
        ]
