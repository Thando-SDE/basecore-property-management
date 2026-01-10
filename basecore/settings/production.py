"""
Production settings for BaseCore Property Management
"""
import os
import dj_database_url
from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# IMPORTANT: Railway domain - this MUST match your actual Railway domain
ALLOWED_HOSTS = [
    'basecore-property-management-production.up.railway.app',
    '.railway.app',
    'localhost',
    '127.0.0.1',
    '0.0.0.0'
]

# Database from Railway environment variable
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# TEMPORARILY disable security for debugging
SECURE_SSL_REDIRECT = False  # Set to True after fixing
SESSION_COOKIE_SECURE = False  # Set to True after fixing  
CSRF_COOKIE_SECURE = False  # Set to True after fixing
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# CSRF trusted origins
CSRF_TRUSTED_ORIGINS = [
    'https://basecore-property-management-production.up.railway.app',
    'https://*.railway.app',
]

# Static files - ensure they're served correctly
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Disable the annoying staticfiles warning
import warnings
warnings.filterwarnings('ignore', message='No directory at:')

print(f"=== PRODUCTION SETTINGS LOADED ===")
print(f"DEBUG: {DEBUG}")
print(f"ALLOWED_HOSTS: {ALLOWED_HOSTS}")
print(f"STATIC_ROOT: {STATIC_ROOT}")
