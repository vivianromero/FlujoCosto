from __future__ import unicode_literals

from codificadores.models import Departamento
from django import template

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
