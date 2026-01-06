"""
Production settings for BaseCore Property Management
"""
import os
import dj_database_url
from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Railway provides the DATABASE_URL environment variable
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Allowed hosts - FIXED FOR RAILWAY
ALLOWED_HOSTS = [
    'pleasant-happiness.up.railway.app',
    '.railway.app',
    'localhost',
    '127.0.0.1',
    '0.0.0.0'
]

# CSRF trusted origins
CSRF_TRUSTED_ORIGINS = [
    'https://pleasant-happiness.up.railway.app',
    'https://*.railway.app'
]

# Comment out drf_spectacular for now to avoid import errors
# INSTALLED_APPS = [app for app in INSTALLED_APPS if app != 'drf_spectacular']
