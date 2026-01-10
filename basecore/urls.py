"""BaseCore URL Configuration"""
from django.contrib import admin
from django.urls import path
from basecore.views import health_check, test_jwt

urlpatterns = [
    path('', health_check, name='health_check'),
    path('test-jwt/', test_jwt, name='test_jwt'),
    path('admin/', admin.site.urls),
]
