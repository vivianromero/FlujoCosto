import uuid

from django.db import models
from django.db.models.functions import Now

from codificadores.models import UnidadContable, Departamento, TipoDocumento, MotivoAjuste, EstadoProducto, \
    ProductoFlujo
from django.utils.translation import gettext_lazy as _

class Documento(models.Model):
    CHOICE_ESTADOS_DOCUMENTO = {
        1: 'Edición',
        2: 'Confirmado',
        3: 'Rechazado',
    }

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fecha = models.DateField(verbose_name=_("Date"))
    fecha_creacion = models.DateTimeField(db_default=Now(), verbose_name=_("Create at"))
    numerocontrol = models.CharField(max_length=50, verbose_name=_("Control Number"))
    numeroconsecutivo = models.IntegerField(verbose_name=_("Consecutive Number"))
    suma_importe = models.DecimalField(max_digits=18, decimal_places=2, default=0.00, verbose_name=_("Amount"))
    observaciones = models.TextField(blank=True, null=True, verbose_name=_("Observations"))
    estado = models.IntegerField(choices=CHOICE_ESTADOS_DOCUMENTO,
                                 db_comment="Estado del documento 1:Edición, 2:Confirmado, 3:Rechazado",
                                 verbose_name=_("Status"))
    reproceso = models.BooleanField(default=False, verbose_name=_("Reprocessing"))
    editar_nc = models.BooleanField(default=False)
    comprob = models.CharField(max_length=150, blank=True, null=True)
    departamento = models.ForeignKey(Departamento, on_delete=models.PROTECT, related_name='documento_departamento')
    tipodocumento = models.ForeignKey(TipoDocumento, on_delete=models.PROTECT, related_name='documento_tipodocumento')
    ueb = models.ForeignKey(UnidadContable, on_delete=models.PROTECT, related_name='documento_tipodocumento')

    class Meta:
        db_table = 'fp_documento'
        #unique_together = (('numeroconsecutivo', 'tipodocumento', 'departamento', 'ueb'),)
        ordering = ['ueb', 'departamento', 'tipodocumento', '-numeroconsecutivo']


class DocumentoDetalle(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cantidad = models.DecimalField(max_digits=18, decimal_places=4, default=0.00,
                                   verbose_name=_("Quantity"))
    precio = models.DecimalField(max_digits=18, decimal_places=7, default=0.00,
                                 verbose_name=_("Price"))
    importe = models.DecimalField(max_digits=18, decimal_places=2, default=0.00,
                                  verbose_name=_("Amount"))
    existencia = models.DecimalField(max_digits=18, decimal_places=4, default=0.00,
                                     verbose_name=_("Existence"))
    documento = models.ForeignKey(Documento, on_delete=models.PROTECT, related_name='documentodetalle_documento')
    estado = models.ForeignKey(EstadoProducto, on_delete=models.PROTECT,
                                 related_name='documentodetalle_productoestado', verbose_name=_("Status"))
    producto = models.ForeignKey(ProductoFlujo, on_delete=models.PROTECT, related_name='documentodetalle_producto',
                                   verbose_name=_("Product"))

    class Meta:
        db_table = 'fp_documentodetalle'


class DocumentoAjuste(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    documento = models.ForeignKey(Documento, on_delete=models.PROTECT, related_name='documentoajuste_documento')
    motivoajuste = models.ForeignKey(MotivoAjuste, on_delete=models.PROTECT, related_name='documentoajuste_motivo',
                                       verbose_name=_("Adjustment Reason"))

    class Meta:
        db_table = 'fp_documentoajuste'


class DocumentoTransfDepartamento(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    documento = models.ForeignKey(Documento, on_delete=models.PROTECT,
                                    related_name='documentotransfdepartamento_documento')
    departamento = models.ForeignKey(Departamento, on_delete=models.PROTECT,
                                       related_name='documentotransfdepartamento_departamento',
                                       verbose_name=_("Department"))

    class Meta:
        db_table = 'fp_documentotransfdepartamento'

#esto es el detalle de la transf hacia departamento PARA EL DEPARTAMENTO DE CONTROL TECNICO
#se genera la transf hacia departamento con los buenos, suma de los defectuosos y prueba sensorial
class DocumentoDetalleTransfDptoControlTecnico(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cantidad = models.DecimalField(max_digits=18, decimal_places=4, default=0.00,
                                   verbose_name=_("Quantity"))
    precio = models.DecimalField(max_digits=18, decimal_places=7, default=0.00,
                                 verbose_name=_("Price"))
    importe = models.DecimalField(max_digits=18, decimal_places=2, default=0.00,
                                  verbose_name=_("Amount"))
    existencia = models.DecimalField(max_digits=18, decimal_places=4, default=0.00,
                                     verbose_name=_("Existence"))
    documento = models.ForeignKey(Documento, on_delete=models.CASCADE, related_name='documentodetalletransfdptocontroltecnico_documento')
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
    documento = models.ForeignKey(Documento, on_delete=models.PROTECT, related_name='documentotransfext_documento')
    unidadcontable = models.ForeignKey(UnidadContable, on_delete=models.PROTECT,
                                         related_name='documentotransfext_unidadcontable')

    class Meta:
        db_table = 'fp_documentotransfexterna'


class DocumentoTransfExternaDptoDestino(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    documentotransfext = models.ForeignKey(Documento, on_delete=models.CASCADE,
                                             related_name='documentotransfextdptodest_documento')
    dptodestino = models.ForeignKey(Departamento, on_delete=models.PROTECT,
                                      related_name='documentotransfextdptodest_dptodest')

    class Meta:
        db_table = 'fp_documentotransfexternadptodestino'


# transf hacia recibida desde otra unidad contable
class DocumentoTransfExternaRecibida(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    documento = models.ForeignKey(Documento, on_delete=models.PROTECT,
                                    related_name='documentotransfextrecibida_documento')
    unidadcontable = models.ForeignKey(UnidadContable, on_delete=models.PROTECT,
                                         related_name='documentotransfextrecibida_unidadcontable')

    class Meta:
        db_table = 'fp_documentotransfexternarecibida'


# ID DEL DOC QUE ORIGINO LA TRANSF
# SI LA BD NO ES UNICA EL DATO DEL ID DOCUMENTO NO EXISTE Y NO SE PUEDE DEFINIR LA UNIDAD CONTABLE ORIGEN.
class DocumentoTransfExternaRecibidaDocOrigen(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    documentoorigen = models.ForeignKey(DocumentoTransfExternaRecibida, on_delete=models.CASCADE,
                                          related_name='documentotransfextrecibidadocorigen_documento')
    documentoorigen = models.ForeignKey(Documento, on_delete=models.PROTECT,
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
    estado = models.ForeignKey(EstadoProducto, on_delete=models.PROTECT,
                                 related_name='documentodetalleestado_estado',
                                 verbose_name=_("Status"))
    documentodetalle = models.ForeignKey(DocumentoDetalle, on_delete=models.PROTECT,
                                           related_name='documentodetalleestado_detalle')

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
    documentodetalle = models.ForeignKey(DocumentoDetalle, on_delete=models.PROTECT,
                                           related_name='documentodetalleproducto_detalle')

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
    documento = models.ForeignKey(Documento, on_delete=models.PROTECT, related_name='documentoorigenversat_documento')
    origen_versat = models.CharField(max_length=40)

    class Meta:
        db_table = 'fp_documentoorigenversat'


# Los documentos del versat que son rechazados, se guarda el id de los documentos del versat que se rechazan
class DocumentoVersatRechazado(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    documentoversat = models.IntegerField()
    fecha_doc_versat = models.DateField()
    fecha_rechazo = models.DateTimeField(db_default=Now())
    ueb = models.ForeignKey(UnidadContable, on_delete=models.PROTECT, related_name='documentoversatrechazado_ueb')

    class Meta:
        db_table = 'fp_documentoversatrechazado'

# Existencia por departamentos
class ExistenciaDpto(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    departamento = models.ForeignKey(Departamento, on_delete=models.PROTECT, related_name='existenciadpto_departamento')
    ueb = models.ForeignKey(UnidadContable, on_delete=models.PROTECT, related_name='existenciadpto_ueb')
    producto = models.ForeignKey(ProductoFlujo, on_delete=models.PROTECT,
                                   related_name='existenciadpto_producto')
    estado = models.ForeignKey(EstadoProducto, on_delete=models.PROTECT,
                                 related_name='existenciadpto_productoestado')
    existencia = models.DecimalField(max_digits=18, decimal_places=4, default=0.00,
                                     verbose_name=_("Existence"))
    importe = models.DecimalField(max_digits=18, decimal_places=2, default=0.00,
                                  verbose_name=_("Amount"))

    class Meta:
        db_table = 'fp_existenciadpto'


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
        unique_together = (('fecha', 'departamento', 'ueb'),)


class FechaCierreMes(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fecha = models.DateField(verbose_name=_("Date"))
    ueb = models.ForeignKey(UnidadContable, on_delete=models.PROTECT,
                              related_name='fechacierremes_ueb',
                              verbose_name="UEB")

    class Meta:
        db_table = 'fp_fechacierremes'
        unique_together = (('fecha', 'ueb'),)
