# views.py
import json
import os
import tarfile
from tarfile import ReadError
from tkinter import filedialog

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.management import call_command
from django.shortcuts import redirect

from codificadores.models import Medida, UnidadContable, MedidaConversion, MarcaSalida, CentroCosto, Cuenta, \
    Departamento, ProductoFlujo, CambioProducto, Vitola, LineaSalida, NumeracionDocumentos, ConfCentrosElementosOtros, MotivoAjuste
from cruds_adminlte3.utils import crud_url_name
from utiles.utils import message_success, message_error
from utiles.utils import obtener_version, codificar


def importacion(request, opcion, modelo):
    archivo_importar = obtener_fichero()
    if archivo_importar:
        data = importar_datos_desde_tar(request, archivo_importar, opcion)
    return redirect(crud_url_name(modelo, 'list', 'app_index:codificadores:'))


@login_required
def uc_importar(request):
    return importacion(request, 'UC', UnidadContable)


@login_required
def um_importar(request):
    return importacion(request, 'UM', Medida)


@login_required
def ms_importar(request):
    return importacion(request, 'MS', MarcaSalida)

@login_required
def ma_importar(request):
    return importacion(request, 'MotAjus', MotivoAjuste)


@login_required
def umc_importar(request):
    return importacion(request, 'UMC', MedidaConversion)


@login_required
def cc_importar(request):
    return importacion(request, 'CC', CentroCosto)


@login_required
def ccta_importar(request):
    return importacion(request, 'CCTA', Cuenta)


@login_required
def dpto_importar(request):
    return importacion(request, 'DPTO', Departamento)


@login_required
def prod_importar(request):
    return importacion(request, 'PROD', ProductoFlujo)

@login_required
def cprod_importar(request):
    return importacion(request, 'CambioPROD', CambioProducto)

@login_required
def vit_importar(request):
    return importacion(request, 'VIT', Vitola)

@login_required
def ls_importar(request):
    return importacion(request, 'LS', LineaSalida)

@login_required
def numdoc_importar(request):
    return importacion(request, 'NumDoc', NumeracionDocumentos)

@login_required
def confccelemg_importar(request):
    return importacion(request, 'ConfCCEleG', ConfCentrosElementosOtros)


def importar_datos_desde_tar(request, archivo_tar, opcion):
    try:
        with tarfile.open(archivo_tar, 'r') as tar:
            for miembro in tar.getmembers():
                if miembro.isfile():
                    contenido = tar.extractfile(miembro)
                    datos_json = json.load(contenido)
                    if contenido.name == 'json_verify':
                        datos_json_verify = datos_json
                    else:
                        check_sum_datos = codificar(json.dumps(datos_json, ensure_ascii=False))
            if valida_json_verify(request, datos_json_verify, check_sum_datos, opcion):
                filename = 'json_data_' + opcion.upper() + '.json'
                ruta_archivo = os.path.join('importar', 'fixtures', filename)
                fichero_json = open(ruta_archivo, "w+")
                fichero_json.write(json.dumps(datos_json))
                fichero_json.close()
                call_command('loaddata', filename)
                message_success(request, "Success", "Importación terminada con éxito")
    except ReadError:
        message_error(request, 'Incorrect format', 'The file is not of type tar.gz')
    except FileNotFoundError:
        message_error(request, 'File not found', "The file doesn't exist")
    except Exception as e:
        message_error(request, 'Data Error', "Error en los datos a importar")
    except:
        message_error(request, 'File Error', "The file doesn't exist or is corrupt")


def valida_json_verify(request, json_verify, check_sum_data, opcion):
    if json_verify['opcion'].upper() != opcion.upper():
        message_error(request, "Error",
                      "La información de este fichero no contiene los datos para la opción seleccionada")
        return False
    if json_verify['version'] != obtener_version():
        message_error(request, "Error", "La versión del sistema no se corresponde con la del fichero a importar")
        return False

    check_sum = codificar(json_verify['opcion'] + json_verify['version'])
    if json_verify['check_sum'] != check_sum or json_verify['check_sum_data'] != check_sum_data:
        message_error(request, "Error", "Los datos han sido modificados, no se podrán importar")
        return False
    return True


def obtener_fichero():
    file_path = settings.MEDIA_ROOT_UPLOAD_FILES
    archivo_importar = filedialog.askopenfilename(
        initialdir=file_path,
        title="Seleccione el fichero",
        filetypes=[("Ficheros a importar", "*.tar.gz"), ("All files", "*.*")]
    )
    return archivo_importar
