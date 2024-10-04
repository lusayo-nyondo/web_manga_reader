# NOTE: THIS FILE IS NOT TRACKED, SO ACTUAL PRODUCTION SETTINGS ARE DIFFERENT
from config.settings.base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

ALLOWED_HOSTS = [
    'pornhwa.online',
]

DEBUG = False
SSH_WELL_KNOWN = '/home/clickmanga/public_html/.well-known/'
