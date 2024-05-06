# views.py
import json
import os
import sys
import tarfile

from django.conf import settings
from django.core import serializers
from django.core.management import call_command
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _

from codificadores.models import UnidadContable, Medida, MedidaConversion, MarcaSalida, CentroCosto, Cuenta, \
    Departamento, CambioProducto, NumeracionDocumentos, MotivoAjuste, ConfCentrosElementosOtros, ConfCentrosElementosOtrosDetalle
from cruds_adminlte3.utils import crud_url_name
from utiles.decorators import adminempresa_required
from utiles.utils import message_success
from utiles.utils import obtener_version, codificar

from django.contrib.auth.models import Group, Permission


@adminempresa_required
def uc_exportar(request):
    # DICC_GROUP_PERMISSION = {
    #     (1, 2, 3, 4, 5):
    #         {"unidadcontable": ['view'],
    #          "cambioproducto": ['view'],
    #          "centrocosto": ['view'],
    #          "confcentroselementosotros": ['view'],
    #          "confcentroselementosotrosdetalle": ['view'],
    #          "confcentroselementosotrosdetallegrouped": ['view'],
    #          "cuenta": ['view'],
    #          "departamento": ['view'],
    #          "lineasalida": ['view'],
    #          "marcasalida": ['view'],
    #          "medida": ['view'],
    #          "medidaconversion": ['view'],
    #          "motivoajuste": ['view'],
    #          "normaconsumo": ['view'],
    #          "normaconsumodetalle": ['view'],
    #          "normaconsumogrouped": ['view'],
    #          "numeraciondocumentos": ['view'],
    #          "productoflujo": ['view'],
    #          "productoflujovitola": ['view'],
    #          "productscapasclapesadas": ['view'],
    #          "unidadcontable": ['view'],
    #          "vitola": ['view'],
    #          "userueb": ['view', 'change', 'add', 'delete'],
    #          "conexionbasedato": ['view', 'change', 'add', 'delete']
    #          },
    #     (5,):
    #         {"unidadcontable": ['change'],
    #          "cambioproducto": ['change', 'add', 'delete'],
    #          "centrocosto": ['change'],
    #          "confcentroselementosotros": ['change'],
    #          "confcentroselementosotrosdetalle": ['change'],
    #          "confcentroselementosotrosdetallegrouped": ['change'],
    #          "departamento": ['change', 'add', 'delete'],
    #          "lineasalida": ['change', 'add', 'delete'],
    #          "marcasalida": ['change', 'add', 'delete'],
    #          "medida": ['change'],
    #          "medidaconversion": ['change', 'add', 'delete'],
    #          "motivoajuste": ['change', 'add', 'delete'],
    #          "normaconsumo": ['change', 'add', 'delete'],
    #          "normaconsumodetalle": ['change', 'add', 'delete'],
    #          "normaconsumogrouped": ['change', 'add', 'delete'],
    #          "numeraciondocumentos": ['change'],
    #          "productoflujo": ['change', 'add', 'delete'],
    #          "productoflujovitola": ['change', 'add', 'delete'],
    #          "productscapasclapesadas": ['change', 'add', 'delete'],
    #          "unidadcontable": ['change'],
    #          "vitola": ['change', 'add', 'delete']
    #          }
    # }
    #
    # # def init_data(apps, schema_editor):
    # #     # act_model_group = apps.get_model('auth', "Group")
    # #     # act_model_permission = apps.get_model('auth', "Permission")
    #
    # groups = [
    #     Group(pk=1, name='Administrador'),
    #     Group(pk=2, name='Operador Flujo'),
    #     Group(pk=3, name='Operador Costo'),
    #     Group(pk=4, name='Consultor'),
    #     Group(pk=5, name='Administrador Empresa'),
    # ]
    # # Group.objects.bulk_create(groups)
    #
    # keys_dicc = DICC_GROUP_PERMISSION.keys()
    # for k in keys_dicc:
    #     models = DICC_GROUP_PERMISSION[k].keys()
    #     list_keys_groups = list(k)
    #     list_permissions = []
    #     list_permiss = []
    #     for m in models:
    #         permiss = DICC_GROUP_PERMISSION[k][m]
    #         for p in permiss:
    #             list_permiss.append(p + '_' + m)
    #     query_permiss = Permission.objects.filter(codename__in=list_permiss)
    #     for permission in query_permiss:
    #         for g in list_keys_groups:
    #             group = Group.objects.get(pk=g)
    #             permission
    #             group.permissions.add(permission)
    return crear_export_datos(request, 'UC', UnidadContable)


@adminempresa_required
def um_exportar(request):
    return crear_export_datos(request, 'UM', Medida)


@adminempresa_required
def umc_exportar(request):
    return crear_export_datos(request, 'UMC', MedidaConversion)


@adminempresa_required
def ms_exportar(request):
    return crear_export_datos(request, 'MS', MarcaSalida)

@adminempresa_required
def ma_exportar(request):
    return crear_export_datos(request, 'MotAjus', MotivoAjuste)


@adminempresa_required
def cc_exportar(request):
    return crear_export_datos(request, 'CC', CentroCosto)


@adminempresa_required
def ccta_exportar(request):
    return crear_export_datos(request, 'CCTA', Cuenta)


@adminempresa_required
def dpto_exportar(request):
    return crear_export_datos(request, 'DPTO', Departamento)


@adminempresa_required
def cprod_exportar(request):
    return crear_export_datos(request, 'CambioPROD', CambioProducto)


@adminempresa_required
def numdoc_exportar(request):
    return crear_export_datos(request, 'NumDoc', NumeracionDocumentos)

@adminempresa_required
def all_conf_exportar(request):
    ruta_archivo = os.path.join('codificadores', 'fixtures', 'ConfigTodas.json')
    output = open(ruta_archivo, "w+")
    call_command('dumpdata', 'codificadores', indent=2, stdout=output)
    output.close()
    json_file = open(ruta_archivo, 'r')
    datos_json = json.dumps(json.load(json_file),ensure_ascii=False)
    return crear_export_file(request, datos_json, 'ALL_CONF', None)

def json_info(opcion):
    version = obtener_version()
    check_sum = codificar(opcion + version)
    dicc_valid = {'opcion': opcion,
                  'version': version,
                  'check_sum': check_sum}
    return dicc_valid

def crear_export_datos(request, opcion, modelo):
    json_data = serializers.serialize("json",  modelo.objects.all()).replace("true", '"True"').replace(
        "false", '"False"')
    return crear_export_file(request, json_data, opcion, modelo)

def crear_export_datos_table(request, opcion, modelo, datos, datos2=[]):
    json_data = serializers.serialize("json", datos).replace("true", '"True"').replace("false", '"False"')
    if datos2:
        json_data2 = serializers.serialize("json", datos2).replace("true", '"True"').replace("false", '"False"')
        json_data = json_data.replace(']', '') + json_data2.replace('[', ', ')
    return crear_export_file(request, json_data, opcion, modelo)


def crear_export_file(request, json_data, opcion, modelo):
    dicc_verify = json_info(opcion)
    file_path = settings.STATIC_ROOT
    check_sum_data = codificar(json_data)
    dicc_verify['check_sum_data'] = check_sum_data

    if len(json_data) <= 2:
        message_success(request=request, title=_("Warning"), text=_("There aren't data to export"))
        return redirect('app_index:index') if model==None else redirect(crud_url_name(modelo, 'list', 'app_index:codificadores:'))

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