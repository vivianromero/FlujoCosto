# Generated by Django 5.0 on 2024-04-19 10:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('codificadores', '0005_alter_tipoproducto_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lineasalida',
            options={'ordering': ['producto__descripcion']},
        ),
    ]
