# from dotenv import load_dotenv
"""
Django settings for flujo_costo project.

Generated by 'django-admin startproject' using Django 5.0.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os
from datetime import timedelta
import environ
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _, get_language
from easy_thumbnails.conf import Settings as Thumbnail_Settings

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent

# env = environ.Env()
env = environ.Env()

environ.Env.read_env(os.path.join(BASE_DIR, '.env.local'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG', default=True)

ALLOWED_HOSTS = ['*']

# Application definition


DJANGO_APPS = [
    # 'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.forms',
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
]

MY_APPS = [
    'codificadores.apps.CodificadoresConfig',
    'configuracion.apps.ConfiguracionConfig',
    'flujo.apps.FlujoConfig',
    'costo.apps.CostoConfig',
    'app_index',
    'app_auth.usuarios',
    'app_auth.grupos',
    'app_auth.permisos',
    'cruds_adminlte3',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_APPS + MY_APPS

CRISPY_TEMPLATE_PACK = 'bootstrap4'

IMAGE_CROPPING_JQUERY_URL = None

INTERNAL_IPS = ('127.0.0.1',)

THUMBNAIL_PROCESSORS = (
                           'image_cropping.thumbnail_processors.crop_corners',
                       ) + Thumbnail_Settings.THUMBNAIL_PROCESSORS

TIME_FORMAT = 'h:i A'
DATETIME_FORMAT = 'd/m/Y H:i:s'
DATE_FORMAT = 'd/m/Y'

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django_session_timeout.middleware.SessionTimeoutMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.admindocs.middleware.XViewMiddleware',
    'django_htmx.middleware.HtmxMiddleware',
    'app_auth.usuarios.middleware.OneSessionPerUserMiddleware',
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
    # 'JWT_AUTH_HEADER_PREFIX': 'Bearer', # <---------- Comentariar esta línea cuando no se pruebe con 'Postman'
}

ROOT_URLCONF = 'urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'wsgi.application'


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
        options.update({'NAME': os.path.join(BASE_DIR, options['NAME'])})

    return options


#
DATABASES = {
    'default': get_db_config()
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

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'es-es'

TIME_ZONE = 'America/Havana'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

STATICFILES_DIRS = [
    BASE_DIR / 'app_index/static',
    BASE_DIR / 'cruds_adminlte3/static'
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

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
        # "datetime": {
        #     "format": "MM/DD/YYYY HH:mm",
        # },
        # "month": {
        #     "format": "MMMM, YYYY",
        # },
    },
    "datetimepicker_js_url": "/static/plugins/bootstrap-datetimepicker/4_17_47/bootstrap-datetimepicker.js",
    "datetimepicker_css_url": "/static/plugins/bootstrap-datetimepicker/4_17_47/bootstrap-datetimepicker.css",
    "bootstrap_icon_css_url": "/static/plugins/bootstrap-icons/font/bootstrap-icons.css",
    "app_static_url": "/static/plugins/bootstrap_datepicker_plus/",
    "momentjs_url": None,  # If you already have momentjs added into your template
}

# Session expiration
SESSION_EXPIRE_SECONDS = 600  # 10 minutos

LOGIN_REDIRECT_URL = reverse_lazy('app_index:index')

SESSION_TIMEOUT_REDIRECT = reverse_lazy('app_index:usuario:login')

SESSION_EXPIRE_AFTER_LAST_ACTIVITY = True

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "django.contrib.auth.backends.AllowAllUsersModelBackend",
    # "guardian.backends.ObjectPermissionBackend",
)