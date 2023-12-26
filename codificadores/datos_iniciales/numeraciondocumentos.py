def init_data(apps, schema_editor):
    """
    Args:
        apps:
        schema_editor:
    """
    NumeracionDocumentos = apps.get_model("codificadores", "NumeracionDocumentos")

    numeraciondocumentos = [
        NumeracionDocumentos(id=1, tiponumeracion='Número Consecutivo', sistema=True, departamento=True, tipo_documento=True),
        NumeracionDocumentos(id=2, tiponumeracion='Número de Control', sistema=False, departamento=True, tipo_documento=True),
    ]

    db_alias = schema_editor.connection.alias
    NumeracionDocumentos.objects.using(db_alias).bulk_create(numeraciondocumentos)