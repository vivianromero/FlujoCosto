from __future__ import unicode_literals

from codificadores.models import Departamento, ProductoFlujo
from codificadores import ChoiceTiposProd
from django import template

from flujo.tables import DocumentosVersatDetalleTable

register = template.Library()


@register.simple_tag
def get_documento_versat_detalle_table(table_class=None, detalle=None):
    if detalle:
        codigos_versat = [p['producto_codigo'] for p in detalle]
        productos = ProductoFlujo.objects.filter(codigo__in=codigos_versat).all()
        codigos_sistema = [p.codigo for p in productos]
        for d in detalle:
            d['existe_sistema'] = d['producto_codigo'] in codigos_sistema
    return DocumentosVersatDetalleTable(detalle) if detalle and table_class else None
