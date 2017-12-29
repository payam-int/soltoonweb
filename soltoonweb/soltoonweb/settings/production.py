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
