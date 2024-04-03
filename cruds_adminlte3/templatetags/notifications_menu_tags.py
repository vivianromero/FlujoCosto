from django.template import Library
from django.utils.html import format_html


register = Library()

@register.simple_tag
def live_notify_dropdown_list(list_class='live_notify_list'):
    html = "<div class='{list_class}'></div>".format(list_class=list_class)
    return format_html(html)
