from django.apps import AppConfig
from django.conf import settings


class FlujoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'flujo'

    def ready(self):
        import flujo.signals
        try:
            from utiles.utils import get_fechas_procesamiento_inicio, get_configuracion_numeracion, \
                get_otras_configuraciones
            settings.NUMERACION_DOCUMENTOS_CONFIG = get_configuracion_numeracion()
            settings.FECHAS_PROCESAMIENTO = get_fechas_procesamiento_inicio()
            settings.OTRAS_CONFIGURACIONES = get_otras_configuraciones()
        except Exception as e:
            print(f"No se han creado los modelos aún")
