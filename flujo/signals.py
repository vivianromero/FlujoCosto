from django.db.models.signals import pre_save
from django.dispatch import receiver

from flujo.models import Documento


@receiver(pre_save, sender=Documento)
def actualiza_anno_mes(sender, instance, **kwargs):
    instance.mes = instance.fecha.month
    instance.anno = instance.fecha.year



