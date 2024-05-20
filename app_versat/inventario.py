from django.db import models
from .general import GenUnidadcontable, GenUsuario, GenSubsistema, GenAlmacen
from .contabilidad import ConCuenta, ConCriterio
from .costo import CosCentro


class InvCategoria(models.Model):
    idcategoria = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'inv_categoria'
#
#
# class InvExistencia(models.Model):
#     idproducto = models.ForeignKey(GenProducto, models.DO_NOTHING, db_column='idproducto')
#     cantidad = models.DecimalField(max_digits=18, decimal_places=4)
#     preciomn = models.DecimalField(max_digits=18, decimal_places=7, blank=True, null=True)
#     importemn = models.DecimalField(max_digits=18, decimal_places=2)
#     preciomlc = models.DecimalField(max_digits=18, decimal_places=7, blank=True, null=True)
#     importemlc = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
#     idmedida = models.ForeignKey(GenMedida, models.DO_NOTHING, db_column='idmedida')
#     idcuentamn = models.ForeignKey(ConCuenta, models.DO_NOTHING, db_column='idcuentamn', blank=True, null=True, related_name='invmn')
#     idcuentamlc = models.ForeignKey(ConCuenta, models.DO_NOTHING, db_column='idcuentamlc', blank=True, null=True, related_name='invmlc')
#     idexistencia = models.AutoField(primary_key=True)
#     salidaprom = models.BooleanField()
#     ubicacion = models.CharField(max_length=50, blank=True, null=True)
#     idcategoria = models.ForeignKey(InvCategoria, models.DO_NOTHING, db_column='idcategoria')
#     crc = models.BigIntegerField()
#
#     class Meta:
#         managed = False
#         db_table = 'inv_existencia'
#
#
# class InvExistenciaalm(models.Model):
#     idexistencia = models.OneToOneField(InvExistencia, models.DO_NOTHING, db_column='idexistencia', primary_key=True)
#     idalmacen = models.ForeignKey(GenAlmacen, models.DO_NOTHING, db_column='idalmacen')
#
#     class Meta:
#         managed = False
#         db_table = 'inv_existenciaalm'


class InvDocumentoestado(models.Model):
    idestado = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'inv_documentoestado'


class InvRegdocum(models.Model):
    idregdocum = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=150)
    tipo = models.IntegerField()
    guid = models.CharField(unique=True, max_length=36)
    claveconfig = models.CharField(max_length=36, blank=True, null=True)
    almacen = models.BooleanField(db_column='Almacen')  # Field name made lowercase.
    texto = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'inv_regdocum'

class InvConcepto(models.Model):
    idconcepto = models.AutoField(primary_key=True)
    idregdocum = models.ForeignKey('InvRegdocum', models.DO_NOTHING, db_column='idregdocum')
    idcriterio = models.ForeignKey(ConCriterio, models.DO_NOTHING, db_column='idcriterio', blank=True, null=True)
    codigo = models.CharField(unique=True, max_length=4)
    descripcion = models.CharField(max_length=100)
    idcategoria = models.ForeignKey(InvCategoria, models.DO_NOTHING, db_column='idcategoria')
    activo = models.BooleanField(db_column='Activo', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'inv_concepto'


class InvDocumento(models.Model):
    iddocumento = models.AutoField(primary_key=True)
    numero = models.IntegerField()
    fecha = models.DateTimeField()
    sumacantidad = models.DecimalField(max_digits=18, decimal_places=4, blank=True, null=True)
    sumaimporte = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    idunidad = models.ForeignKey(GenUnidadcontable, models.DO_NOTHING, db_column='idunidad')
    idestado = models.ForeignKey('InvDocumentoestado', models.DO_NOTHING, db_column='idestado')
    idusuario = models.ForeignKey(GenUsuario, models.DO_NOTHING, db_column='idusuario', blank=True, null=True, related_name='idusuario_invdocumento_set')
    sumaexistencia = models.DecimalField(max_digits=18, decimal_places=4, blank=True, null=True)
    idconcepto = models.ForeignKey(InvConcepto, models.DO_NOTHING, db_column='idconcepto')
    numctrl = models.CharField(max_length=50, blank=True, null=True)
    idsubsistema = models.ForeignKey(GenSubsistema, models.DO_NOTHING, db_column='idsubsistema', blank=True, null=True)
    descripcion = models.CharField(max_length=250, blank=True, null=True)
    doc_almacen = models.ManyToManyField(GenAlmacen, through='InvDocumentoalm', through_fields=('iddocumento', 'idalmacen'))
    idusrconfirmar = models.ForeignKey(GenUsuario, models.DO_NOTHING, db_column='idusrconfirmar', blank=True, null=True, related_name='idusrconfirmar_invdocumento_set')
    crc = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'inv_documento'


# class InvMovimiento(models.Model):
#     idmovimiento = models.AutoField(primary_key=True)
#     cantidad = models.DecimalField(max_digits=18, decimal_places=4)
#     importe = models.DecimalField(max_digits=18, decimal_places=2)
#     existencia = models.DecimalField(max_digits=18, decimal_places=4)
#     iddocumento = models.ForeignKey(InvDocumento, models.DO_NOTHING, db_column='iddocumento')
#     idproducto = models.ForeignKey(GenProducto, models.DO_NOTHING, db_column='idproducto')
#     idmedida = models.ForeignKey(GenMedida, models.DO_NOTHING, db_column='idmedida')
#     crc = models.BigIntegerField()
#     precio = models.DecimalField(max_digits=18, decimal_places=7)
#
#     class Meta:
#         managed = False
#         db_table = 'inv_movimiento'
#
#
class InvDocumentoalm(models.Model):
    iddocumento = models.OneToOneField(InvDocumento, models.DO_NOTHING, db_column='iddocumento', primary_key=True)
    idalmacen = models.ForeignKey(GenAlmacen, models.DO_NOTHING, db_column='idalmacen')

    class Meta:
        managed = False
        db_table = 'inv_documentoalm'
#
#
# class InvDocumentomlc(models.Model):
#     iddocumento = models.OneToOneField(InvDocumento, models.DO_NOTHING, db_column='iddocumento', primary_key=True)
#     sumaimporte = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
#     crc = models.BigIntegerField()
#
#     class Meta:
#         managed = False
#         db_table = 'inv_documentomlc'
#
#
class InvDocumentocta(models.Model):
    iddocumento = models.OneToOneField(InvDocumento, models.DO_NOTHING, db_column='iddocumento', primary_key=True)
    idcuenta = models.ForeignKey(ConCuenta, models.DO_NOTHING, db_column='idcuenta', blank=True, null=True, related_name='idcuenta_invdocumentocta_set')
    idcuentamlc = models.ForeignKey(ConCuenta, models.DO_NOTHING, db_column='idcuentamlc', blank=True, null=True, related_name='idcuentamlc_invdocumentocta_set')

    class Meta:
        managed = False
        db_table = 'inv_documentocta'
#
#
# class InvDocumentoentidad(models.Model):
#     iddocumento = models.OneToOneField(InvDocumento, models.DO_NOTHING, db_column='iddocumento', primary_key=True)
#     identidad = models.ForeignKey(GenEntidad, models.DO_NOTHING, db_column='identidad')
#     iddocdev = models.IntegerField()
#
#     class Meta:
#         managed = False
#         db_table = 'inv_documentoentidad'
#
#
class InvDocumentogasto(models.Model):
    iddocumento = models.OneToOneField(InvDocumento, models.DO_NOTHING, db_column='iddocumento', primary_key=True)
    idcentro = models.ForeignKey(CosCentro, models.DO_NOTHING, db_column='idcentro')

    class Meta:
        managed = False
        db_table = 'inv_documentogasto'
#
#
# class InvDocumentoorden(models.Model):
#     iddocumento = models.OneToOneField(InvDocumento, models.DO_NOTHING, db_column='iddocumento', primary_key=True)
#     orden = models.CharField(max_length=10)
#
#     class Meta:
#         managed = False
#         db_table = 'inv_documentoorden'
#
#
# class InvDocumentotransfemit(models.Model):
#     iddocumento = models.OneToOneField(InvDocumento, models.DO_NOTHING, db_column='iddocumento', primary_key=True)
#     idalmacen = models.ForeignKey(GenAlmacen, models.DO_NOTHING, db_column='idalmacen')
#
#     class Meta:
#         managed = False
#         db_table = 'inv_documentotransfemit'
#
#
# class InvDocumentotransfemitext(models.Model):
#     iddocumento = models.IntegerField(primary_key=True)
#     destino = models.CharField(max_length=100)
#
#     class Meta:
#         managed = False
#         db_table = 'inv_documentotransfemitext'
#
#
# class InvDocumentotransfrec(models.Model):
#     iddocumento = models.OneToOneField(InvDocumento, models.DO_NOTHING, db_column='iddocumento', primary_key=True, related_name='iddocumento_invdocumentotransfrec_set')
#     iddocorigen = models.ForeignKey(InvDocumento, models.DO_NOTHING, db_column='iddocorigen', blank=True, null=True, related_name='iddocorigen_invdocumentotransfrec_set')
#     descrip = models.CharField(max_length=50, blank=True, null=True)
#     idalmacen = models.ForeignKey(GenAlmacen, models.DO_NOTHING, db_column='idalmacen')
#     automatico = models.BooleanField(blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'inv_documentotransfrec'
#
#
# class InvDocumentotransfrecext(models.Model):
#     iddocumento = models.IntegerField(primary_key=True)
#     origen = models.CharField(max_length=100)
#     doc = models.CharField(max_length=50, blank=True, null=True)
#     descrip = models.CharField(max_length=50, blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'inv_documentotransfrecext'
#
#
# class InvDocumentocomp(models.Model):
#     iddocumento = models.OneToOneField('InvDocumentoentidad', models.DO_NOTHING, db_column='iddocumento', primary_key=True)
#     recargo = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
#     descuento = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
#     sumaimporte = models.DecimalField(max_digits=18, decimal_places=2)
#     idmoneda = models.ForeignKey(GenMoneda, models.DO_NOTHING, db_column='idmoneda')
#     idtasa = models.ForeignKey(GenTasacambio, models.DO_NOTHING, db_column='idtasa', blank=True, null=True)
#     crearoblig = models.BooleanField()
#     iva = models.DecimalField(max_digits=18, decimal_places=4, blank=True, null=True)
#     factura = models.CharField(max_length=50, blank=True, null=True)
#     crc = models.BigIntegerField()
#     contrato = models.CharField(max_length=50, blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'inv_documentocomp'
#
#
# class InvDocumentocompmlc(models.Model):
#     iddocumento = models.OneToOneField(InvDocumentocomp, models.DO_NOTHING, db_column='iddocumento', primary_key=True)
#     sumaimporte = models.DecimalField(max_digits=18, decimal_places=2)
#     recargo = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
#     descuento = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
#     idmoneda = models.ForeignKey(GenMoneda, models.DO_NOTHING, db_column='idmoneda')
#     crc = models.BigIntegerField()
#
#     class Meta:
#         managed = False
#         db_table = 'inv_documentocompmlc'
#
# class InvServasoc(models.Model):
#     idservicio = models.AutoField(db_column='idServicio', primary_key=True)  # Field name made lowercase.
#     codigo = models.CharField(unique=True, max_length=3)
#     descripcion = models.CharField(max_length=200)
#
#     class Meta:
#         managed = False
#         db_table = 'inv_ServAsoc'
#
# class InvDocumentoserv(models.Model):
#     iddocumento = models.ForeignKey(InvDocumento, models.DO_NOTHING, db_column='iddocumento')
#     identidad = models.ForeignKey(GenEntidad, models.DO_NOTHING, db_column='identidad')
#     idservicio = models.ForeignKey(InvServasoc, models.DO_NOTHING, db_column='idservicio')
#     idmoneda = models.ForeignKey(GenMoneda, models.DO_NOTHING, db_column='idmoneda')
#     idtasa = models.ForeignKey(GenTasacambio, models.DO_NOTHING, db_column='idtasa', blank=True, null=True)
#     importe = models.DecimalField(max_digits=18, decimal_places=2)
#     iddocumentoserv = models.AutoField(primary_key=True)
#     crc = models.BigIntegerField()
#
#     class Meta:
#         managed = False
#         db_table = 'inv_documentoserv'
#         unique_together = (('iddocumento', 'identidad', 'idservicio', 'idmoneda'),)



