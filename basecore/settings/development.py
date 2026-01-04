# basecore/settings/development.py
from .base import *

# Remove any DEBUG or ALLOWED_HOSTS from base imports
# by overriding them explicitly
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0', '::1']

print(f"DEBUG set to: {DEBUG}")
print(f"ALLOWED_HOSTS set to: {ALLOWED_HOSTS}")

# SQLite database for development
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Disable SSL in development
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False