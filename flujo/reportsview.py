from app_index.views import BaseModalFormView
from reports.reports import ReportGenerator
from .reportsforms import *
from .utils import dame_fecha


def repexistencia(kwargs):
    func_ret = {
        'success': True,
        'errors': {},
        'success_title': 'Report ok',
        'error_title': '',
    }
    report_generator = ReportGenerator('Reporte de Existencias', output_formats=['xlsx'])
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
        'param_estado':param_estado if param_estado else None,
        'param_periodo': param_periodo
    }
    report_generator.generate_report(parameters)
    return  {
        'success': True,
        'errors': {},
        'success_title': 'Report ok',
        'error_title': '',
    }


class ReportExistenciaModalFormView(BaseModalFormView):
    template_name = 'app_index/modals/modal_form.html'
    form_class = ReportExistenciaForm
    father_view = 'app_index:index'
    hx_target = '#body'
    hx_swap = 'outerHTML'
    hx_retarget = '#dialog'
    hx_reswap = 'outerHTML'
    modal_form_title = 'Reporte de Existencia'
    max_width = '850px'
    funcname = {
        'submitted': repexistencia,
    }
    # funcname = {}
    # viewname = {
    #     'submitted': 'app_index:flujo:repexistencia',
    # }
    close_on_error = True

    def get_context_data(self, **kwargs):
        # fecha = self.request.GET.get('fecha', None)
        context = super().get_context_data(**kwargs)
        dep_queryset = context['form'].fields['departamento'].queryset
        ueb = self.request.user.ueb
        dep_queryset = dep_queryset.filter(unidadcontable=ueb)
        context['form'].fields['departamento'].queryset = dep_queryset
        # context.update({
        #     'btn_generar_doc': 'Generar Documento',
        # })
        return context

    def get_fields_kwargs(self, form):
        kw = {}
        kw.update({
            'request': self.request,
            'departamento': form.cleaned_data['departamento'],
            'estados': form.cleaned_data['estados'],
        })
        # if self.request.POST['event_action'] in ['submitted']:
        #     kw.update(
        #         {'departamento': form.cleaned_data['departamento']})
        return kw
