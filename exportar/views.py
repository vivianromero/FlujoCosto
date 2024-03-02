# views.py
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required

@login_required
def uc_exportar(request):
    # Lógica para generar el contenido del archivo (por ejemplo, usando pandas)
    contenido_archivo = "Contenido del archivo a exportar"

    # Configuración de la respuesta HTTP para la descarga del archivo
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="archivo_exportado_uc.csv"'

    # Escribir el contenido del archivo en la respuesta
    response.write(contenido_archivo)
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

    # Configuración de la respuesta HTTP para la descarga del archivo
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="archivo_exportado_umc.csv"'

    # Escribir el contenido del archivo en la respuesta
    response.write(contenido_archivo)
    return response
