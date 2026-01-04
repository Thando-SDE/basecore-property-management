from django.urls import path
from .views import (
    LeaseListCreateView, 
    LeaseDetailView,
    LeaseTerminateView,
    LeaseRenewView
)

urlpatterns = [
    path('', LeaseListCreateView.as_view(), name='lease-list'),
    path('<int:pk>/', LeaseDetailView.as_view(), name='lease-detail'),
    path('<int:pk>/terminate/', LeaseTerminateView.as_view(), name='lease-terminate'),
    path('<int:pk>/renew/', LeaseRenewView.as_view(), name='lease-renew'),
]