import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Determine environment
environment = os.environ.get('DJANGO_ENV', 'development').lower()

print(f"=== Loading {environment} settings ===")

if environment == 'production':
    from .production import *
    print("✓ Production settings loaded")
else:
    from .development import *
    print("✓ Development settings loaded")

# Verify critical settings
print(f"DEBUG: {DEBUG}")
print(f"ALLOWED_HOSTS: {ALLOWED_HOSTS}")
