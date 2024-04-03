# Generated by Django 5.0 on 2024-03-18 15:47

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('codificadores', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserUeb',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('ueb', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='codificadores.unidadcontable', verbose_name='UEB')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
                'db_table': 'cfg_userueb',
                'ordering': ('ueb', 'username', 'pk'),
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='ConexionBaseDato',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('database_name', models.CharField(max_length=250, verbose_name='Database Name')),
                ('database_user', models.CharField(max_length=250, verbose_name='User Name')),
                ('password', models.CharField(max_length=250, verbose_name='Password')),
                ('host', models.CharField(max_length=250, verbose_name='Host')),
                ('port', models.CharField(max_length=100, verbose_name='Port')),
                ('sistema', models.CharField(default='VersatSarasola', max_length=50, verbose_name='System')),
                ('unidadcontable', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='codificadores.unidadcontable', verbose_name='UEB')),
            ],
            options={
                'verbose_name': 'Database conexion',
                'verbose_name_plural': 'Conexions of data bases',
                'db_table': 'cfg_conexionasedato',
                'ordering': ['unidadcontable__codigo', 'sistema'],
            },
        ),
        migrations.CreateModel(
            name='ConsecutivoDocumento',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('numero', models.IntegerField(verbose_name='Number')),
                ('numeraciondocumento', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='consecutivodocumento_numeracion', to='codificadores.numeraciondocumentos', verbose_name='Enumeration Type')),
                ('ueb', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='consecutivo_ueb', to='codificadores.unidadcontable', verbose_name='UEB')),
            ],
            options={
                'db_table': 'cfg_consecutivodocumento',
            },
        ),
        migrations.CreateModel(
            name='ConsecutivoDocumentoDepartamento',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('consecutivodocumento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='consecutivodocumentodpto_consecutivodocumento', to='configuracion.consecutivodocumento')),
                ('departamento', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='consecutivodocumentodpto_departamento', to='codificadores.departamento', verbose_name='Department')),
            ],
            options={
                'db_table': 'cfg_consecutivodocumentodepartamento',
            },
        ),
        migrations.CreateModel(
            name='ConsecutivoDocumentoTipoDocumento',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('consecutivodocumento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='consecutivodocumentotipodoc_consecutivodocumento', to='configuracion.consecutivodocumento')),
                ('tipodocumento', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='consecutivodocumentotipodoc_tipodocumento', to='codificadores.tipodocumento')),
            ],
            options={
                'db_table': 'cfg_consecutivodocumentotipodocumento',
            },
        ),
        migrations.CreateModel(
            name='LoggedInUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_key', models.CharField(blank=True, max_length=32, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='logged_in_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddIndex(
            model_name='userueb',
            index=models.Index(fields=['username', 'email', 'ueb', 'last_login'], name='cfg_userueb_usernam_82f8ee_idx'),
        ),
        migrations.AddIndex(
            model_name='conexionbasedato',
            index=models.Index(fields=['unidadcontable', 'sistema'], name='cfg_conexio_unidadc_0ea369_idx'),
        ),
    ]
