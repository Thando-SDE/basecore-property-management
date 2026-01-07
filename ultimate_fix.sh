#!/bin/bash
echo "=== ULTIMATE FIX: Clean deployment ==="

# 1. Backup current files
mkdir -p backup
cp basecore/settings/production.py backup/
cp basecore/urls.py backup/

# 2. Create SIMPLE base.py if it doesn't exist
if [ ! -f "basecore/settings/base.py" ]; then
    cat > basecore/settings/base.py << 'BASEEOF'
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'users',
    'properties',
    'tenants',
    'leases',
    'payments',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'basecore.urls'
WSGI_APPLICATION = 'basecore.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'users.User'
BASEEOF
fi

# 3. Create SIMPLE production.py
cat > basecore/settings/production.py << 'PRODEOF'
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
PRODEOF

# 4. Create SIMPLE urls.py
cat > basecore/urls.py << 'URLSEOF'
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def health(request):
    return JsonResponse({"status": "ok", "service": "BaseCore"})

urlpatterns = [
    path('', health),
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/properties/', include('properties.urls')),
    path('api/tenants/', include('tenants.urls')),
    path('api/leases/', include('leases.urls')),
    path('api/payments/', include('payments.urls')),
]
URLSEOF

# 5. Create proper wsgi.py
cat > basecore/wsgi.py << 'WSGIEOF'
import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'basecore.settings.production')
application = get_wsgi_application()
WSGIEOF

# 6. Deploy
git add basecore/settings/production.py basecore/settings/base.py basecore/urls.py basecore/wsgi.py
git commit -m "ULTIMATE FIX: Completely clean deployment"
git push origin main

echo "✅ Ultimate fix deployed! Monitor with: railway logs --follow"
