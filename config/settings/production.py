# NOTE: THIS FILE IS NOT TRACKED, SO ACTUAL PRODUCTION SETTINGS ARE DIFFERENT

from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'clickmanga',
        'USER': 'root',
        'PASSWORD': '',
    }
}

ALLOWED_HOSTS = [
    'clickmanga.xyz',
]

DEBUG = False
