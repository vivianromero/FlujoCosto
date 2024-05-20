from django.db import models
from app_versat.general import GenMascara, GenUnidadcontable


class CosApertura(models.Model):
    idapertura = models.AutoField(primary_key=True)
    idmascara = models.ForeignKey('GenMascara', models.DO_NOTHING, db_column='idmascara')
    idunidad = models.ForeignKey('GenUnidadcontable', models.DO_NOTHING, db_column='idunidad', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cos_apertura'


class CosCentro(models.Model):
    idcentro = models.AutoField(primary_key=True)
    clave = models.CharField(max_length=50)
    clavenivel = models.CharField(max_length=25)
    descripcion = models.CharField(max_length=255)
    idapertura = models.ForeignKey('CosApertura', models.DO_NOTHING, db_column='idapertura')
    activo = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'cos_centro'
        unique_together = (('clave', 'idapertura'), ('idapertura', 'clavenivel'),)


# class CosElementoGasto(models.Model):
#     idelementogasto = models.AutoField(primary_key=True)
#     codigo = models.CharField(max_length=50)
#     descripcion = models.CharField(max_length=255)
#     activo = models.BooleanField()
#
#     class Meta:
#         managed = True
#         db_table = 'cos_elementogasto'
#
# class CosPartida(models.Model):
#     idpartida = models.AutoField(primary_key=True)
#     codigo = models.CharField(max_length=50)
#     descripcion = models.CharField(max_length=255)
#     activo = models.BooleanField()
#
#     class Meta:
#         managed = True
#         db_table = 'cos_partida'
#
# class CosSubElementoGasto(models.Model):
#     idsubelemento = models.AutoField(primary_key=True)
#     codigo = models.CharField(max_length=50)
#     descripcion = models.CharField(max_length=255)
#     activo = models.BooleanField()
#     idelementogasto = models.ForeignKey('CosElementoGasto', models.DO_NOTHING, db_column='idelementogasto')
#     idpartida = models.ForeignKey('CosPartida', models.DO_NOTHING, db_column='idpartida')
#
#     class Meta:
#         managed = True
#         db_table = 'cos_subelementogasto'
