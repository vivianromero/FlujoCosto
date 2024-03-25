# views.py
import json
import os
import tarfile
from tarfile import ReadError

from django.conf import settings
from django.shortcuts import redirect

from codificadores.models import Medida, UnidadContable, MedidaConversion
from cruds_adminlte3.utils import crud_url_name
from utiles.decorators import adminempresa_required
from utiles.utils import message_success, message_error
from utiles.utils import obtener_version, codificar
from django.core.management import call_command


# @adminempresa_required
def uc_importar(request):
    # TODO funcion para que me devuelva el fichero, siempre debe de estar en
    # staticfiles/upload
    filename="Exportando_UC_1-0-241101_SisGestFC.tar.gz"
    file_path = settings.STATIC_ROOT
    archivo_importar = os.path.join(file_path, 'upload', filename)
    data = importar_datos_desde_tar(request, archivo_importar, 'UC')
    return redirect(crud_url_name(UnidadContable, 'list', 'app_index:codificadores:'))

@adminempresa_required
def um_importar(request):
    # TODO funcion para que me devuelva el fichero, siempre debe de estar en
    # staticfiles/upload
    filename="Exportando_UM_1-0-241101_SisGestFC.tar.gz"
    # filename="data_K.tar.gz"
    file_path = settings.STATIC_ROOT
    archivo_importar = os.path.join(file_path, 'upload', filename)
    data = importar_datos_desde_tar(request, archivo_importar, 'UM')
    return redirect(crud_url_name(Medida, 'list', 'app_index:codificadores:'))

@adminempresa_required
def umc_importar(request):
    # TODO funcion para que me devuelva el fichero, siempre debe de estar en
    # staticfiles/upload
    filename="Exportando_UMC_1-0-241101_SisGestFC.tar.gz"
    # filename="data_K.tar.gz"
    file_path = settings.STATIC_ROOT
    archivo_importar = os.path.join(file_path, 'upload', filename)
    data = importar_datos_desde_tar(request, archivo_importar, 'UMC')
    return redirect(crud_url_name(MedidaConversion, 'list', 'app_index:codificadores:'))


# @adminempresa_required
# def umc_importar(request):
#     return simple_upload(request)
#
# @adminempresa_required
# def ms_importar(request):
#     return crear_export_file(request, 'MS', MarcaSalida)

def importar_datos_desde_tar(request, archivo_tar, opcion):
    try:
        with tarfile.open(archivo_tar, 'r') as tar:
            for miembro in tar.getmembers():
                if miembro.isfile():
                    contenido = tar.extractfile(miembro)
                    datos_json = json.load(contenido)
                    if contenido.name == 'json_verify':
                        datos_json_verify = datos_json
                        # check_sum_verify = codificar(datos_json_verify['opcion'] + datos_json_verify['version'])
                    else:
                        check_sum_datos = codificar(str(datos_json).replace("'", '"'))
                        # Procesa los datos según tus necesidades
            if valida_json_verify(request, datos_json_verify, check_sum_datos, opcion):
                filename = 'json_data_'+opcion.upper()+'.json'
                ruta_archivo = os.path.join('importar', 'fixtures', filename)
                fichero_json = open(ruta_archivo, "w+")
                fichero_json.write(str(datos_json).replace("'", '"'))
                fichero_json.close()
                call_command('loaddata', filename)
                message_success(request, "Success", "Importación terminada con éxito")
    except ReadError:
        message_error(request, 'Incorrect format', 'The file is not of type tar.gz')
    except FileNotFoundError:
        message_error(request, 'File not found', "The file doesn't exist")
    except Exception as e:
        message_error(request, 'File not found', "The file doesn't exist")
    except:
        message_error(request, 'File Error', "The file doesn't exist or is corrupt")

def valida_json_verify(request, json_verify, check_sum_data, opcion):
    if json_verify['opcion'].upper() != opcion.upper():
        message_error(request, "Error", "La información de este fichero no contiene los datos para la opción seleccionada")
        return False
    if json_verify['version'] != obtener_version():
        message_error(request, "Error", "La versión del sistema no se corresponde con la del fichero a importar")
        return False

    check_sum = codificar(json_verify['opcion'] + json_verify['version'])
    if json_verify['check_sum'] != check_sum or json_verify['check_sum_data'] != check_sum_data:
        message_error(request, "Error", "Los datos han sido modificados, no se podrán importar")
        return False
    return True

# def subir_archivo(request):
#     if request.method == 'POST':
#         importar_datos_desde_tar(archivo_tar.temporary_file_path())
#
#     return render(request, 'subir_fichero.html', context={})

# def simple_upload(request):
#     if request.method == 'POST' and request.FILES['myfile']:
#         myfile = request.FILES['myfile']
#         fs = FileSystemStorage()
#         filename = fs.save(myfile.name, myfile)
#         uploaded_file_url = fs.url(filename)
#         return render(request, 'core/simple_upload.html', {
#             'uploaded_file_url': uploaded_file_url
#         })
#     return render(request, 'core/simple_upload.html')

# def json_info(opcion):
#     version = obtener_version()
#     check_sum = codificar(opcion + version)
#     dicc_valid = {'opcion': opcion,
#                   'version': version,
#                   'check_sum': check_sum}
#     return dicc_valid
#
# def crear_export_file(request, opcion, modelo):
#
#     dicc_verify = json_info(opcion)
#     file_path = "staticfiles"
#
#     json_data = serializers.serialize("json", modelo.objects.all())
#     check_sum_data = codificar(json_data)
#     dicc_verify['check_sum_data'] = check_sum_data
#
#     if len(json_data) <= 2:
#         message_success(request=request, title=_("Warning"), text=_("There aren't data to export"))
#         return redirect(crud_url_name(modelo, 'list', 'app_index:codificadores:'))
#
#     encoder = json.encoder.JSONEncoder()
#     json_verify = encoder.encode(dicc_verify)
#
#     filenameverify = 'verify_' + dicc_verify['opcion'] + '.json'
#     ruta_archivo_verify = os.path.join(file_path, 'download', filenameverify)
#     fichero_json = open(ruta_archivo_verify, "w+")
#     fichero_json.write(json_verify)
#     fichero_json.close()
#
#     filenamedata = 'data_'+ dicc_verify['opcion'] + '.json'
#     ruta_archivo_data = os.path.join(file_path, 'download', filenamedata)
#     file_json_data = open(ruta_archivo_data, "w+")
#     file_json_data.write(json_data)
#     file_json_data.close()
#
#     filename = "Exportando_" + dicc_verify['opcion'] + '_' + dicc_verify['version'].replace('.', '-') + ".tar.gz"
#     ruta_archivo = os.path.join(file_path, 'download', filename)
#     with tarfile.open(ruta_archivo, mode='w:bz2') as out:
#         out.add(ruta_archivo_verify, "json_verify")
#         out.add(ruta_archivo_data, "json_data")
#
#
#     # Configuración de la respuesta HTTP para la descarga del archivo
#     response = HttpResponse(open(ruta_archivo, 'rb'), content_type='application/gzip')
#     response['Content-Disposition'] = f'attachment; filename={filename}'
#     return response

