import uuid

from django.db import models
from django.db.models.functions import Now

from codificadores.models import UnidadContable, Departamento, TipoDocumento, MotivoAjuste, EstadoProducto, \
    ProductoFlujo
from configuracion.models import Ueb


class Documento(models.Model):
    CHOICE_ESTADOS_DOCUMENTO = {
        1: 'Edición',
        2: 'Confirmado',
        3: 'Rechazado',
    }

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fecha = models.DateField()
    fecha_creacion = models.DateTimeField(db_default=Now())
    numerocontrol = models.CharField(max_length=50)
    numeroconsecutivo = models.IntegerField()
    suma_importe = models.DecimalField(max_digits=18, decimal_places=2, default=0.00)
    observaciones = models.TextField(blank=True, null=True)
    estado = models.IntegerField(choices=CHOICE_ESTADOS_DOCUMENTO,
                                 db_comment="Estado del documento 1:Edición, 2:Confirmado, 3:Rechazado")
    reproceso = models.BooleanField(default=False)
    editar_nc = models.BooleanField(default=False)
    comprob = models.CharField(max_length=150, blank=True, null=True)
    iddepartamento = models.ForeignKey(Departamento, on_delete=models.PROTECT, related_name='documento_departamento')
    idtipodocumento = models.ForeignKey(TipoDocumento, on_delete=models.PROTECT, related_name='documento_tipodocumento')
    idueb = models.ForeignKey(Ueb, on_delete=models.PROTECT, related_name='documento_tipodocumento')

    class Meta:
        db_table = 'fp_documento'
        #unique_together = (('numeroconsecutivo', 'idtipodocumento', 'iddepartamento', 'idueb'),)
        ordering = ['idueb', 'iddepartamento', 'idtipodocumento', '-numeroconsecutivo']


class DocumentoDetalle(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cantidad = models.DecimalField(max_digits=18, decimal_places=4, default=0.00)
    precio = models.DecimalField(max_digits=18, decimal_places=7, default=0.00)
    importe = models.DecimalField(max_digits=18, decimal_places=2, default=0.00)
    existencia = models.DecimalField(max_digits=18, decimal_places=4, default=0.00)
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

#esto es el detalle de la transf hacia departamento PARA EL DEPARTAMENTO DE CONTROL TECNICO
#se genera la transf hacia departamento con los buenos, suma de los defectuosos y prueba sensorial
class DocumentoDetalleTransfDptoControlTecnico(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cantidad = models.DecimalField(max_digits=18, decimal_places=4, default=0.00)
    precio = models.DecimalField(max_digits=18, decimal_places=7, default=0.00)
    importe = models.DecimalField(max_digits=18, decimal_places=2, default=0.00)
    existencia = models.DecimalField(max_digits=18, decimal_places=4, default=0.00)
    iddocumento = models.ForeignKey(Documento, on_delete=models.CASCADE, related_name='documentodetalletransfdptocontroltecnico_documento')
    idproducto = models.ForeignKey(ProductoFlujo, on_delete=models.PROTECT, related_name='documentodetalletransfdptocontroltecnico_producto')
    buenos = models.IntegerField(default=0)
    defectuoso_cc = models.IntegerField(default=0)
    defectuoso_cien = models.IntegerField(default=0)
    sensorial = models.IntegerField(default=0)
    rotos = models.IntegerField(default=0)

    class Meta:
        db_table = 'fp_documentodetalletransfdptocontroltecnico'

class DocumentoTransfDepartamentoRecibida(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    iddocumento = models.ForeignKey(Documento, on_delete=models.PROTECT,
                                    related_name='documentotransfdepartamentorecibida_documento')
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
    iddocumentotransfext = models.ForeignKey(Documento, on_delete=models.CASCADE,
                                             related_name='documentotransfextdptodest_documento')
    iddptodestino = models.ForeignKey(Departamento, on_delete=models.PROTECT,
                                      related_name='documentotransfextdptodest_dptodest')

    class Meta:
        db_table = 'fp_documentotransfexternadptodestino'


# transf hacia recibida desde otra unidad contable
class DocumentoTransfExternaRecibida(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    iddocumento = models.ForeignKey(Documento, on_delete=models.PROTECT,
                                    related_name='documentotransfextrecibida_documento')
    idunidadcontable = models.ForeignKey(UnidadContable, on_delete=models.PROTECT,
                                         related_name='documentotransfextrecibida_unidadcontable')

    class Meta:
        db_table = 'fp_documentotransfexternarecibida'


# ID DEL DOC QUE ORIGINO LA TRANSF
# SI LA BD NO ES UNICA EL DATO DEL ID DOCUMENTO NO EXISTE Y NO SE PUEDE DEFINIR LA UNIDAD CONTABLE ORIGEN.
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


# Devolución recibida desde otro dpto
class DocumentoDevolucionRecibida(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    iddocumento = models.ForeignKey(Documento, on_delete=models.PROTECT,
                                    related_name='documentodevolucionrecibida_documento')
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
    origen_versat = models.CharField(max_length=40)

    class Meta:
        db_table = 'fp_documentoorigenversat'


# Los documentos del versat que son rechazados, se guarda el id de los documentos del versat que se rechazan
class DocumentoVersatRechazado(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    iddocumentoversat = models.IntegerField()
    fecha_doc_versat = models.DateField()
    fecha_rechazo = models.DateTimeField(db_default=Now())
    idueb = models.ForeignKey(Ueb, on_delete=models.PROTECT, related_name='documentoversatrechazado_ueb')

    class Meta:
        db_table = 'fp_documentoversatrechazado'

# Existencia por departamentos
class ExistenciaDpto(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    iddepartamento = models.ForeignKey(Departamento, on_delete=models.PROTECT, related_name='existenciadpto_departamento')
    idueb = models.ForeignKey(Ueb, on_delete=models.PROTECT, related_name='existenciadpto_ueb')
    idproducto = models.ForeignKey(ProductoFlujo, on_delete=models.PROTECT,
                                   related_name='existenciadpto_producto')
    idestado = models.ForeignKey(EstadoProducto, on_delete=models.PROTECT,
                                 related_name='existenciadpto_productoestado')
    existencia = models.DecimalField(max_digits=18, decimal_places=4, default=0.00)
    importe = models.DecimalField(max_digits=18, decimal_places=2, default=0.00)

    class Meta:
        db_table = 'fp_existenciadpto'


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
