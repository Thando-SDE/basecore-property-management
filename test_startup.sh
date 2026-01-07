#!/bin/bash
echo "=== Testing Django Startup ==="

# Test 1: Basic Django check
python manage.py check --settings=basecore.settings.production

# Test 2: Test imports
python -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'basecore.settings.production')
try:
    import django
    django.setup()
    print('✅ Django setup complete')
    
    # Test critical imports
    from django.contrib.auth import get_user_model
    print('✅ Auth imports work')
    
    from rest_framework.test import APIClient
    print('✅ DRF imports work')
    
    from basecore.views import health_check
    print('✅ Custom views import')
    
except Exception as e:
    print(f'❌ Import error: {e}')
    import traceback
    traceback.print_exc()
"

# Test 3: Try to run a simple server (timeout after 5 seconds)
echo -e "\n=== Testing server startup (5 second test) ==="
timeout 5 python manage.py runserver --settings=basecore.settings.production 0.0.0.0:8000 &
SERVER_PID=$!
sleep 3
if ps -p $SERVER_PID > /dev/null; then
    echo "✅ Server started successfully"
    kill $SERVER_PID 2>/dev/null
else
    echo "❌ Server failed to start"
fi
