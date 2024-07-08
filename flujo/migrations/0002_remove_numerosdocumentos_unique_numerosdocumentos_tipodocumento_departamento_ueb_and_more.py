# Generated by Django 5.0 on 2024-06-29 12:09

import codificadores.models
import django.db.models.deletion
import django_choices_field.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codificadores', '0002_cargar_datos'),
        ('flujo', '0001_initial'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='numerosdocumentos',
            name='unique_numerosdocumentos_tipodocumento_departamento_ueb',
        ),
        migrations.RemoveIndex(
            model_name='numerosdocumentos',
            name='fp_numerosd_tipodoc_ba11b9_idx',
        ),
        migrations.RemoveIndex(
            model_name='numerosdocumentos',
            name='fp_numerosd_tipodoc_abea0b_idx',
        ),
        migrations.RenameField(
            model_name='numerosdocumentos',
            old_name='consecutivo',
            new_name='numero',
        ),
        migrations.RemoveField(
            model_name='numerosdocumentos',
            name='control',
        ),
        migrations.RemoveField(
            model_name='numerosdocumentos',
            name='tipodocumento',
        ),
        migrations.AddField(
            model_name='numerosdocumentos',
            name='tiponumero',
            field=django_choices_field.fields.IntegerChoicesField(choices=[(1, 'Número Consecutivo'), (2, 'Número de Control')], choices_enum=codificadores.models.TipoNumeroDoc, default=1, verbose_name='Tipo número'),
        ),
        migrations.AlterField(
            model_name='numerosdocumentos',
            name='departamento',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='numerodoc_departamento', to='codificadores.departamento', verbose_name='Department'),
        ),
    ]
