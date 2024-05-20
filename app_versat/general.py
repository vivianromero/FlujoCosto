from django.db import models

from codificadores import ChoiceTiposProd


class GenUnidadcontable(models.Model):
    idunidad = models.AutoField(primary_key=True)
    codigo = models.CharField(unique=True, max_length=10)
    nombre = models.CharField(unique=True, max_length=30)
    activo = models.BooleanField()
    direccion = models.CharField(db_column='Direccion', max_length=150, blank=True,
                                 null=True)
    dircorreo = models.CharField(db_column='DirCorreo', max_length=150, blank=True,
                                 null=True)
    idnae = models.IntegerField(blank=True, null=True)
    iddpa = models.IntegerField(blank=True, null=True)
    idreup = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'gen_unidadcontable'
        ordering = ['codigo']


class GenFormato(models.Model):
    idformato = models.AutoField(primary_key=True)
    nombre = models.CharField(unique=True, max_length=30)
    longitud = models.IntegerField()
    separador = models.CharField(max_length=1)
    enuso = models.BooleanField()

    class Meta:
        managed = True
        db_table = 'gen_formato'


class GenMascara(models.Model):
    idmascara = models.AutoField(primary_key=True)
    idformato = models.ForeignKey(GenFormato, models.DO_NOTHING, db_column='idformato')
    nombre = models.CharField(max_length=30)
    longitud = models.SmallIntegerField()
    abreviatura = models.CharField(max_length=5, blank=True, null=True)
    posicion = models.SmallIntegerField()

    class Meta:
        managed = True
        db_table = 'gen_mascara'


class GenMedida(models.Model):
    idmedida = models.AutoField(primary_key=True)
    clave = models.CharField(max_length=6)
    descripcion = models.CharField(max_length=50)

    class Meta:
        managed = True
        db_table = 'gen_medida'
        ordering = ['clave']


class GenProducto(models.Model):
    idproducto = models.AutoField(primary_key=True)
    codigo = models.CharField(unique=True, max_length=50)
    descripcion = models.CharField(max_length=100)
    idmedida = models.ForeignKey(GenMedida, models.DO_NOTHING, db_column='idmedida')
    idnivelclas = models.ForeignKey('GenNivelclasprod', models.DO_NOTHING, db_column='idnivelclas')
    activo = models.BooleanField()
    precio = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'gen_producto'

class GenUsuario(models.Model):
    idusuario = models.AutoField(primary_key=True)
    tipo = models.SmallIntegerField()
    activo = models.BooleanField()
    loginusuario = models.CharField(unique=True, max_length=128)
    nombre = models.CharField(max_length=128, blank=True, null=True)
    intentos = models.IntegerField()
    expira = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'gen_usuario'


class GenNivelclasprod(models.Model):
    idnivelclas = models.AutoField(primary_key=True)
    clavenivel = models.CharField(max_length=50)
    clave = models.CharField(unique=True, max_length=50)
    idapertura = models.ForeignKey('GenAperturaprod', models.DO_NOTHING, db_column='idapertura')
    activo = models.BooleanField()
    descripcion = models.CharField(max_length=100)

    class Meta:
        managed = True
        db_table = 'gen_nivelclasprod'
        unique_together = (('idapertura', 'clavenivel'),)


class GenAperturaprod(models.Model):
    idapertura = models.AutoField(primary_key=True)
    idmascara = models.ForeignKey('GenMascara', models.DO_NOTHING, db_column='idmascara')

    class Meta:
        managed = True
        db_table = 'gen_aperturaprod'


# class ConApertura(models.Model):
#     idapertura = models.AutoField(primary_key=True)
#     idmascara = models.ForeignKey(GenMascara, models.DO_NOTHING, db_column='idmascara')
#     idunidad = models.ForeignKey(GenUnidadcontable, models.DO_NOTHING, db_column='idunidad', blank=True, null=True)
#     tipo = models.SmallIntegerField()
#
#     class Meta:
#         managed = True
#         db_table = 'con_apertura'
#
#
# class ConCuenta(models.Model):
#     idcuenta = models.AutoField(primary_key=True)
#     clave = models.CharField(unique=True, max_length=50)
#     idapertura = models.ForeignKey(ConApertura, models.DO_NOTHING, db_column='idapertura')
#     activa = models.BooleanField()
#
#     class Meta:
#         managed = True
#         db_table = 'con_cuenta'


# class ConCuentanat(models.Model):
#     idcuenta = models.ForeignKey(ConCuenta, models.DO_NOTHING, db_column='idcuenta', primary_key=True)
#     clave = models.CharField(unique=True, max_length=50)
#     descripcion = models.CharField(unique=True, max_length=255)
#     naturaleza = models.SmallIntegerField()
#
#     class Meta:
#         managed = True
#         db_table = 'con_cuentanat'

class GenSubsistema(models.Model):
    idsubsistema = models.AutoField(primary_key=True)
    nombre = models.CharField(unique=True, max_length=30)
    guid = models.CharField(unique=True, max_length=16)
    sps = models.CharField(db_column='SPS', max_length=3802)
    hsps = models.CharField(db_column='HSPS', max_length=900)

    class Meta:
        managed = True
        db_table = 'gen_subsistema'

class GenAlmacen(models.Model):
    idalmacen = models.AutoField(primary_key=True)
    codigo = models.CharField(unique=True, max_length=4)
    nombre = models.CharField(unique=True, max_length=30)
    idunidad = models.ForeignKey('GenUnidadcontable', models.DO_NOTHING, db_column='idunidad')
    activo = models.BooleanField()
    jefe = models.CharField(db_column='Jefe', max_length=150)  # Field name made lowercase.
    direccion = models.CharField(db_column='Direccion', max_length=150)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'gen_almacen'


# SisGestMP

class MPMarca(models.Model):
    idMarca = models.AutoField(primary_key=True)
    codigoMarca = models.CharField(unique=True, max_length=50)
    descripcion = models.CharField(unique=True, max_length=50)

    class Meta:
        managed = True
        db_table = 'Marca'
        ordering = ['descripcion']


# Sispax
class SisPaxClaseProducto(models.Model):
    id = models.AutoField(primary_key=True)
    descripcion = models.CharField(unique=True)
    capote_fortaleza = models.CharField(max_length=1)

    class Meta:
        managed = True
        db_table = 'fp_ClaseProducto'


class SisPaxTipoProductoFlujo(models.Model):
    id = models.AutoField(primary_key=True)
    descripcion = models.CharField(unique=True)

    class Meta:
        managed = True
        db_table = 'fp_TipoProductoFlujo'


class SisPaxMedida(models.Model):
    idmedida = models.AutoField(primary_key=True)
    clave = models.CharField(unique=True)
    descripcion = models.CharField(unique=True)

    class Meta:
        managed = True
        db_table = 'gen_medida'


class SisPaxProductoFlujo(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    codigo = models.CharField(unique=True)
    descripcion = models.CharField(unique=True)
    activo = models.BooleanField(default=True)
    tipo = models.ForeignKey(SisPaxTipoProductoFlujo, on_delete=models.DO_NOTHING, db_column="tipo")
    fk_um = models.ForeignKey(SisPaxMedida, on_delete=models.DO_NOTHING, db_column="fk_um")

    class Meta:
        managed = True
        db_table = 'fp_ProductoFlujo'

    @property
    def get_clasemateriaprima(self):
        return None if self.tipo.pk != ChoiceTiposProd.MATERIAPRIMA else self.productoclase_producto.get().fk_claseprod


class SispaxProductoFlujoClase(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    fk_prod = models.ForeignKey(SisPaxProductoFlujo, on_delete=models.DO_NOTHING, db_column="fk_prod",
                                related_name='productoclase_producto')
    fk_claseprod = models.ForeignKey(SisPaxClaseProducto, on_delete=models.DO_NOTHING, db_column="fk_claseprod",
                                     related_name='productoclase_clase')

    class Meta:
        managed = True
        db_table = 'fp_ProductoFlujoClase'


class SisPaxCategoriaVitola(models.Model):
    id = models.AutoField(primary_key=True)
    descripcion = models.CharField(unique=True)

    class Meta:
        managed = True
        db_table = 'fp_Categorias'


class SisPaxTipoVitola(models.Model):
    id = models.AutoField(primary_key=True)
    descripcion = models.CharField(unique=True)

    class Meta:
        managed = True
        db_table = 'fp_TipoVitola'


class SisPaxVitola(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    diametro = models.DecimalField(max_digits=10, decimal_places=2)
    longitud = models.IntegerField()
    fk_cat = models.ForeignKey(SisPaxCategoriaVitola, models.DO_NOTHING, db_column="fk_cat")
    destino = models.CharField(max_length=1)
    fk_tipo = models.ForeignKey(SisPaxTipoVitola, models.DO_NOTHING, db_column="fk_tipo",
                                related_name='vitola_producto')
    fk_prod = models.ForeignKey(SisPaxProductoFlujo, models.DO_NOTHING, db_column="fk_prod")
    cepo = models.IntegerField()
    prod_capa = models.ForeignKey(SisPaxProductoFlujo, models.DO_NOTHING, db_column="prod_capa",
                                  related_name='vitola_productocapa')
    prod_pesada = models.ForeignKey(SisPaxProductoFlujo, models.DO_NOTHING, db_column="prod_pesada",
                                    related_name='vitola_productopesada')

    class Meta:
        managed = True
        db_table = 'fp_Vitolas'

