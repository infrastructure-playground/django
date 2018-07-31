import os
from configparser import SafeConfigParser
from django.conf import settings

config_file = os.path.join(settings.BASE_DIR, 'settings', 'configs.cfg')
config_parser = SafeConfigParser()
config_parser.read(config_file)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config_parser.get('django', 'SECRET_KEY')

DEBUG = False

CDN_HOSTNAME = config_parser.get('file_storage', 'CDN_HOSTNAME')

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': config_parser.get('postgres', 'SERVICE'),
        'NAME': config_parser.get('postgres', 'DB'),
        'PASSWORD': config_parser.get('postgres', 'PASSWORD'),
        'PORT': config_parser.get('postgres', 'PORT'),
        'USER': config_parser.get('postgres', 'USER')
    }
}
