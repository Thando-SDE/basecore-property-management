from django.urls import path
from .views import (
    PaymentListCreateView,
    PaymentDetailView,
    CreatePaymentIntentView,
    MarkPaymentPaidView,
    StripeWebhookView
)

urlpatterns = [
    path('', PaymentListCreateView.as_view(), name='payment-list'),
    path('<int:pk>/', PaymentDetailView.as_view(), name='payment-detail'),
    path('<int:payment_id>/create-intent/', CreatePaymentIntentView.as_view(), name='create-payment-intent'),
    path('<int:pk>/mark-paid/', MarkPaymentPaidView.as_view(), name='mark-payment-paid'),
    path('webhook/', StripeWebhookView.as_view(), name='stripe-webhook'),
]