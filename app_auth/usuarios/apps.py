from django.apps import AppConfig


class UsuariosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_auth.usuarios'

    def ready(self):
        import app_auth.usuarios.signals
