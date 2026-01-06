"""
WSGI config for basecore project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# IMPORTANT: Use production settings on Railway
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'basecore.settings.production')

application = get_wsgi_application()
