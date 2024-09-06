import os
from django.conf import settings
from django.http import HttpResponse, HttpResponseServerError, JsonResponse
from pyreportjasper import PyReportJasper

import os
from django.conf import settings
from django.http import HttpResponse, HttpResponseServerError
from pyreportjasper import PyReportJasper
from django.http import FileResponse


class ReportGenerator:
    def __init__(self, report_name, output_formats=None):
        self.report_name = report_name
        self.output_formats = output_formats if output_formats else ["pdf"]
        self.input_file = os.path.join(settings.REPORTS_DIR, f'{report_name}.jrxml')
        self.output_file = os.path.join(settings.REPORTS_OUTPUT, report_name)
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

            # Retorna la respuesta HTTP con el archivo generado
            return self.get_http_response()

        except Exception as e:
            # Captura cualquier error durante la generación del reporte
            return HttpResponseServerError(f"Error al generar el reporte: {str(e)}")

    def get_http_response(self):
        try:
            # Por defecto se genera un archivo en el primer formato indicado
            file_extension = self.output_formats[0]
            output_file = f"{self.output_file}.{file_extension}"

            # Leer el archivo generado
            with open(output_file, 'rb') as file:
                # response = HttpResponse(file.read(), content_type=f'application/{file_extension}')
                response = FileResponse(open(output_file, 'rb'), content_type='application/pdf')
                # El encabezado 'inline' permite que el navegador intente abrir el archivo en la misma pestaña
                response['Content-Disposition'] = f'inline; filename="{self.report_name}.{file_extension}"'
                return response
        except FileNotFoundError:
            return HttpResponseServerError("El archivo de reporte no fue encontrado.")
        except Exception as e:
            return HttpResponseServerError(f"Ha ocurrido un error al leer el archivo de reporte: {str(e)}")