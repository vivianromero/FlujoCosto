from app_index.views import BaseModalFormView
from reports.reports import ReportGenerator
from .reportsforms import *
from .utils import dame_fecha
from django.http import HttpResponse, HttpResponseServerError, JsonResponse
import json

def genera_report(kwargs):
    departamento = kwargs['departamento']
    estados = kwargs['estados']
    ueb = kwargs['request'].user.ueb
    fecha_procesamiento_fin = dame_fecha(ueb, departamento)
    fecha_procesamiento_init = fecha_procesamiento_fin.replace(day=1)
    param_periodo = f"Del {fecha_procesamiento_init.strftime('%d/%m/%Y')} al {fecha_procesamiento_fin.strftime('%d/%m/%Y')}"

    if '0' in estados:
        estados.remove('0')
    param_estado = ','.join(estados)

    parameters = {
        'param_ueb_id': str(ueb.pk),
        'param_departamento_id': str(departamento.pk),
        'param_estado': param_estado if param_estado else None,
        'param_periodo': param_periodo,
        'param_fechai': '2024-01-01',
        'param_fechaf': '2024-01-31'
    }
    report_name = kwargs.get('report_name', '')
    report_generator = ReportGenerator(report_name, output_formats=['pdf'])
    generado = report_generator.generate_report(parameters)
    return json.loads(generado.content)


def loadreport(kwargs):
    func_ret = {
        'success': True,
        'errors': {},
        'success_title': 'Report Generado con Éxito',
        'error_title': '',
    }

    generado = genera_report(kwargs)
    if generado.get('error', False):
        func_ret.update({
            'success': False,
            'error_title': "Se ha producido un error al generar el reporte"
        })
    return func_ret


class ReportModalFormView(BaseModalFormView):
    template_name = 'app_index/modals/modal_form.html'
    form_class = ReportExistenciaForm
    father_view = 'app_index:index'
    hx_target = '#body'
    hx_swap = 'outerHTML'
    hx_retarget = '#dialog'
    hx_reswap = 'outerHTML'
    modal_form_title = ''
    max_width = '850px'

    funcname = {
        'submitted': loadreport,
    }

    close_on_error = True

    def get_context_data(self, **kwargs):
        # fecha = self.request.GET.get('fecha', None)
        context = super().get_context_data(**kwargs)
        dep_queryset = context['form'].fields['departamento'].queryset
        ueb = self.request.user.ueb
        dep_queryset = dep_queryset.filter(unidadcontable=ueb)
        context['form'].fields['departamento'].queryset = dep_queryset
        return context

    def get_fields_kwargs(self, form):
        kw = {}
        kw.update({
            'request': self.request,
            'departamento': form.cleaned_data['departamento'],
            'estados': form.cleaned_data['estados'],
            'report_name': self.report_name,
        })

        return kw

class ReportExistenciaModalFormView(ReportModalFormView):
    modal_form_title = 'Reporte de Existencia'
    report_name = 'Reporte de Existencias'

class ReportMovimientoModalFormView(ReportModalFormView):
    modal_form_title = 'Reporte de Movimiento'
    report_name = 'Reporte de Movimiento'


