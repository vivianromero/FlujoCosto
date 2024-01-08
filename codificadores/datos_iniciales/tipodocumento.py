def init_data(apps, schema_editor):
    """
    Args:
        apps:
        schema_editor:
    """
    TipoDocumento = apps.get_model("codificadores", "TipoDocumento")

    tipos_documento = [
        TipoDocumento(id=1, descripcion='Entrada Desde Versat', operacion='E'),
        TipoDocumento(id=2, descripcion='Salida Hacia Versat', operacion='S'),
        TipoDocumento(id=3, descripcion='Transferencia Hacia Departamento', operacion='S'),
        TipoDocumento(id=4, descripcion='Transferencia Desde Departamento', operacion='E'),
        TipoDocumento(id=5, descripcion='Ajuste de Aumento', operacion='E'),
        TipoDocumento(id=6, descripcion='Ajuste de Disminución', operacion='S'),
        TipoDocumento(id=7, descripcion='Recepción de Producción de Reproceso', operacion='E'),
        TipoDocumento(id=8, descripcion='Recepción de Producción', operacion='E'),
        TipoDocumento(id=9, descripcion='Devolución', operacion='S'),
        TipoDocumento(id=10, descripcion='Sobrante Sujeto a Investigación', operacion='E'),
        TipoDocumento(id=12, descripcion='Carga Inicial', operacion='E'),
        TipoDocumento(id=13, descripcion='Devolución Recibida', operacion='E'),
        TipoDocumento(id=14, descripcion='Cambio de Estado', operacion='S'),
        TipoDocumento(id=15, descripcion='Transferencia Externa', operacion='S'),
        TipoDocumento(id=16, descripcion='Recibir Transferencia Externa', operacion='E'),
        TipoDocumento(id=17, descripcion='Venta a Trabajadores', operacion='S'),
        TipoDocumento(id=18, descripcion='Reporte de SubProductos', operacion='E'),
        TipoDocumento(id=19, descripcion='Cambio de Producto', operacion='S'),

    ]

    db_alias = schema_editor.connection.alias
    TipoDocumento.objects.using(db_alias).bulk_create(tipos_documento)