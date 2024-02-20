import uuid

from django.contrib.auth.models import User
from django.db import models

from codificadores.models import UnidadContable, Departamento, TipoDocumento, NumeracionDocumentos
from cruds_adminlte3.utils import crud_url
from django.utils.translation import gettext_lazy as _


# class Ueb(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     idunidadcontable = models.ForeignKey(UnidadContable, on_delete=models.PROTECT,
#                                          verbose_name="UEB")
#
#     class Meta:
#         db_table = 'cfg_ueb'


class ConexionBaseDato(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    database_name = models.CharField(max_length=250, verbose_name=_("Database Name"))
    database_user = models.CharField(max_length=250, verbose_name=_("User Name"))
    password = models.CharField(max_length=250, verbose_name=_("Password"))
    host = models.CharField(max_length=250, verbose_name=_("Host"))
    port = models.CharField(max_length=100, verbose_name=_("Port"))
    idunidadcontable = models.OneToOneField(UnidadContable, on_delete=models.PROTECT, verbose_name="UEB")

    class Meta:
        db_table = 'cfg_conexionasedato'

class ConsecutivoDocumento(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    idnumeraciondocumento = models.ForeignKey(NumeracionDocumentos, on_delete=models.PROTECT,
                                              related_name='consecutivodocumento_numeracion',
                                              verbose_name=_("Enumeration Type"))
    numero = models.IntegerField(verbose_name=_("Number"))
    idueb = models.ForeignKey(UnidadContable, on_delete=models.PROTECT, related_name='consecutivo_ueb', verbose_name="UEB")

    class Meta:
        db_table = 'cfg_consecutivodocumento'


class ConsecutivoDocumentoDepartamento(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    idconsecutivodocumento = models.ForeignKey(ConsecutivoDocumento, on_delete=models.CASCADE,
                                               related_name='consecutivodocumentodpto_consecutivodocumento')
    iddepartamento = models.ForeignKey(Departamento, on_delete=models.PROTECT,
                                       related_name='consecutivodocumentodpto_departamento',
                                       verbose_name=_("Department"))

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
    idueb = models.ForeignKey(UnidadContable, on_delete=models.PROTECT, related_name='ueb_user')
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
