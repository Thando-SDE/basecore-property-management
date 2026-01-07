"""basecore URL Configuration - WITH WORKING JWT"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from basecore.views import health_check

urlpatterns = [
    # Health check
    path('', health_check, name='health-check'),
    
    # Admin
    path('admin/', admin.site.urls),
    
    # JWT Authentication - CRITICAL: These MUST be here
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # API endpoints
    path('api/users/', include('users.urls')),
    path('api/properties/', include('properties.urls')),
    path('api/tenants/', include('tenants.urls')),
    path('api/leases/', include('leases.urls')),
    path('api/payments/', include('properties.urls')),
]

# Debug: Show URLs
print("✅ URLs configured with JWT endpoints")
