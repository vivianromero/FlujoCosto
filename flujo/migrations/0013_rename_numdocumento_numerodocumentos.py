# Generated by Django 5.0 on 2024-06-30 13:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('codificadores', '0002_cargar_datos'),
        ('flujo', '0012_delete_numerosdocumentos'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='NumDocumento',
            new_name='NumeroDocumentos',
        ),
    ]
