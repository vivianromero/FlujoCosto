# views.py
import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from utiles.utils import obtener_version, codificar


@login_required
def uc_exportar(request):
    # Lógica para generar el contenido del archivo (por ejemplo, usando pandas)
    contenido_archivo = "Contenido del archivo a exportar"

    json_verify = json_info('UC')

    # Configuración de la respuesta HTTP para la descarga del archivo
    response = HttpResponse(content_type='text/json')
    response['Content-Disposition'] = 'attachment; filename="archivo_exportado_uc.json"'

    # Escribir el contenido del archivo en la respuesta
    response.write(json_verify)
    return response

@login_required
def um_exportar(request):
    # Lógica para generar el contenido del archivo (por ejemplo, usando pandas)
    contenido_archivo = "Contenido del archivo a exportar"

    # Configuración de la respuesta HTTP para la descarga del archivo
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="archivo_exportado_um.csv"'

    # Escribir el contenido del archivo en la respuesta
    response.write(contenido_archivo)
    return response

@login_required
def umc_exportar(request):
    # Lógica para generar el contenido del archivo (por ejemplo, usando pandas)
    contenido_archivo = "Contenido del archivo a exportar"

    app_version_file = open('version', 'r')

    # Configuración de la respuesta HTTP para la descarga del archivo
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="archivo_exportado_umc.csv"'

    # Escribir el contenido del archivo en la respuesta
    response.write(contenido_archivo)
    return response

def json_info(opcion):
    version = obtener_version()
    check_sum = codificar(opcion + version)
    dicc_valid = {'opcion': opcion,
                  'version': version,
                  'check_sum': check_sum}
    encoder = json.encoder.JSONEncoder()
    # json_info = encoder.encode(dicc_valid)
    return encoder.encode(dicc_valid)

