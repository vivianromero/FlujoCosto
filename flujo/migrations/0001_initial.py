# Generated by Django 5.0 on 2024-03-18 15:47

import django.db.models.deletion
import django.db.models.functions.datetime
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('codificadores', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Documento',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('fecha', models.DateField(verbose_name='Date')),
                ('fecha_creacion', models.DateTimeField(db_default=django.db.models.functions.datetime.Now(), verbose_name='Create at')),
                ('numerocontrol', models.CharField(max_length=50, verbose_name='Control Number')),
                ('numeroconsecutivo', models.IntegerField(verbose_name='Consecutive Number')),
                ('suma_importe', models.DecimalField(decimal_places=2, default=0.0, max_digits=18, verbose_name='Amount')),
                ('observaciones', models.TextField(blank=True, null=True, verbose_name='Observations')),
                ('estado', models.IntegerField(choices=[(1, 'Edición'), (2, 'Confirmado'), (3, 'Rechazado')], db_comment='Estado del documento 1:Edición, 2:Confirmado, 3:Rechazado', verbose_name='Status')),
                ('reproceso', models.BooleanField(default=False, verbose_name='Reprocessing')),
                ('editar_nc', models.BooleanField(default=False)),
                ('comprob', models.CharField(blank=True, max_length=150, null=True)),
                ('departamento', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='documento_departamento', to='codificadores.departamento')),
                ('tipodocumento', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='documento_tipodocumento', to='codificadores.tipodocumento')),
                ('ueb', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='documento_tipodocumento', to='codificadores.unidadcontable')),
            ],
            options={
                'db_table': 'fp_documento',
                'ordering': ['ueb', 'departamento', 'tipodocumento', '-numeroconsecutivo'],
            },
        ),
        migrations.CreateModel(
            name='DocumentoAjuste',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('documento', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='documentoajuste_documento', to='flujo.documento')),
                ('motivoajuste', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='documentoajuste_motivo', to='codificadores.motivoajuste', verbose_name='Adjustment Reason')),
            ],
            options={
                'db_table': 'fp_documentoajuste',
            },
        ),
        migrations.CreateModel(
            name='DocumentoDetalle',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('cantidad', models.DecimalField(decimal_places=4, default=0.0, max_digits=18, verbose_name='Quantity')),
                ('precio', models.DecimalField(decimal_places=7, default=0.0, max_digits=18, verbose_name='Price')),
                ('importe', models.DecimalField(decimal_places=2, default=0.0, max_digits=18, verbose_name='Amount')),
                ('existencia', models.DecimalField(decimal_places=4, default=0.0, max_digits=18, verbose_name='Existence')),
                ('documento', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='documentodetalle_documento', to='flujo.documento')),
                ('estado', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='documentodetalle_productoestado', to='codificadores.estadoproducto', verbose_name='Status')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='documentodetalle_producto', to='codificadores.productoflujo', verbose_name='Product')),
            ],
            options={
                'db_table': 'fp_documentodetalle',
            },
        ),
        migrations.CreateModel(
            name='DocumentoDetalleEstado',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('existencia', models.DecimalField(decimal_places=6, default=0.0, max_digits=18, verbose_name='Existence')),
                ('documentodetalle', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='documentodetalleestado_detalle', to='flujo.documentodetalle')),
                ('estado', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='documentodetalleestado_estado', to='codificadores.estadoproducto', verbose_name='Status')),
            ],
            options={
                'db_table': 'fp_documentodetalleestado',
            },
        ),
        migrations.CreateModel(
            name='DocumentoDetalleProducto',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('existencia', models.DecimalField(decimal_places=6, default=0.0, max_digits=18, verbose_name='Existence')),
                ('documentodetalle', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='documentodetalleproducto_detalle', to='flujo.documentodetalle')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='documentodetalleproducto_producto', to='codificadores.productoflujo', verbose_name='Product')),
            ],
            options={
                'db_table': 'fp_documentodetalleproducto',
            },
        ),
        migrations.CreateModel(
            name='DocumentoDetalleTransfDptoControlTecnico',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('cantidad', models.DecimalField(decimal_places=4, default=0.0, max_digits=18, verbose_name='Quantity')),
                ('precio', models.DecimalField(decimal_places=7, default=0.0, max_digits=18, verbose_name='Price')),
                ('importe', models.DecimalField(decimal_places=2, default=0.0, max_digits=18, verbose_name='Amount')),
                ('existencia', models.DecimalField(decimal_places=4, default=0.0, max_digits=18, verbose_name='Existence')),
                ('buenos', models.IntegerField(default=0, verbose_name='Good')),
                ('defectuoso_cc', models.IntegerField(default=0, verbose_name='Defective CC')),
                ('defectuoso_cien', models.IntegerField(default=0, verbose_name='Defective 100%')),
                ('sensorial', models.IntegerField(default=0, verbose_name='Sensory Test')),
                ('rotos', models.IntegerField(default=0, verbose_name='Broken')),
                ('documento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documentodetalletransfdptocontroltecnico_documento', to='flujo.documento')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='documentodetalletransfdptocontroltecnico_producto', to='codificadores.productoflujo', verbose_name='Product')),
            ],
            options={
                'db_table': 'fp_documentodetalletransfdptocontroltecnico',
            },
        ),
        migrations.CreateModel(
            name='DocumentoDetalleVenta',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('importe', models.DecimalField(decimal_places=2, default=0.0, max_digits=18, verbose_name='Amount')),
                ('documentodetalle', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='documentodetalleventa_detalle', to='flujo.documentodetalle')),
            ],
            options={
                'db_table': 'fp_documentodetalleventa',
            },
        ),
        migrations.CreateModel(
            name='DocumentoDevolucion',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('documento', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='documentodevolucion_documento', to='flujo.documento')),
            ],
            options={
                'db_table': 'fp_documentodevolucion',
            },
        ),
        migrations.CreateModel(
            name='DocumentoDevolucionRecibida',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('documento', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='documentodevolucionrecibida_documento', to='flujo.documento')),
                ('documentoorigen', models.ForeignKey(db_comment='Documento que originó la devolucion hacia el departamento', on_delete=django.db.models.deletion.PROTECT, related_name='documentodevolucionrecibida_documentoorigen', to='flujo.documento')),
            ],
            options={
                'db_table': 'fp_documentodevolucionrecibida',
            },
        ),
        migrations.CreateModel(
            name='DocumentoOrigenVersat',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('documentoversat', models.IntegerField()),
                ('origen_versat', models.CharField(max_length=40)),
                ('documento', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='documentoorigenversat_documento', to='flujo.documento')),
            ],
            options={
                'db_table': 'fp_documentoorigenversat',
            },
        ),
        migrations.CreateModel(
            name='DocumentoTransfDepartamento',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('departamento', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='documentotransfdepartamento_departamento', to='codificadores.departamento', verbose_name='Department')),
                ('documento', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='documentotransfdepartamento_documento', to='flujo.documento')),
            ],
            options={
                'db_table': 'fp_documentotransfdepartamento',
            },
        ),
        migrations.CreateModel(
            name='DocumentoTransfDepartamentoRecibida',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('documento', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='documentotransfdepartamentorecibida_documento', to='flujo.documento')),
                ('documentoorigen', models.ForeignKey(db_comment='Documento que originó la transferencia hacia el departamento', on_delete=django.db.models.deletion.PROTECT, related_name='documentotransfdepartamentorecibida_documentoorigen', to='flujo.documento')),
            ],
            options={
                'db_table': 'fp_documentotransfdesdedepartamento',
            },
        ),
        migrations.CreateModel(
            name='DocumentoTransfExterna',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('documento', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='documentotransfext_documento', to='flujo.documento')),
                ('unidadcontable', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='documentotransfext_unidadcontable', to='codificadores.unidadcontable')),
            ],
            options={
                'db_table': 'fp_documentotransfexterna',
            },
        ),
        migrations.CreateModel(
            name='DocumentoTransfExternaDptoDestino',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('documentotransfext', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documentotransfextdptodest_documento', to='flujo.documento')),
                ('dptodestino', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='documentotransfextdptodest_dptodest', to='codificadores.departamento')),
            ],
            options={
                'db_table': 'fp_documentotransfexternadptodestino',
            },
        ),
        migrations.CreateModel(
            name='DocumentoTransfExternaRecibida',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('documento', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='documentotransfextrecibida_documento', to='flujo.documento')),
                ('unidadcontable', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='documentotransfextrecibida_unidadcontable', to='codificadores.unidadcontable')),
            ],
            options={
                'db_table': 'fp_documentotransfexternarecibida',
            },
        ),
        migrations.CreateModel(
            name='DocumentoTransfExternaRecibidaDocOrigen',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('documentoorigen', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='documentotransfextrecibida_documentoorigen', to='flujo.documento')),
            ],
            options={
                'db_table': 'fp_documentotransfexternarecibidadocorigen',
            },
        ),
        migrations.CreateModel(
            name='DocumentoVersatRechazado',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('documentoversat', models.IntegerField()),
                ('fecha_doc_versat', models.DateField()),
                ('fecha_rechazo', models.DateTimeField(db_default=django.db.models.functions.datetime.Now())),
                ('ueb', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='documentoversatrechazado_ueb', to='codificadores.unidadcontable')),
            ],
            options={
                'db_table': 'fp_documentoversatrechazado',
            },
        ),
        migrations.CreateModel(
            name='ExistenciaDpto',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('existencia', models.DecimalField(decimal_places=4, default=0.0, max_digits=18, verbose_name='Existence')),
                ('importe', models.DecimalField(decimal_places=2, default=0.0, max_digits=18, verbose_name='Amount')),
                ('departamento', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='existenciadpto_departamento', to='codificadores.departamento')),
                ('estado', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='existenciadpto_productoestado', to='codificadores.estadoproducto')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='existenciadpto_producto', to='codificadores.productoflujo')),
                ('ueb', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='existenciadpto_ueb', to='codificadores.unidadcontable')),
            ],
            options={
                'db_table': 'fp_existenciadpto',
            },
        ),
        migrations.CreateModel(
            name='FechaCierreMes',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('fecha', models.DateField(verbose_name='Date')),
                ('ueb', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='fechacierremes_ueb', to='codificadores.unidadcontable', verbose_name='UEB')),
            ],
            options={
                'db_table': 'fp_fechacierremes',
                'unique_together': {('fecha', 'ueb')},
            },
        ),
        migrations.CreateModel(
            name='FechaPeriodo',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('fecha', models.DateField(verbose_name='Date')),
                ('departamento', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='fechaperiodo_departamento', to='codificadores.departamento', verbose_name='Department')),
                ('ueb', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='fechaperiodo_ueb', to='codificadores.unidadcontable', verbose_name='UEB')),
            ],
            options={
                'db_table': 'fp_fechaperiodo',
                'unique_together': {('fecha', 'departamento', 'ueb')},
            },
        ),
    ]
