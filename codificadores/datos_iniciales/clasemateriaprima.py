def init_data(apps, schema_editor):
    """
    Args:
        apps:
        schema_editor:
    """
    ClaseMateriaPrima = apps.get_model("codificadores", "ClaseMateriaPrima")

    clases_materiaPrima = [
        ClaseMateriaPrima(id=1, descripcion='Capote', capote_fortaleza='C'),
        ClaseMateriaPrima(id=2, descripcion='F1', capote_fortaleza='F'),
        ClaseMateriaPrima(id=3, descripcion='F2', capote_fortaleza='F'),
        ClaseMateriaPrima(id=4, descripcion='F3', capote_fortaleza='F'),
        ClaseMateriaPrima(id=5, descripcion='Capa Clasificada', capote_fortaleza='P'),
        ClaseMateriaPrima(id=6, descripcion='Capa sin Clasificar', capote_fortaleza='P'),
        ClaseMateriaPrima(id=7, descripcion='F4', capote_fortaleza='F'),
    ]

    db_alias = schema_editor.connection.alias
    ClaseMateriaPrima.objects.using(db_alias).bulk_create(clases_materiaPrima)