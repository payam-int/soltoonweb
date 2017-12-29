from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*.soltoon.net', 'soltoon.net']

EMAIL_USE_TLS = True
EMAIL_HOST = '127.0.0.1'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 25
DEFAULT_FROM_EMAIL = 'Soltoon <net@soltoon.net>'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'soltoon',
        'USER': os.environ['SOLTOON_DB_USERNAME'],
        'PASSWORD': os.environ['SOLTOON_DB_PASSWORD'],
        'HOST': 'localhost',
        'PORT': '',
    }
}

SECURE_SSL_REDIRECT = True
