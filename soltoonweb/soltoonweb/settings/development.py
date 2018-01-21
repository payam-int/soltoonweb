from .base import *

ALLOWED_HOSTS = ['*']

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

SOLTOON_SANDBOX = {
    'main-class': 'AI.java',
    'jar-directory': '~/.soltoonsandbox/jars/',
    'library': '/home/payam/PycharmProjects/soltoonweb/soltoonweb/libraries/soltoon-game-1.1.2-jar-with-dependencies.jar',
    'docker-images': {
        'code2jar': 'code2jar'
    }
}
