"""User URLs - ONLY user management, NO JWT"""
from django.urls import path
from .views import RegisterView, UserProfileView

urlpatterns = [
    path('', RegisterView.as_view(), name='register'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    # NO JWT endpoints here - they're in basecore/urls.py
]
