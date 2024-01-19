import uuid
from django.db import models
from django.contrib.auth.models import User
from codificadores.models import UnidadContable, Departamento, TipoDocumento, NumeracionDocumentos
from cruds_adminlte3.utils import crud_url


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
    idnumeraciondocumento = models.ForeignKey(NumeracionDocumentos, on_delete=models.PROTECT,
                                              related_name='consecutivodocumento_numeracion')
    numero = models.IntegerField()
    idueb = models.ForeignKey(Ueb, on_delete=models.PROTECT, related_name='consecutivo_ueb')

    class Meta:
        db_table = 'cfg_consecutivodocumento'


class ConsecutivoDocumentoDepartamento(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    idconsecutivodocumento = models.ForeignKey(ConsecutivoDocumento, on_delete=models.CASCADE,
                                               related_name='consecutivodocumentodpto_consecutivodocumento')
    iddepartamento = models.ForeignKey(Departamento, on_delete=models.PROTECT,
                                       related_name='consecutivodocumentodpto_departamento')

    class Meta:
        db_table = 'cfg_consecutivodocumentodepartamento'


class ConsecutivoDocumentoTipoDocumento(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    idconsecutivodocumento = models.ForeignKey(ConsecutivoDocumento, on_delete=models.CASCADE,
                                               related_name='consecutivodocumentotipodoc_consecutivodocumento')
    idtipodocumento = models.ForeignKey(TipoDocumento, on_delete=models.PROTECT,
                                        related_name='consecutivodocumentotipodoc_tipodocumento')

    class Meta:
        db_table = 'cfg_consecutivodocumentotipodocumento'


class UserUeb(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    idueb = models.ForeignKey(Ueb, on_delete=models.PROTECT, related_name='ueb_user')
    iduser = models.ForeignKey(User, on_delete=models.PROTECT, related_name='user_ueb')

    def __str__(self):
        return self.iduser.username

    def get_absolute_url(self):
        return crud_url(self, 'update', namespace='app_index:userueb')

    class Meta:
        db_table = 'cfg_userueb'


# Model to store the list of logged-in users
class LoggedInUser(models.Model):
    user = models.OneToOneField(User, related_name='logged_in_user', on_delete=models.CASCADE)
    # Session keys are 32 characters long
    session_key = models.CharField(max_length=32, null=True, blank=True)

    def __str__(self):
        return self.user.username
