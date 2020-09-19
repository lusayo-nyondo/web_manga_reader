# NOTE: THIS FILE IS NOT TRACKED SO ACTUAL TESTING DETAILS ARE DIFFERENT

from .base import *

DEBUG = True

ALLOWED_HOSTS = [
    'neetlord.pythonanywhere.com',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'neetlord$mangapoint',
        'USER': 'neetlord',
        'HOST': 'neetlord.mysql.pythonanywhere-services.com',
        'PASSWORD': 'NyondoNyondo'
    }
}
