from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from .test_views import simple_health

@require_GET
def health_check(request):
    """Health check endpoint for Railway"""
    return JsonResponse({
        "status": "healthy",
        "service": "BaseCore Property Management API",
        "version": "1.0.0",
        "database": "connected"
    })

urlpatterns = [
    path('', health_check, name='health-check'),
    path('health/', simple_health, name='simple-health'),  # Simple always-works endpoint
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/properties/', include('properties.urls')),
    path('api/tenants/', include('tenants.urls')),
    path('api/leases/', include('leases.urls')),
    path('api/payments/', include('payments.urls')),
]
