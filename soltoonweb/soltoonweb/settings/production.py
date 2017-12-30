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

INSTALLED_APPS = INSTALLED_APPS + [
    'opbeat.contrib.django',
]

OPBEAT = {
    'ORGANIZATION_ID': '7fbb8834f86243438483759a7a293cec',
    'APP_ID': '6787f6306e',
    'SECRET_TOKEN': '2b5cb5e6452ca38f9746e5e263480dbcf6618f82',
}

MIDDLEWARE = MIDDLEWARE + [
    'opbeat.contrib.django.middleware.OpbeatAPMMiddleware',
]

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
