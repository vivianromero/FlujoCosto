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
        constraints = [
            models.UniqueConstraint(
                fields=['clave', 'idapertura'],
                name='unique_centro_clave_idapertura'
            ),
            models.UniqueConstraint(
                fields=['idapertura', 'clavenivel'],
                name='unique_centro_idapertura_clavenivel'
            ),
        ]

