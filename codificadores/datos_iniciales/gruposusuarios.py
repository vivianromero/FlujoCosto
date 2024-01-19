def init_data(apps, schema_editor):
    """
    Args:
        apps:
        schema_editor:
    """
    Grupos = apps.get_model("auth", "Group")

    grupos = [
        CategoriaVitola(id=1, name='Administración'),
        CategoriaVitola(id=2, name='Operador Flujo'),
        CategoriaVitola(id=3, name='Operador Costo'),
        CategoriaVitola(id=4, name='Consultor'),
    ]

    db_alias = schema_editor.connection.alias
    Grupos.objects.using(db_alias).bulk_create(grupos)