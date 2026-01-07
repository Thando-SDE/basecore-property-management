import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'basecore.settings.production')
django.setup()

from django.test import RequestFactory
from basecore.views import health_check

rf = RequestFactory()
request = rf.get('/')
response = health_check(request)

print(f'Status Code: {response.status_code}')
print(f'Content: {response.content.decode()}')
print('✅ Health check works!')
