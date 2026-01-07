"""
Production settings for BaseCore Property Management
"""
import os
import dj_database_url
from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Railway URL
ALLOWED_HOSTS = [
    'pleasant-happiness.up.railway.app',
    '.railway.app',
    'localhost',
    '127.0.0.1',
    '0.0.0.0'
]

# Database
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# Security
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# CSRF trusted origins
CSRF_TRUSTED_ORIGINS = [
    'https://pleasant-happiness.up.railway.app',
    'https://*.railway.app',
]

# Disable warnings
import warnings
warnings.filterwarnings('ignore', message='No directory at:')
