# Generated by Django 5.0 on 2024-03-26 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configuracion', '0002_alter_conexionbasedato_sistema_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conexionbasedato',
            name='sistema',
            field=models.CharField(choices=[('VersatSarasola', 'VersatSarasola'), ('SisGestMP', 'SisGestMP')], default='VersatSarasola', verbose_name='System'),
        ),
    ]