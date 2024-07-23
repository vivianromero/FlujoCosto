from __future__ import unicode_literals
from ast import literal_eval
from django import template

from codificadores.models import Departamento
from django.conf import settings

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
    if 16 in arg_list and value == 16 and settings.OTRAS_CONFIGURACIONES and 'Sistema Centralizado' in settings.OTRAS_CONFIGURACIONES.keys():
        return not settings.OTRAS_CONFIGURACIONES['Sistema Centralizado']['activo']
    return value not in arg_list
