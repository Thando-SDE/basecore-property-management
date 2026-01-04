import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'basecore.settings')
import django
django.setup()

from django.conf import settings
print(f"=== SETTINGS CHECK ===")
print(f"DEBUG: {settings.DEBUG}")
print(f"ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
print(f"DATABASES engine: {settings.DATABASES['default']['ENGINE']}")
print(f"DATABASES name: {settings.DATABASES['default']['NAME']}")
