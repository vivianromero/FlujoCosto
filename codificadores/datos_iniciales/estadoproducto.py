def init_data(apps, schema_editor):
    """
    Args:
        apps:
        schema_editor:
    """
    EstadoProducto = apps.get_model("codificadores", "EstadoProducto")

    estados_producto = [
        EstadoProducto(id=1, descripcion='Bueno'),
        EstadoProducto(id=2, descripcion='Deficiente'),
        EstadoProducto(id=3, descripcion='Rechazo'),
    ]

    db_alias = schema_editor.connection.alias
    EstadoProducto.objects.using(db_alias).bulk_create(estados_producto)