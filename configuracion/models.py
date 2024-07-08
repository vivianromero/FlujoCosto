import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from codificadores.models import UnidadContable
from cruds_adminlte3.utils import crud_url
from . import ChoiceSystems


class ConexionBaseDato(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    database_name = models.CharField(max_length=250, verbose_name=_("Database Name"))
    database_user = models.CharField(max_length=250, verbose_name=_("User Name"))
    password = models.CharField(max_length=250, verbose_name=_("Password"))
    host = models.CharField(max_length=250, verbose_name=_("Host"))
    port = models.CharField(max_length=100, verbose_name=_("Port"))
    unidadcontable = models.ForeignKey(UnidadContable, on_delete=models.PROTECT, verbose_name="UEB")
    sistema = models.CharField(choices=ChoiceSystems.CHOICE_SYSTEMS, default=ChoiceSystems.VERSATSARASOLA,
                               verbose_name=_("System"))

    class Meta:
        db_table = 'cfg_conexionbasedato'
        indexes = [
            models.Index(
                fields=[
                    'unidadcontable',
                    'sistema',
                ]
            ),
        ]
        ordering = ['unidadcontable__codigo', 'sistema']
        verbose_name_plural = _('Conexions of data bases')
        verbose_name = _('Database conexion')
        constraints = [
            models.UniqueConstraint(
                fields=['unidadcontable', 'sistema'],
                name='unique_conexionbasedato_unidadcontable_sistema'
            ),
        ]


    def __str__(self):
        return "%s - %s" % (self.sistema, self.database_name)


class UserUeb(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ueb = models.ForeignKey(UnidadContable, on_delete=models.PROTECT, null=True,
                            blank=True, verbose_name='UEB')

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return crud_url(self, 'update', namespace='app_index:userueb')

    class Meta:
        db_table = 'cfg_userueb'
        indexes = [
            models.Index(
                fields=[
                    'username',
                    'email',
                    'ueb',
                    'last_login',
                ]
            ),
        ]
        ordering = ('ueb', 'username', 'pk')
        verbose_name_plural = _('Users')
        verbose_name = _('User')

    @property
    def is_admin(self):
        return self.groups.filter(name="Administrador").exists()

    @property
    def is_operflujo(self):
        return self.groups.filter(name="Operador Flujo").exists()

    @property
    def is_opercosto(self):
        return self.groups.filter(name="Operador Costo").exists()

    @property
    def is_consultor(self):
        return self.groups.filter(name="Consultor").exists()

    @property
    def is_adminempresa(self):
        return self.groups.filter(name="Administrador Empresa").exists() and self.ueb and self.ueb.is_empresa

    @property
    def is_consultoremp(self):
        return self.groups.filter(name="Consultor").exists() and self.ueb and self.ueb.is_empresa


# Model to store the list of logged-in users
class LoggedInUser(models.Model):
    user = models.OneToOneField(UserUeb, related_name='logged_in_user', on_delete=models.CASCADE)
    # Session keys are 32 characters long
    session_key = models.CharField(max_length=32, null=True, blank=True)

    def __str__(self):
        return self.user.username
