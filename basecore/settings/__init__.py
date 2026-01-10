"""
Django settings module initialization.
Loads settings from base.py, development.py, or production.py
based on DJANGO_SETTINGS_MODULE environment variable.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Clear any Django cache if exists
import sys
if 'django.conf' in sys.modules:
    del sys.modules['django.conf']
