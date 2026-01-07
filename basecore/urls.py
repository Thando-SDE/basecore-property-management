"""basecore URL Configuration"""
from django.contrib import admin
from django.urls import path, include
from basecore.views import health_check  # IMPORT from views.py

urlpatterns = [
    # Health check - IMPORTED from views.py
    path('', health_check, name='health-check'),
    
    # Admin
    path('admin/', admin.site.urls),
    
    # API endpoints (JWT will be added AFTER app works)
    path('api/users/', include('users.urls')),
    path('api/properties/', include('properties.urls')),
    path('api/tenants/', include('tenants.urls')),
    path('api/leases/', include('leases.urls')),
    path('api/payments/', include('payments.urls')),
]
