import os
import sys

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'basecore.settings.production')

import django
django.setup()

from django.conf import settings

print("=" * 60)
print("QUICK DIAGNOSIS")
print("=" * 60)

# 1. Check if REST Framework is installed
print("\n1. Checking Django REST Framework...")
if 'rest_framework' in settings.INSTALLED_APPS:
    print("   ✅ REST Framework is installed")
else:
    print("   ❌ REST Framework is NOT installed")

# 2. Check if Simple JWT is installed
print("\n2. Checking Simple JWT...")
if 'rest_framework_simplejwt' in settings.INSTALLED_APPS:
    print("   ✅ Simple JWT is installed")
else:
    print("   ❌ Simple JWT is NOT installed")

# 3. Check users app
print("\n3. Checking users app...")
if 'users' in settings.INSTALLED_APPS:
    print("   ✅ Users app is installed")
else:
    print("   ❌ Users app is NOT installed")

# 4. Quick URL test
print("\n4. Available URL patterns:")
try:
    from django.urls import get_resolver
    resolver = get_resolver()
    
    # Simple check for common patterns
    patterns_to_check = [
        'api/users/',
        'api/token/',
        'api/auth/',
        'api/login/',
        'api/register/'
    ]
    
    found_patterns = []
    for pattern in resolver.url_patterns:
        pattern_str = str(pattern.pattern)
        for check in patterns_to_check:
            if check in pattern_str:
                found_patterns.append(pattern_str)
    
    if found_patterns:
        for pattern in found_patterns:
            print(f"   ✅ Found: {pattern}")
    else:
        print("   ❓ No user/auth URLs found")
        
except Exception as e:
    print(f"   Error: {e}")

print("\n" + "=" * 60)
print("RECOMMENDATION:")
print("=" * 60)

# Give recommendation based on findings
if 'rest_framework_simplejwt' in settings.INSTALLED_APPS:
    print("Simple JWT is installed. Try these endpoints:")
    print("  - /api/token/ (POST for login)")
    print("  - /api/token/refresh/ (POST)")
else:
    print("Simple JWT not found. You might need to install it:")
    print("  pip install djangorestframework-simplejwt")
    print("  Add to INSTALLED_APPS: 'rest_framework_simplejwt'")

print("\nTo test: curl -X POST https://your-url/api/token/ \\")
print('  -H "Content-Type: application/json" \\')
print('  -d \'{"username": "youruser", "password": "yourpass"}\'')
