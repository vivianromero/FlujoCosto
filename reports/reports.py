import os
from django.conf import settings
from django.http import HttpResponse, HttpResponseServerError, JsonResponse
from pyreportjasper import PyReportJasper

import os
from django.conf import settings
from django.http import HttpResponse, HttpResponseServerError
from pyreportjasper import PyReportJasper
from django.http import FileResponse
from django.urls import reverse
from django.core.cache import cache
from django.shortcuts import redirect


def ver_pdf(request):
    data_report = cache.get_many(['report_name', 'path_report', 'format_report', 'report_error'])
    if data_report:
        if data_report['report_error']:
            return redirect(reverse('app_index:error_generatereport'))
        file_extension = data_report['format_report'][0]
        report_name = data_report['report_name']
        pdf_path = data_report['path_report'] + '.' + file_extension

        with open(pdf_path, 'rb') as pdf_file:
            pdf_data = pdf_file.read()

        response = HttpResponse(pdf_data, content_type=f'application/{file_extension}')
        response['Content-Disposition'] = f'inline; filename={report_name}'
        return response
    return HttpResponse("""No existen datos para mpstrar""")


class ReportGenerator:
    def __init__(self, report_name, output_formats=None, ueb=None, user=None):
        self.report_name = report_name
        self.output_formats = output_formats if output_formats else ["pdf"]
        self.input_file = os.path.join(settings.REPORTS_DIR, f'{report_name}.jrxml')
        report_name_output = report_name
        report_name_output = report_name_output + "_" + ueb.codigo+'-'+ueb.nombre+'_' if ueb else report_name_output
        report_name_output = report_name_output + "_" + user.username if user else report_name_output

        self.output_file = os.path.join(settings.REPORTS_OUTPUT, report_name_output)
        self.pyreportjasper = PyReportJasper()

        db_settings = settings.DATABASES['default']
        self.conn = {
            'jdbc_driver': 'org.postgresql.Driver',
            'driver': 'postgres',
            'username': db_settings['USER'],
            'password': db_settings['PASSWORD'],
            'host': db_settings['HOST'],
            'database': db_settings['NAME'],
            'port': db_settings.get('PORT', '5432')
        }

        cache.set_many(
            {'report_name': self.report_name,
             'path_report': self.output_file,
             'format_report': self.output_formats,
             'report_error': False},
            timeout=None
        )

    def generate_report(self, parameters, locale='en_US'):
        try:
            # Configura el reporte
            self.pyreportjasper.config(
                input_file=self.input_file,
                output_file=self.output_file,
                db_connection=self.conn,
                output_formats=self.output_formats,
                parameters=parameters,
                locale=locale
            )

            # Procesa el reporte
            self.pyreportjasper.process_report()

            # pdf_path = f'{output_file}.pdf'

            # Enviar la URL del PDF como JSON
            # response_data = {
            #     'pdf_path': self.output_file,
            #     'url': reverse('app_index:reportes:ver_pdf')
            # }
            return JsonResponse({})
            # Retorna la respuesta HTTP con el archivo generado
            # return self.get_http_response()
        except Exception as e:
            # Captura cualquier error durante la generación del reporte
            # return HttpResponseServerError(f"Error al generar el reporte: {str(e)}")
            cache.set('report_error', True)
            return JsonResponse({'error':str(e)})

    # def get_http_response(self):
    #     try:
    #         # Por defecto se genera un archivo en el primer formato indicado
    #         file_extension = self.output_formats[0]
    #         output_file = f"{self.output_file}.{file_extension}"
    #
    #         # Leer el archivo generado
    #         with open(output_file, 'rb') as file:
    #             response = HttpResponse(file.read(), content_type=f'application/{file_extension}')
    #
    #             # response = FileResponse(open(output_file, 'rb'), content_type='application/pdf')
    #             # El encabezado 'inline' permite que el navegador intente abrir el archivo en la misma pestaña
    #             # response['Content-Disposition'] = f'inline; filename="{self.report_name}.{file_extension}"'
    #             response['Content-Disposition'] = f'attachment; filename="{self.report_name}.{file_extension}"'
    #             return response
    #     except FileNotFoundError:
    #         return HttpResponseServerError("El archivo de reporte no fue encontrado.")
    #     except Exception as e:
    #         return HttpResponseServerError(f"Ha ocurrido un error al leer el archivo de reporte: {str(e)}")
