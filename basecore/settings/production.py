from .base import *
import os
import dj_database_url

DEBUG = False

ALLOWED_HOSTS = [
    'pleasant-happiness.up.railway.app',
    '.railway.app',
    'localhost',
    '127.0.0.1',
    '0.0.0.0'
]

DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600,
    )
}

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

CSRF_TRUSTED_ORIGINS = [
    'https://pleasant-happiness.up.railway.app',
    'https://*.railway.app',
]

# Disable static files warning
import warnings
warnings.filterwarnings('ignore', message='No directory at:')
