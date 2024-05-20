from django.db import models
from .general import GenSubsistema

class ConApertura(models.Model):
    idapertura = models.AutoField(primary_key=True)
    idmascara = models.ForeignKey('GenMascara', models.DO_NOTHING, db_column='idmascara')
    idunidad = models.ForeignKey('GenUnidadcontable', models.DO_NOTHING, db_column='idunidad', blank=True, null=True)
    tipo = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'con_apertura'

class ConCuenta(models.Model):
    idcuenta = models.AutoField(primary_key=True)
    clave = models.CharField(max_length=50)
    idapertura = models.ForeignKey('ConApertura', models.DO_NOTHING, db_column='idapertura')
    activa = models.BooleanField()

    class Meta:
        managed = True
        db_table = 'con_cuenta'
        unique_together = (('idapertura', 'clave'),)

class ConCuentanat(models.Model):
    idcuenta = models.ForeignKey('ConCuenta', models.DO_NOTHING, db_column='idcuenta')
    cuenta = models.CharField(db_column='clave', max_length=50, primary_key=True)
    descripcion = models.CharField(max_length=255)
    naturaleza = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'con_cuentanat'


class ConCriterio(models.Model):
    idcriterio = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=200)
    idsubsistema = models.ForeignKey('GenSubsistema', models.DO_NOTHING, db_column='idsubsistema')

    class Meta:
        managed = False
        db_table = 'con_criterio'
