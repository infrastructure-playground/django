"""
Django settings for project project.

Generated by 'django-admin startproject' using Django 2.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import datetime

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!


# SECURITY WARNING: don't run with debug turned on in production!


ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

START_APPS = [
    'authentication',
    'inventory',
]
INSTALLED_APPS += START_APPS

THIRD_PARTY_APPS = [
    'rest_framework',
    'corsheaders',
]
INSTALLED_APPS += THIRD_PARTY_APPS

CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_WHITELIST = (
    '127.0.0.1:4200',
    'localhost:4200',
    'localhost'
)

if os.environ.get('WHITELIST'):
    whitelist = os.environ['WHITELIST']
    for host in whitelist.split(','):
        CORS_ORIGIN_WHITELIST += (host,)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'project.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Singapore'

USE_I18N = True

USE_L10N = True

USE_TZ = True

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        # 'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    )
}

JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(hours=1),
    # 'JWT_ALLOW_REFRESH': True,
}


# AUTH_USER_MODEL = 'authentication.Account'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = 'static'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

LOGGING = {
           'version': 1,
           'disable_existing_loggers': False,
           'formatters': {
               'verbose': {
                   'format': '[%(asctime)s][%(name)s:%(lineno)s][%(levelname)s] %(message)s',
                   'datefmt': '%Y/%b/%d %H:%M:%S'
               },
               'colored': {'()': 'colorlog.ColoredFormatter',
                           'format': '[%(log_color)s%(asctime)s%(reset)s][%(name)s:%(lineno)s][%(log_color)s%(levelname)s%(reset)s] %(message)s',
                           'datefmt': '%Y/%b/%d %H:%M:%S',
                           'log_colors': {'DEBUG': 'cyan',
                                          'INFO': 'green',
                                          'WARNING': 'bold_yellow',
                                          'ERROR': 'red',
                                          'CRITICAL': 'red,bg_white'},
                           'secondary_log_colors': {},
                           'style': '%'},
           },
           'handlers': {
               'console': {
                   'level': 'DEBUG',
                   'class': 'logging.StreamHandler',
                   'formatter': 'colored'
               },
               'mail_admins': {
                   'level': 'ERROR',
                   'class': 'django.utils.log.AdminEmailHandler',
               },
           },
           'loggers': {
               'django': {
                   'handlers': ['console'],
                   'propagate': True,
               },
               'django.request': {
                   'handlers': ['mail_admins'],
                   'level': 'ERROR',
               },
           }
}
__app_logging = {'handlers': ['console', ],
                 'level': 'DEBUG',
                 'propagate': True}
for proj_app in START_APPS:
    LOGGING.get('loggers').update({proj_app: __app_logging})

if os.environ.get('ENV') == 'prod':
    from .production_settings import *
elif os.environ.get('ENV') == 'test':
    from .test_settings import *
else:
    DEV_APPS = [
        'drf_yasg',
    ]
    INSTALLED_APPS += DEV_APPS
    from .development_settings import *

# Google Cloud Environments
if os.environ.get('GAE_INSTANCE'):  # Google App Engine cloud deployment
  from .gae_settings import *

if os.environ.get('GKE'):
  from .gke_settings import *


if os.environ.get('TEST_DB_ENV'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
