# Generated by Django 5.0 on 2024-03-25 15:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codificadores', '0002_marcasalida_activa_medida_activa'),
        ('configuracion', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conexionbasedato',
            name='sistema',
            field=models.CharField(choices=[(1, 'VersatSarasola'), (2, 'SisGestMP')], default='VersatSarasola', editable=False, verbose_name='System'),
        ),
        migrations.AlterField(
            model_name='conexionbasedato',
            name='unidadcontable',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='codificadores.unidadcontable', verbose_name='UEB'),
        ),
        migrations.AlterUniqueTogether(
            name='conexionbasedato',
            unique_together={('unidadcontable', 'sistema')},
        ),
    ]
