"""ULTRA SIMPLE URL config - just to test"""
from django.contrib import admin
from django.urls import path
from basecore.views import health_check, test_jwt

urlpatterns = [
    path('', health_check),
    path('test-jwt/', test_jwt),
    path('admin/', admin.site.urls),
]

# Test endpoints
from .test_views import test_headers, test_admin_simulation

urlpatterns += [
    path('test-headers/', test_headers),
    path('test-admin-sim/', test_admin_simulation),
]
