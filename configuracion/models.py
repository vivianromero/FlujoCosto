import uuid
from django.db import models
from django.contrib.auth.models import User
from codificadores.models import UnidadContable, Departamento, TipoDocumento, NumeracionDocumentos


class Ueb(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    idunidadcontable = models.ForeignKey(UnidadContable, on_delete=models.PROTECT)

    class Meta:
        db_table = 'cfg_ueb'

class ConexionBaseDato(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    database_name = models.CharField(max_length=250)
    database_user = models.CharField(max_length=250)
    password = models.CharField(max_length=250)
    host = models.CharField(max_length=250)
    port = models.CharField(max_length=100)
    idueb = models.ForeignKey(Ueb, on_delete=models.PROTECT)

    class Meta:
        db_table = 'cfg_conexionasedato'
        unique_together = (('database_name', 'idueb'),)

class ConsecutivoDocumento(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    idnumeraciondocumento = models.ForeignKey(NumeracionDocumentos, on_delete=models.PROTECT, related_name='consecutivodocumento_numeracion')
    numero = models.IntegerField()
    prefijo = models.CharField(max_length=3, blank=True, null=True)
    idueb = models.ForeignKey(Ueb, on_delete=models.PROTECT, related_name='consecutivo_ueb')

    class Meta:
        db_table = 'cfg_consecutivodocumento'

class ConsecutivoDocumentoDepartamento(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    idconsecutivodocumento = models.ForeignKey(ConsecutivoDocumento, on_delete=models.CASCADE, related_name='consecutivodocumentodpto_consecutivodocumento')
    iddepartamento = models.ForeignKey(Departamento, on_delete=models.PROTECT, related_name='consecutivodocumentodpto_departamento')

    class Meta:
        db_table = 'cfg_consecutivodocumentodepartamento'

class ConsecutivoDocumentoTipoDocumento(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    idconsecutivodocumento = models.ForeignKey(ConsecutivoDocumento, on_delete=models.CASCADE, related_name='consecutivodocumentotipodoc_consecutivodocumento')
    idtipodocumento = models.ForeignKey(TipoDocumento, on_delete=models.PROTECT, related_name='consecutivodocumentotipodoc_tipodocumento')

    class Meta:
        db_table = 'cfg_consecutivodocumentotipodocumento'

class UserUeb(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    idueb = models.ForeignKey(Ueb, on_delete=models.PROTECT, related_name='ueb_user')
    iduser = models.ForeignKey(User, on_delete=models.PROTECT, related_name='user_ueb')

    class Meta:
        db_table = 'cfg_userueb'
