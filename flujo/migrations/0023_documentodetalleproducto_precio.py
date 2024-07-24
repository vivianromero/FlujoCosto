# Generated by Django 5.0.7 on 2024-07-24 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flujo', '0022_alter_documentotransfexternarecibida_documento'),
    ]

    operations = [
        migrations.AddField(
            model_name='documentodetalleproducto',
            name='precio',
            field=models.DecimalField(decimal_places=7, default=0.0, max_digits=18, verbose_name='Price'),
        ),
    ]
