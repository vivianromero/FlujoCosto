# Generated by Django 5.0 on 2024-04-23 13:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('codificadores', '0008_normaconsumogrouped'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='normaconsumogrouped',
            options={'ordering': ['tipo', 'producto__descripcion', 'fecha']},
        ),
    ]
