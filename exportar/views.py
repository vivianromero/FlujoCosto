# views.py
import json
import os
import tarfile

from django.conf import settings
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _

from codificadores.models import UnidadContable, Medida, MedidaConversion, MarcaSalida, CentroCosto, Cuenta, \
    Departamento, ProductoFlujo, ProductoFlujoClase, CambioProducto
from cruds_adminlte3.utils import crud_url_name
from utiles.decorators import adminempresa_required
from utiles.utils import message_success
from utiles.utils import obtener_version, codificar


@adminempresa_required
def uc_exportar(request):
    return crear_export_file(request, 'UC', UnidadContable)


@adminempresa_required
def um_exportar(request):
    return crear_export_file(request, 'UM', Medida)


@adminempresa_required
def umc_exportar(request):
    return crear_export_file(request, 'UMC', MedidaConversion)


@adminempresa_required
def ms_exportar(request):
    return crear_export_file(request, 'MS', MarcaSalida)


@adminempresa_required
def cc_exportar(request):
    return crear_export_file(request, 'CC', CentroCosto)


@adminempresa_required
def ccta_exportar(request):
    return crear_export_file(request, 'CCTA', Cuenta)


@adminempresa_required
def dpto_exportar(request):
    return crear_export_file(request, 'DPTO', Departamento)


@adminempresa_required
def prod_exportar(request):
    return crear_export_file(request, 'PROD', ProductoFlujo)

@adminempresa_required
def cprod_exportar(request):
    return crear_export_file(request, 'CambioPROD', CambioProducto)

def json_info(opcion):
    version = obtener_version()
    check_sum = codificar(opcion + version)
    dicc_valid = {'opcion': opcion,
                  'version': version,
                  'check_sum': check_sum}
    return dicc_valid


def crear_export_file(request, opcion, modelo):
    dicc_verify = json_info(opcion)
    file_path = settings.STATIC_ROOT
    json_data = serializers.serialize("json", modelo.objects.all()).replace("true", '"True"').replace("false", '"False"')
    if opcion == 'PROD':
        json_data2 = serializers.serialize("json", ProductoFlujoClase.objects.all()).replace("true", '"True"').replace("false",
                                                                                                              '"False"')
        json_data = json_data.replace(']','') + json_data2.replace('[',', ')

    check_sum_data = codificar(json_data)
    dicc_verify['check_sum_data'] = check_sum_data

    if len(json_data) <= 2:
        message_success(request=request, title=_("Warning"), text=_("There aren't data to export"))
        return redirect(crud_url_name(modelo, 'list', 'app_index:codificadores:'))

    encoder = json.encoder.JSONEncoder()
    json_verify = encoder.encode(dicc_verify)

    filenameverify = 'verify_' + dicc_verify['opcion'] + '.json'
    ruta_archivo_verify = os.path.join(file_path, 'download', filenameverify)
    fichero_json = open(ruta_archivo_verify, "w+")
    fichero_json.write(json_verify)
    fichero_json.close()

    filenamedata = 'data_' + dicc_verify['opcion'] + '.json'
    ruta_archivo_data = os.path.join(file_path, 'download', filenamedata)
    file_json_data = open(ruta_archivo_data, "w+")
    file_json_data.write(json_data)
    file_json_data.close()

    filename = "Exportando_" + dicc_verify['opcion'] + '_' + dicc_verify['version'].replace('.',
                                                                                            '-') + "_SisGestFC.tar.gz"
    ruta_archivo = os.path.join(file_path, 'download', filename)
    with tarfile.open(ruta_archivo, mode='w:bz2') as out:
        out.add(ruta_archivo_verify, "json_verify")
        out.add(ruta_archivo_data, "json_data")

    # Configuración de la respuesta HTTP para la descarga del archivo
    response = HttpResponse(open(ruta_archivo, 'rb'), content_type='application/gzip')
    response['Content-Disposition'] = f'attachment; filename={filename}'
    return response
