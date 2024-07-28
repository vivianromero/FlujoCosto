from __future__ import unicode_literals

from ast import literal_eval

from django import template
from django.conf import settings

from codificadores import ChoiceTiposDoc
from codificadores.models import Departamento

register = template.Library()


@register.simple_tag
def is_initialized(departamento, ueb):
    return Departamento.inicializado(departamento, ueb)


@register.simple_tag
def get_departamento_name(departamento):
    return Departamento.objects.get(id=departamento).descripcion if departamento else None


@register.simple_tag
def get_departamento_object(departamento):
    return Departamento.objects.get(id=departamento) if departamento else None


@register.simple_tag
def not_in(value, arg_list):
    arg_list = literal_eval(arg_list)
    if ChoiceTiposDoc.RECIBIR_TRANS_EXTERNA in arg_list and value == ChoiceTiposDoc.RECIBIR_TRANS_EXTERNA and settings.OTRAS_CONFIGURACIONES and 'Sistema Centralizado' in settings.OTRAS_CONFIGURACIONES.keys():
        return not settings.OTRAS_CONFIGURACIONES['Sistema Centralizado']['activo']
    if value and int(value) == ChoiceTiposDoc.ENTRADA_DESDE_VERSAT:
        return False
    return value not in arg_list
