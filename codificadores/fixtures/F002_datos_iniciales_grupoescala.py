from codificadores.models import *
from codificadores import ChoiceTiposProd, ChoiceEstadosProd, ChoiceClasesMatPrima, ChoiceCategoriasVit, ChoiceMotivosAjuste, ChoiceTiposDoc, ChoiceTipoNumeroDoc, ChoiceConfCentrosElementosOtros
from django.http.response import HttpResponse
from utiles.utils import json_response

modulo = "codificadores"


def init_data(apps, schema_editor):
    act_model_grupo_escala = apps.get_model(modulo, "GrupoEscalaCargo")

    grupo_escala = [
        GrupoEscalaCargo(pk=1, grupo="I", salario=2100.00),
        GrupoEscalaCargo(pk=2, grupo="II", salario=2200.00),
        GrupoEscalaCargo(pk=3, grupo="III", salario=2300.00),
        GrupoEscalaCargo(pk=4, grupo="IV", salario=2420.00),
        GrupoEscalaCargo(pk=5, grupo="V", salario=2540.00),
        GrupoEscalaCargo(pk=6, grupo="VI", salario=2660.00),
        GrupoEscalaCargo(pk=7, grupo="VII", salario=2810.00),
        GrupoEscalaCargo(pk=8, grupo="VIII", salario=2960.00),
        GrupoEscalaCargo(pk=9, grupo="IX", salario=3110.00),
        GrupoEscalaCargo(pk=10, grupo="X", salario=3260.00),
        GrupoEscalaCargo(pk=11, grupo="XI", salario=3410.00),
        GrupoEscalaCargo(pk=12, grupo="XII", salario=3610.00),
        GrupoEscalaCargo(pk=13, grupo="XIII", salario=3810.00),
        GrupoEscalaCargo(pk=14, grupo="XIV", salario=4010.00),
        GrupoEscalaCargo(pk=15, grupo="XV", salario=4210.00),
        GrupoEscalaCargo(pk=16, grupo="XVI", salario=4410.00),
        GrupoEscalaCargo(pk=17, grupo="XVII", salario=4610.00),
        GrupoEscalaCargo(pk=18, grupo="XVIII", salario=4810.00),
        GrupoEscalaCargo(pk=19, grupo="XIX", salario=5060.00),
        GrupoEscalaCargo(pk=20, grupo="XX", salario=5310.00),
        GrupoEscalaCargo(pk=21, grupo="XXI", salario=5560.00),
        GrupoEscalaCargo(pk=22, grupo="XXII", salario=5810.00),
        GrupoEscalaCargo(pk=23, grupo="XXIII", salario=6060.00),
        GrupoEscalaCargo(pk=24, grupo="XXIV", salario=6310.00),
        GrupoEscalaCargo(pk=25, grupo="XXV", salario=6610.00),
        GrupoEscalaCargo(pk=26, grupo="XXVI", salario=6960.00),
        GrupoEscalaCargo(pk=27, grupo="XXVII", salario=7310.00),
        GrupoEscalaCargo(pk=28, grupo="XXVIII", salario=7660.00),
        GrupoEscalaCargo(pk=29, grupo="XXIX", salario=8010.00),
        GrupoEscalaCargo(pk=30, grupo="XXX", salario=8510.00),
        GrupoEscalaCargo(pk=31, grupo="XXXI", salario=9010.00),
        GrupoEscalaCargo(pk=32, grupo="XXXII", salario=9510.00),
    ]
    act_model_grupo_escala.objects.bulk_create(grupo_escala)
