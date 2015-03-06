"""
Django settings for _main project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'hedp(ir(kxva)uauzc5^z^p9_t8_@rqfwn2u1jamj(ftv$5or8'

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


INSTALLED_APPS = (
    'grappelli',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'django_extensions',
    'account',
    'company',
    'customer',
    'util',
    'price',
    'boat',
    'cancel',
    # 'offer',
    'order',
    'amenity',
    'maintenance',
    'review',
    'manager',
)

AUTH_USER_MODEL = 'account.BaseUser'

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = '_main.urls'

WSGI_APPLICATION = '_main.wsgi.application'


STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
)

# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
ADMINS = (('Arun', 'arunghosh@gmail.com'),)
TIME_FORMAT = "%d %b %Y T %X"
DATE_FORMAT = "%Y-%m-%d"

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = '/media/'

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

GRAPPELLI_ADMIN_TITLE = "Boats of Kerala"

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'rdtcontacttree@gmail.com'
EMAIL_HOST_PASSWORD = 'invincible123#$'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# handler404 = 'manage.views.error.404_view'
