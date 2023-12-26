def init_data(apps, schema_editor):
    """
    Args:
        apps:
        schema_editor:
    """
    TipoVitola = apps.get_model("codificadores", "TipoVitola")

    tipos_vitola = [
        TipoVitola(id=1, descripcion='Picadura'),
        TipoVitola(id=2, descripcion='Hoja'),
    ]

    db_alias = schema_editor.connection.alias
    TipoVitola.objects.using(db_alias).bulk_create(tipos_vitola)