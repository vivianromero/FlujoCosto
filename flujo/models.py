import uuid
from django.db import models
from codificadores.models import UnidadContable, Departamento, TipoDocumento, MotivoAjuste, EstadoProducto, \
    ProductoFlujo
from configuracion.models import Ueb


class Documento(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fecha = models.DateField()
    fecha_creado = models.DateField()
    numerocontrol = models.CharField(max_length=50)
    numeroconsecutivo = models.IntegerField()
    observaciones = models.TextField(blank=True, null=True)
    confirmado = models.BooleanField(default=False)
    rechazado = models.BooleanField(default=False)
    reproceso = models.BooleanField(default=False)
    editar_nc = models.BooleanField(default=False)
    comprob = models.CharField(max_length=150, blank=True, null=True)
    iddepartamento = models.ForeignKey(Departamento, on_delete=models.PROTECT, related_name='documento_departamento')
    idtipodocumento = models.ForeignKey(TipoDocumento, on_delete=models.PROTECT, related_name='documento_tipodocumento')
    idueb = models.ForeignKey(Ueb, on_delete=models.PROTECT, related_name='documento_tipodocumento')

    class Meta:
        db_table = 'fp_documento'
        unique_together = (('numeroconsecutivo', 'idtipodocumento', 'iddepartamento', 'idueb'),)
        ordering = ['idueb', 'iddepartamento', 'idtipodocumento', '-numeroconsecutivo']

class DocumentoDetalle(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cantidad = models.DecimalField(max_digits=18, decimal_places=6, default=0.00)
    importe = models.DecimalField(max_digits=18, decimal_places=2, default=0.00)
    existencia = models.DecimalField(max_digits=18, decimal_places=6, default=0.00)
    iddocumento = models.ForeignKey(Documento, on_delete=models.PROTECT, related_name='documentodetalle_documento')
    idestado = models.ForeignKey(EstadoProducto, on_delete=models.PROTECT,
                                 related_name='documentodetalle_productoestado')
    idproducto = models.ForeignKey(ProductoFlujo, on_delete=models.PROTECT, related_name='documentodetalle_producto')

    class Meta:
        db_table = 'fp_documentodetalle'

class DocumentoAjuste(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    iddocumento = models.ForeignKey(Documento, on_delete=models.PROTECT, related_name='documentoajuste_documento')
    idmotivoajuste = models.ForeignKey(MotivoAjuste, on_delete=models.PROTECT, related_name='documentoajuste_motivo')

    class Meta:
        db_table = 'fp_documentoajuste'

class DocumentoTransfDepartamento(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    iddocumento = models.ForeignKey(Documento, on_delete=models.PROTECT,
                                    related_name='documentotransfdepartamento_documento')
    iddepartamento = models.ForeignKey(Departamento, on_delete=models.PROTECT,
                                       related_name='documentotransfdepartamento_departamento')

    class Meta:
        db_table = 'fp_documentotransfdepartamento'

class DocumentoTransfDepartamentoRecibida(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    iddocumento = models.ForeignKey(Documento, on_delete=models.PROTECT, related_name='documentotransfdepartamentorecibida_documento')
    iddocumentoorigen = models.ForeignKey(Documento, on_delete=models.PROTECT,
                                    related_name='documentotransfdepartamentorecibida_documentoorigen',
                                    db_comment="Documento que originó la transferencia hacia el departamento")

    class Meta:
        db_table = 'fp_documentotransfdesdedepartamento'

class DocumentoTransfExterna(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    iddocumento = models.ForeignKey(Documento, on_delete=models.PROTECT, related_name='documentotransfext_documento')
    idunidadcontable = models.ForeignKey(UnidadContable, on_delete=models.PROTECT,
                                         related_name='documentotransfext_unidadcontable')

    class Meta:
        db_table = 'fp_documentotransfexterna'

class DocumentoTransfExternaDptoDestino(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    iddocumentotransfext = models.ForeignKey(Documento, on_delete=models.CASCADE, related_name='documentotransfextdptodest_documento')
    iddptodestino = models.ForeignKey(Departamento, on_delete=models.PROTECT, related_name='documentotransfextdptodest_dptodest')

    class Meta:
        db_table = 'fp_documentotransfexternadptodestino'

#transf hacia recibida desde otra unidad contable
class DocumentoTransfExternaRecibida(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    iddocumento = models.ForeignKey(Documento, on_delete=models.PROTECT, related_name='documentotransfextrecibida_documento')
    idunidadcontable = models.ForeignKey(UnidadContable, on_delete=models.PROTECT,
                                         related_name='documentotransfextrecibida_unidadcontable')

    class Meta:
        db_table = 'fp_documentotransfexternarecibida'

#ID DEL DOC QUE ORIGINO LA TRANSF
#SI LA BD NO ES UNICA EL DATO DEL ID DOCUMENTO NO EXISTE Y NO SE PUEDE DEFINIR LA UNIDAD CONTABLE ORIGEN.
class DocumentoTransfExternaRecibidaDocOrigen(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    iddocumentoorigen = models.ForeignKey(DocumentoTransfExternaRecibida, on_delete=models.CASCADE,
                                    related_name='documentotransfextrecibidadocorigen_documento')
    iddocumentoorigen = models.ForeignKey(Documento, on_delete=models.PROTECT,
                                          related_name='documentotransfextrecibida_documentoorigen')

    class Meta:
        db_table = 'fp_documentotransfexternarecibidadocorigen'


# Venta a trabajadores
class DocumentoDetalleVenta(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    importe = models.DecimalField(max_digits=18, decimal_places=2, default=0.00)
    iddocumentodetalle = models.ForeignKey(DocumentoDetalle, on_delete=models.PROTECT,
                                           related_name='documentodetalleventa_detalle')

    class Meta:
        db_table = 'fp_documentodetalleventa'


# Cambio de estado, estado destino
class DocumentoDetalleEstado(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    existencia = models.DecimalField(max_digits=18, decimal_places=6, default=0.00)
    idestado = models.ForeignKey(EstadoProducto, on_delete=models.PROTECT,
                                 related_name='documentodetalleestado_estado')
    iddocumentodetalle = models.ForeignKey(DocumentoDetalle, on_delete=models.PROTECT,
                                           related_name='documentodetalleestado_detalle')

    class Meta:
        db_table = 'fp_documentodetalleestado'

# Cambio de producto, producto destino
class DocumentoDetalleProducto(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    existencia = models.DecimalField(max_digits=18, decimal_places=6, default=0.00)
    idproducto = models.ForeignKey(ProductoFlujo, on_delete=models.PROTECT,
                                   related_name='documentodetalleproducto_producto')
    iddocumentodetalle = models.ForeignKey(DocumentoDetalle, on_delete=models.PROTECT,
                                           related_name='documentodetalleproducto_detalle')

    class Meta:
        db_table = 'fp_documentodetalleproducto'


class DocumentoDevolucion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    iddocumento = models.ForeignKey(Documento, on_delete=models.PROTECT,
                                    related_name='documentodevolucion_documento')

    class Meta:
        db_table = 'fp_documentodevolucion'

#Devolución recibida desde otro dpto
class DocumentoDevolucionRecibida(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    iddocumento = models.ForeignKey(Documento, on_delete=models.PROTECT, related_name='documentodevolucionrecibida_documento')
    iddocumentoorigen = models.ForeignKey(Documento, on_delete=models.PROTECT,
                                    related_name='documentodevolucionrecibida_documentoorigen',
                                    db_comment="Documento que originó la devolucion hacia el departamento")

    class Meta:
        db_table = 'fp_documentodevolucionrecibida'

# Se guardan los documentos que se salvan o confirman y son los procedents del versat
class DocumentoOrigenVersat(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    iddocumentoversat = models.IntegerField()
    iddocumento = models.ForeignKey(Documento, on_delete=models.PROTECT, related_name='documentoorigenversat_documento')

    class Meta:
        db_table = 'fp_documentoorigenversat'

# Los documentos del versat que son rechazados, se guarda el id de los documentos del versat que se rechazan
class DocumentoVersatRechazado(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    iddocumentoversat = models.IntegerField()
    idueb = models.ForeignKey(Ueb, on_delete=models.PROTECT, related_name='documentoversatrechazado_ueb')

    class Meta:
        db_table = 'fp_documentoversatrechazado'

class FechaPeriodo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fecha = models.DateField()
    iddepartamento = models.ForeignKey(Departamento, on_delete=models.PROTECT,
                                       related_name='fechaperiodo_departamento')
    idueb = models.ForeignKey(Ueb, on_delete=models.PROTECT,
                                       related_name='fechaperiodo_ueb')

    class Meta:
        db_table = 'fp_fechaperiodo'
        unique_together = (('fecha', 'iddepartamento', 'idueb'),)


class FechaCierreMes(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fecha = models.DateField()
    idueb = models.ForeignKey(Ueb, on_delete=models.PROTECT,
                                       related_name='fechacierremes_ueb')
    class Meta:
        db_table = 'fp_fechacierremes'
        unique_together = (('fecha', 'idueb'),)
