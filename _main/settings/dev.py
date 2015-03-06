from .base import *

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': 'localhost',
        'PORT': '5432',
        'NAME': 'bok_db',
        'USER': 'postgres',
        'PASSWORD': 'abcd1234',
        'OPTIONS': {
            "autocommit": True,
        },
    }
}
