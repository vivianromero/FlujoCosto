from codificadores.models import FichaCostoFilas

modulo = "codificadores"


def init_data(apps, schema_editor):
    act_model_filas_fichacosto = apps.get_model(modulo, "FichaCostoFilas")

    filas_fichacosto = [
        FichaCostoFilas(pk=1, fila=1.0, descripcion='Gasto Material', encabezado=True),
        FichaCostoFilas(pk=2, fila=1.1, descripcion='Materia Prima y Materiales', desglosado=True),
        FichaCostoFilas(pk=3, fila=1.2, descripcion='Gastos Materia Prima Tabaco', desglosado=True),
    ]
    act_model_filas_fichacosto.objects.bulk_create(filas_fichacosto)
