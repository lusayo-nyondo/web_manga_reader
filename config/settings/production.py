# NOTE: THIS FILE IS NOT TRACKED, SO ACTUAL PRODUCTION SETTINGS ARE DIFFERENT
from config.settings.base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'clickmanga',
        'USER': 'clickmanga',
        'PASSWORD': 'clickmanga-program',
    }
}

ALLOWED_HOSTS = [
    'clickmanga.xyz',
]

DEBUG = False
SSH_WELL_KNOWN = '/home/clickmanga/public_html/.well-known/'
