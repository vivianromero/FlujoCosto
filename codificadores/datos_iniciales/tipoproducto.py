def init_data(apps, schema_editor):
    """
    Args:
        apps:
        schema_editor:
    """
    TipoProducto = apps.get_model("codificadores", "TipoProducto")

    tipos_producto = [
        TipoProducto(id=1, descripcion='Pesada'),
        TipoProducto(id=2, descripcion='Materia Prima'),
        TipoProducto(id=3, descripcion='Habilitación'),
        TipoProducto(id=4, descripcion='Línea de Salida'),
        TipoProducto(id=5, descripcion='Vitola'),
        TipoProducto(id=6, descripcion='Subproducto'),
        TipoProducto(id=7, descripcion='Línea sin Terminar'),
    ]

    db_alias = schema_editor.connection.alias
    TipoProducto.objects.using(db_alias).bulk_create(tipos_producto)