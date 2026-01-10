"""BaseCore URL Configuration"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from basecore.views import health_check, test_jwt

urlpatterns = [
    # Root and health check
    path('', health_check, name='health_check'),
    path('health/', health_check, name='health_check'),
    
    # Test endpoint
    path('test-jwt/', test_jwt, name='test_jwt'),
    
    # JWT Authentication endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Admin
    path('admin/', admin.site.urls),
    
    # API endpoints for each app
    path('api/users/', include('users.urls')),
    path('api/properties/', include('properties.urls')),
    path('api/tenants/', include('tenants.urls')),
    path('api/leases/', include('leases.urls')),
    path('api/payments/', include('payments.urls')),
]

print(f"=== URL CONFIG LOADED ===")
print(f"Total patterns: {len(urlpatterns)}")
for url in urlpatterns:
    print(f"  {url.pattern}")
