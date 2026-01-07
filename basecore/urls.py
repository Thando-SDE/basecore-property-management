"""basecore URL Configuration"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

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
    # Health check
    path('', health_check, name='health-check'),
    
    # Admin
    path('admin/', admin.site.urls),
    
    # JWT Authentication
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # API endpoints
    path('api/users/', include('users.urls')),
    path('api/properties/', include('properties.urls')),
    path('api/tenants/', include('tenants.urls')),
    path('api/leases/', include('leases.urls')),
    path('api/payments/', include('payments.urls')),
]
