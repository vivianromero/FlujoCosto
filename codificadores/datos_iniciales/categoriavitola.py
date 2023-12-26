def init_data(apps, schema_editor):
    """
    Args:
        apps:
        schema_editor:
    """
    CategoriaVitola = apps.get_model("codificadores", "CategoriaVitola")

    categorias_vitola = [
        CategoriaVitola(id=5, descripcion='IX', orden=5),
        CategoriaVitola(id=6, descripcion='ND', orden=6),
        CategoriaVitola(id=7, descripcion='V', orden=1),
        CategoriaVitola(id=8, descripcion='VI', orden=2),
        CategoriaVitola(id=9, descripcion='VII', orden=3),
        CategoriaVitola(id=10, descripcion='VIII', orden=4),
    ]

    db_alias = schema_editor.connection.alias
    CategoriaVitola.objects.using(db_alias).bulk_create(categorias_vitola)