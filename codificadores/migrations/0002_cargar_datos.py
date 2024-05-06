# Generated by Django 5.0 on 2024-05-03 17:06

from django.db import migrations
from codificadores.fixtures import F001_datos_iniciales_codificadores


def load_data(apps, schema_editor):
    F001_datos_iniciales_codificadores.init_data(apps, schema_editor)


class Migration(migrations.Migration):
    dependencies = [
        ('codificadores', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_data)
    ]
