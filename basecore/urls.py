from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def health(request):
    return JsonResponse({"status": "ok", "service": "BaseCore"})

urlpatterns = [
    path('', health),
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/properties/', include('properties.urls')),
    path('api/tenants/', include('tenants.urls')),
    path('api/leases/', include('leases.urls')),
    path('api/payments/', include('payments.urls')),
]
