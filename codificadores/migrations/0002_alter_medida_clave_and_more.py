# Generated by Django 5.0 on 2024-02-29 15:26

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codificadores', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medida',
            name='clave',
            field=models.CharField(max_length=6, unique=True, verbose_name='Key'),
        ),
        migrations.AlterField(
            model_name='medidaconversion',
            name='factor_conversion',
            field=models.DecimalField(db_comment='Factor de conversión', decimal_places=6, max_digits=10, validators=[django.core.validators.MinValueValidator(1e-06, message='The value must be greater than 0')], verbose_name='Convertion Factor'),
        ),
    ]