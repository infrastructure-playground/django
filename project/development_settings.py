import os

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'secret_key')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

CDN_HOSTNAME = os.environ.get('CDN_HOSTNAME')
if CDN_HOSTNAME:
    # put "CDN Credentials" here if any
    pass

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases
if os.environ.get('DOCKERIZED'):  # To avoid error in makemigrations during build
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'HOST': os.environ.get('POSTGRES_SERVICE'),
            'NAME': os.environ.get('POSTGRES_DB'),
            'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
            'PORT': os.environ.get('POSTGRES_PORT'),
            'USER': os.environ.get('POSTGRES_USER')
        }
    }
