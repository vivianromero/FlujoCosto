def init_data(apps, schema_editor):
    """
    Args:
        apps:
        schema_editor:
    """
    MotivoAjuste = apps.get_model("codificadores", "MotivoAjuste")

    motivos_ajuste = [
        MotivoAjuste(id=1, descripcion='Merma', aumento=False),
        MotivoAjuste(id=2, descripcion='Rotura', aumento=False),
        MotivoAjuste(id=3, descripcion='Promoción', aumento=False),
        MotivoAjuste(id=4, descripcion='SubProductos', aumento=False),
    ]

    db_alias = schema_editor.connection.alias
    MotivoAjuste.objects.using(db_alias).bulk_create(motivos_ajuste)