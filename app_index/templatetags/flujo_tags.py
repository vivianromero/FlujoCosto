from __future__ import unicode_literals

from codificadores.models import Departamento
from django import template

from flujo.tables import DocumentosVersatDetalleTable

register = template.Library()


@register.simple_tag
def get_documento_versat_detalle_table(table_class=None, detalle=None):
    return DocumentosVersatDetalleTable(detalle) if detalle and table_class else None
