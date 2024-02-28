from django.db import models

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

class GenMascara(models.Model):
    idmascara = models.AutoField(primary_key=True)
    idformato = models.ForeignKey('GenFormato', models.DO_NOTHING, db_column='idformato')
    nombre = models.CharField(max_length=30)
    longitud = models.SmallIntegerField()
    abreviatura = models.CharField(max_length=5, blank=True, null=True)
    posicion = models.SmallIntegerField()

    class Meta:
        managed = True
        db_table = 'gen_mascara'


class GenFormato(models.Model):
    idformato = models.AutoField(primary_key=True)
    nombre = models.CharField(unique=True, max_length=30)
    longitud = models.IntegerField()
    separador = models.CharField(max_length=1)
    enuso = models.BooleanField()

    class Meta:
        managed = True
        db_table = 'gen_formato'


class GenMedida(models.Model):
    idmedida = models.AutoField(primary_key=True)
    clave = models.CharField(max_length=6)
    descripcion = models.CharField(max_length=50)

    class Meta:
        managed = True
        db_table = 'gen_medida'

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

