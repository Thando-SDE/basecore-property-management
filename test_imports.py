import os
import sys

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'basecore.settings.production')

try:
    import django
    django.setup()
    print("✅ Django setup successful")
    
    # Test imports
    from basecore.views import health_check
    print("✅ Health check import successful")
    
    from rest_framework_simplejwt.views import TokenObtainPairView
    print("✅ JWT imports successful")
    
    # Test a simple request
    from django.test import RequestFactory
    rf = RequestFactory()
    request = rf.get('/')
    response = health_check(request)
    print(f"✅ Health check returns: {response.status_code}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
