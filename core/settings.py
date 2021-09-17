# -*- encoding: utf-8 -*-


import os

import dj_database_url
import environ
from decouple import config
from django.utils.translation import ugettext_lazy as _
from unipath import Path

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
env = environ.Env(DEBUG=(bool, False), ENABLE_TENANT_SCHEMAS=(bool, False))
environ.Env.read_env()  # reading .env file
######
BASE_DIR = Path(__file__).parent
CORE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='S#perS3crEt_1122')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

# load production server from .env
ALLOWED_HOSTS = ['*', '127.0.0.1', config('SERVER', default='127.0.0.1')]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'widget_tweaks',
    'rest_framework',
    # 'rest_framework_api_key',
    'drf_spectacular',
    'rosetta',
    # 'chartjs',
    'django_extensions',
    'common',
    'authentication',
    'app'  # Enable the inner app 
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'
LOGIN_REDIRECT_URL = "home"  # Route defined in app/urls.py
LOGOUT_REDIRECT_URL = "home"  # Route defined in app/urls.py
TEMPLATE_DIR = os.path.join(CORE_DIR, "core/templates")  # ROOT dir for templates

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {"default": dj_database_url.config(conn_max_age=600)}

# Rosetta
ROSETTA_SHOW_AT_ADMIN_PANEL = True
ROSETTA_STORAGE_CLASS = 'rosetta.storage.CacheRosettaStorage'
LANGUAGES = [
    # ('en', _('English')),
    ('es', _('Spanish')),
]
LOCALE_PATHS = (os.path.join(CORE_DIR, 'core/locale'),)


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = env('LANGUAGE_CODE', default='es-UY')

TIME_ZONE = env('LANGUAGE_CODE', default='America/Montevideo')

USE_I18N = True

USE_L10N = True

USE_TZ = True

#############################################################
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_ROOT = os.path.join(CORE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(CORE_DIR, 'core/static'),
)
#############################################################
ADMIN_EMAIL = env('ADMIN_EMAIL', default=None)
ADMIN_USERNAME = env('ADMIN_USERNAME', default=None)
ADMIN_PASSWORD = env('ADMIN_PASSWORD', default=None)

#############################################################
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DATETIME_FORMAT': '%d/%m/%y %H:%M',
    'DATE_FORMAT': '%d/%m/%Y',

    # config for djangorestframework-datatables
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
        'rest_framework_datatables.renderers.DatatablesRenderer',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework_datatables.pagination.DatatablesPageNumberPagination',
    'PAGE_SIZE': 50,

    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'SGM-API',
    'DESCRIPTION': 'This API exposes all the necessary methods for managing the mobile app and frontend',
    'VERSION':  env('API_VERSION', default='1.0.0'),
    # OTHER SETTINGS
}
#############################################################
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': env('LOG_LEVEL', default='INFO'),
    },
}
#############################################################

MY_TEMPLATES_SETTINGS = {
    'DOMAIN': env('DOMAIN', default='localhost:8000'),
    'SIDEBAR_LOGO': env('SIDEBAR_LOGO', default='/static/favicon.ico'),
    'SIDEBAR_TITLE': env('SIDEBAR_TITLE', default='SGM'),
}
#############################################################
# EMAIL_USE_TLS = True
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = env('EMAIL_HOST')
# EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
# EMAIL_HOST_USER = env('EMAIL_HOST_USER')
# EMAIL_PORT = env('EMAIL_PORT')
# EMAIL_TO = env('EMAIL_TO').split(',')
# DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
# FROM_EMAIL = EMAIL_HOST_USER
#############################################################
