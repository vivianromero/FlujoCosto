# from dotenv import load_dotenv
"""
Django settings for flujo_costo project.

Generated by 'django-admin startproject' using Django 5.0.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import os
from datetime import timedelta
from pathlib import Path

# import environ TODO esto se habilita cuando funcione el environ
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from easy_thumbnails.conf import Settings as Thumbnail_Settings

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve()

##### TODO esto se habilita cuando funcione el environ
# env = environ.Env()
# env = environ.Env()
#
# environ.Env.read_env(os.path.join(BASE_DIR, '.env.local'))
######

MEDIA_ROOT_UPLOAD_FILES = (os.path.join(BASE_DIR.parent, 'staticfiles/upload'))
REPORTS_DIR = (os.path.join(BASE_DIR.parent, 'Reportes/reports'))
REPORTS_OUTPUT = (os.path.join(BASE_DIR.parent, 'Reportes/output'))

APP_VERSION = (os.path.join(BASE_DIR.parent, 'config/version'))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = env('SECRET_KEY') TODO esto se habilita cuando funcione el environ
SECRET_KEY = 'django-insecure-h-yyy!9x0ci_%88!mham!0$j%jkd0j+#!8@r6ent@h513m=b^e'

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = env('DEBUG', default=True) TODO esto se habilita cuando funcione el environ
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition


DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.forms',
    'password_expire',
    'bulk_sync',
    'bulk_update_or_create',
]

THIRD_APPS = [
    'corsheaders',
    'crispy_bootstrap4',
    'crispy_forms',
    'django_ajax',
    'django_filters',
    'django_htmx',
    'django_select2',
    'django_tables2',
    'easy_thumbnails',
    'image_cropping',
    'menu_generator',
    'rest_framework',
    'rest_framework.authtoken',
    'bootstrap_datepicker_plus',
    'bootstrap_daterangepicker',
    'crispy_formset_modal',
    'mptt',
    'sweetify',
    'importar',
    'template_partials',
]

MY_APPS = [
    'codificadores.apps.CodificadoresConfig',
    'configuracion.apps.ConfiguracionConfig',
    'flujo.apps.FlujoConfig',
    'costo.apps.CostoConfig',
    'app_index',
    'app_versat.apps.AppVersatConfig',
    'app_apiversat',
    'app_auth.usuarios',
    'cruds_adminlte3',
    # 'preparacarga.apps.PreparaCargaConfig',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_APPS + MY_APPS

CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap4'
CRISPY_TEMPLATE_PACK = 'bootstrap4'


IMAGE_CROPPING_JQUERY_URL = None

INTERNAL_IPS = ('127.0.0.1',)

THUMBNAIL_PROCESSORS = (
                           'image_cropping.thumbnail_processors.crop_corners',
                       ) + Thumbnail_Settings.THUMBNAIL_PROCESSORS

TIME_FORMAT = 'h:i A'
DATETIME_FORMAT = 'd/m/Y H:i:s'
DATE_FORMAT = 'd/m/Y'
DATE_INPUT_FORMATS = [
    '%d/%m/%Y',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 'django_session_timeout.middleware.SessionTimeoutMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.admindocs.middleware.XViewMiddleware',
    'django_htmx.middleware.HtmxMiddleware',
    'django_auto_logout.middleware.auto_logout',
    'app_auth.usuarios.middleware.OneSessionPerUserMiddleware',
    'app_auth.usuarios.middleware.PasswordExpireMiddleware',
    'app_versat.middleware.DatabaseConectionMiddleware',
]

CORS_ORIGIN_ALLOW_ALL = False
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_WHITELIST = (
    'https://127.0.0.1:8000',
    'https://localhost:8000',
    'https://127.0.0.1:8080',
    'https://localhost:8080',
    'https://127.0.0.1:3000',
    'https://localhost:3000',
    'http://127.0.0.1:8000',
    'http://localhost:8000',
    'http://127.0.0.1:8080',
    'http://localhost:8080',
    'http://127.0.0.1:3000',
    'http://localhost:3000',
)

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'TEST_REQUEST_RENDERER_CLASSES': (
        'rest_framework.renderers.MultiPartRenderer',
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.TemplateHTMLRenderer',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 50,
}

JWT_AUTH = {
    'JWT_ALLOW_REFRESH': True,
    'JWT_EXPIRATION_DELTA': timedelta(hours=1),
    'JWT_REFRESH_EXPIRATION_DELTA': timedelta(days=7),
}

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.i18n',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                'django_auto_logout.context_processors.auto_logout_client',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases
def get_db_config(environ_var='DATABASE_URL'):
    """Get Database configuration."""
    options = env.db(var=environ_var, default='sqlite:///db.sqlite3')
    if options.get('ENGINE') != 'django.db.backends.sqlite3':
        return options

    # This will allow use a relative to the project root DB path
    # for SQLite like 'sqlite:///db.sqlite3'
    if not options['NAME'] == ':memory:' and not os.path.isabs(options['NAME']):
        options.update({'NAME': os.path.join(BASE_DIR.parent, options['NAME'])})

    return options


### TODO esto se habilita cuando funcione el environ
#
# DATABASES = {
#     'default': get_db_config()
# }
#####

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'flujo_costo1',
        'USER': 'flujo_costo',
        'PASSWORD': 'flujo_costo.123*-',
        'HOST': '172.17.0.3',
        'PORT': '5432',
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTH_USER_MODEL = 'configuracion.UserUeb'

LOCALE_PATHS = [
    os.path.join(BASE_DIR.parent, 'locale'),
]

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'es'

LANGUAGES = [
    ("es", _("Spanish")),
    # ("en", _("English")),
]

TIME_ZONE = 'America/Havana'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

STATICFILES_DIRS = [
    BASE_DIR.parent / 'app_index/static',
    BASE_DIR.parent / 'cruds_adminlte3/static'
]

STATIC_ROOT = os.path.join(BASE_DIR.parent, 'staticfiles')

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

TEMPUS_DOMINUS_INCLUDE_ASSETS = False

TEMPUS_DOMINUS_LOCALIZE = True

BOOTSTRAP_DATEPICKER_PLUS = {
    "options": {
        # "locale": get_language(),
        "showClose": True,
        "showClear": True,
        "showTodayButton": True,
        "allowInputToggle": True,
    },
    "variant_options": {
        "date": {
            "format": "DD/MM/YYYY",
        },
    },
    # "datetimepicker_js_url": "/static/plugins/bootstrap-datetimepicker/4_17_47/bootstrap-datetimepicker.js",
    # "datetimepicker_css_url": "/static/plugins/bootstrap-datetimepicker/4_17_47/bootstrap-datetimepicker.css",
    # "bootstrap_icon_css_url": "/static/plugins/bootstrap-icons/font/bootstrap-icons.css",
    # "app_static_url": "/static/plugins/bootstrap_datepicker_plus/",
    "momentjs_url": None,  # If you already have momentjs added into your template
}

# Session expiration
# SESSION_EXPIRE_SECONDS = float(env('SESSION_EXPIRE_SECONDS')) TODO esto se habilita cuando funcione el environ
# SESSION_EXPIRE_SECONDS = 600

LOGIN_REDIRECT_URL = reverse_lazy('app_index:index')

LOGOUT_REDIRECT_URL = reverse_lazy('app_index:usuario:login')

# SESSION_TIMEOUT_REDIRECT = reverse_lazy('app_index:usuario:login')

# SESSION_EXPIRE_AFTER_LAST_ACTIVITY = True

AUTO_LOGOUT = {
    'IDLE_TIME': timedelta(minutes=30),
    # 'SESSION_TIME': timedelta(minutes=30),
    'MESSAGE': 'La sessióh ha expirado. Por favor introduzca nuevamente sus credenciales para continuar.',
    'REDIRECT_TO_LOGIN_IMMEDIATELY': True,
}

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "django.contrib.auth.backends.AllowAllUsersModelBackend",
)

DATABASE_ROUTERS = ['app_versat.routers.ApiDynamicDbRouter']

# contact information if password is expired
PASSWORD_EXPIRE_CONTACT = ""
# expire passwords after 90 days
PASSWORD_EXPIRE_SECONDS = 90 * 24 * 60 * 60
# start warning 10 days before expiration
PASSWORD_EXPIRE_WARN_SECONDS = 10 * 24 * 60 * 60

# To redirect new users to the change password page
PASSWORD_EXPIRE_FORCE = True

# exclude superusers from the password expiration
PASSWORD_EXPIRE_EXCLUDE_SUPERUSERS = True

# Configuraciones de la API VERSAT TODO esto se habilita cuando funcione el environ
# URL_API = env('URL_API')
# CONNECTION_TOKEN_API = env('CONNECTION_TOKEN_API')
# USERNAME_API = env('USERNAME_API')
# PASSWORD_API = env('PASSWORD_API')

URL_API = 'http://127.0.0.1:8085/'
# CONNECTION_TOKEN_API = 'e57f3a72-5508-4935-af3d-36ff98997239'
# CONNECTION_TOKEN_API = '1a2d5d4c-a525-4126-a76a-c7b0b878828e'
CONNECTION_TOKEN_API = 'e0a03a63-ca79-4121-9053-08b0f28a9077'
USERNAME_API = 'ettvcl'
PASSWORD_API = 'Zxc123*-'

NUMERACION_DOCUMENTOS_CONFIG = None
FECHAS_PROCESAMIENTO = None
OTRAS_CONFIGURACIONES = None

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}