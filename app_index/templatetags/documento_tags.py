from __future__ import unicode_literals

from ast import literal_eval

from django import template

register = template.Library()


@register.simple_tag
def is_in(value, arg_list):
    arg_list = literal_eval(arg_list)
    return value.estado in arg_list
