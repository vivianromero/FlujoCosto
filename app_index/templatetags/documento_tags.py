from __future__ import unicode_literals

from ast import literal_eval

from django import template

from codificadores import ChoiceTiposDoc

register = template.Library()


@register.simple_tag
def is_in(value, arg_list):
    arg_list = literal_eval(arg_list)
    if value.tipodocumento.pk == ChoiceTiposDoc.ENTRADA_DESDE_VERSAT:
        return False
    return value.estado in arg_list
