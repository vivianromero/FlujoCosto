# Generated by Django 5.0 on 2024-04-26 14:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codificadores', '0011_alter_numeraciondocumentos_tiponumeracion'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConfCentrosElementosOtros',
            fields=[
                ('id', models.AutoField(choices=[(1, 'Centros de Costo'), (2, 'Elementos de Gastos')], editable=False, primary_key=True, serialize=False)),
                ('clave', models.CharField(max_length=80, unique=True, verbose_name='Configurar Centros y Elementos')),
            ],
            options={
                'db_table': 'cla_confcentroselementosotros',
                'ordering': ['clave'],
            },
        ),
        migrations.AlterField(
            model_name='numeraciondocumentos',
            name='departamento',
            field=models.BooleanField(db_comment='Si el número es por departamento', default=False, verbose_name='Por Departmento'),
        ),
        migrations.AlterField(
            model_name='numeraciondocumentos',
            name='prefijo',
            field=models.BooleanField(db_comment='Si el número de documento va a contener un prefijo', default=False, verbose_name='Usar Prefijo'),
        ),
        migrations.AlterField(
            model_name='numeraciondocumentos',
            name='sistema',
            field=models.BooleanField(db_comment='Si es controlado por el sistema', default=False, verbose_name='Controlada por el sistema'),
        ),
        migrations.AlterField(
            model_name='numeraciondocumentos',
            name='tipo_documento',
            field=models.BooleanField(db_comment='Si el número es por tipo de documento', default=False, verbose_name='Por tipo de Documento'),
        ),
        migrations.AlterField(
            model_name='numeraciondocumentos',
            name='tiponumeracion',
            field=models.IntegerField(choices=[(1, 'Número Consecutivo'), (2, 'Número de Control')], unique=True, verbose_name='Tipo de Enumeración'),
        ),
        migrations.CreateModel(
            name='ConfCentrosElementosOtrosDetalle',
            fields=[
                ('id', models.IntegerField(editable=False, primary_key=True, serialize=False)),
                ('descripcion', models.CharField(max_length=250)),
                ('valor', models.CharField(blank=True, max_length=100, null=True)),
                ('clave', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='confccelem_clave', to='codificadores.confcentroselementosotros', verbose_name='Configurar')),
            ],
            options={
                'db_table': 'cla_confcentroselementosotrosdetalle',
                'ordering': ['clave', 'descripcion'],
                'indexes': [models.Index(fields=['clave', 'descripcion'], name='cla_confcen_clave_i_8d78b0_idx')],
                'unique_together': {('clave', 'descripcion')},
            },
        ),
    ]
