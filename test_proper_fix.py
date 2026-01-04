import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'basecore.settings')
import django
django.setup()

from django.conf import settings
print(f"\n=== FINAL DJANGO SETTINGS ===")
print(f"DEBUG: {settings.DEBUG}")
print(f"ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
print(f"DATABASE ENGINE: {settings.DATABASES['default']['ENGINE']}")
