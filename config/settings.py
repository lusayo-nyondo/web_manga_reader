"""
This file has to be modified based on the deployment environment.
For this branch, it is suited towards neetlord.pythonanywhere.com.
"""

import os
import django
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(BASE_DIR)

# Add the site application root to the import path here, because django seems to disobey regular python
# import rules.
SITE_APP_ROOT = os.path.dirname(BASE_DIR)
sys.path.append(SITE_APP_ROOT)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '5j1c=bf12)vhnu%qymy!2j9nt8a3$(2srgfxh_n*8qwpdq#ovs'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

LIVE_HOST = 'localhost:8000'

LOGIN_URL = '/account/sign_in'
LOGOUT_URL = '/account/logout'

LOGIN_REDIRECT_URL = '/manga_list'

SOCIAL_AUTH_GITHUB_KEY = '88ea351bc7fc238dae9f'
SOCIAL_AUTH_GITHUB_SECRET = 'ef771cdde71445d7e0493699781baf864d4492c5'

SOCIAL_AUTH_FACEBOOK_KEY = '563892190925479'
SOCIAL_AUTH_FACEBOOK_SECRET = 'a38bea84f5e5e872a7588e1b1f80d9dd'

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '931797996770-93hjribfjpvrv66bkgceu63rpibk93vb.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'rNvzHxJ9XrQSzV4Ywa9hHdze'

SOCIAL_AUTH_URL_NAMESPACE = 'social'

ALLOWED_HOSTS = [
    'neetlord.pythonanywhere.com',
    'localhost',
    '127.0.0.1',
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'social_django',

    'users',
    'manga',
    'user_manga_integration',
    'social_integration',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'social_django.middleware.SocialAuthExceptionMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'social_django.context_processors.backends',  # <--
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'neetlord$mangapoint',
        'USER': 'neetlord',
        'HOST': 'neetlord.mysql.pythonanywhere-services.com',
        'PASSWORD': 'NyondoNyondo',
        #'NAME': 'mangapoint',
        #'USER': 'root',
        #'PASSWORD': '',
        'PORT': '3306'
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

WORKSPACE_ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '/workspaces/')

AUTH_USER_MODEL = "users.SiteUser"

AUTHENTICATION_BACKENDS = (
    'social_core.backends.github.GithubOAuth2',
    'social_core.backends.twitter.TwitterOAuth',
    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)