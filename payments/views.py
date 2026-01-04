import stripe
from datetime import date
from django.conf import settings
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Payment, PaymentIntent
from .serializers import PaymentSerializer, PaymentIntentSerializer
from leases.models import Lease

# Initialize Stripe (test mode)
stripe.api_key = settings.STRIPE_SECRET_KEY if hasattr(settings, 'STRIPE_SECRET_KEY') else 'sk_test_placeholder'

class PaymentListCreateView(generics.ListCreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Users can only see payments for THEIR properties
        user_leases = Lease.objects.filter(property__manager=self.request.user)
        return Payment.objects.filter(lease__in=user_leases)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    def perform_create(self, serializer):
        serializer.save()

class PaymentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user_leases = Lease.objects.filter(property__manager=self.request.user)
        return Payment.objects.filter(lease__in=user_leases)

class CreatePaymentIntentView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, payment_id):
        try:
            # Verify user owns this payment
            user_leases = Lease.objects.filter(property__manager=request.user)
            payment = Payment.objects.get(id=payment_id, lease__in=user_leases)
            
            # Create Stripe payment intent (in test mode)
            intent = stripe.PaymentIntent.create(
                amount=int(payment.amount * 100),  # Convert to cents
                currency='zar',
                metadata={
                    'payment_id': payment.id,
                    'lease_id': payment.lease.id,
                    'property_id': payment.lease.property.id
                }
            )
            
            # Save payment intent
            payment_intent = PaymentIntent.objects.create(
                payment=payment,
                stripe_intent_id=intent.id,
                client_secret=intent.client_secret,
                status=intent.status
            )
            
            # Update payment with Stripe ID
            payment.stripe_payment_intent_id = intent.id
            payment.save()
            
            serializer = PaymentIntentSerializer(payment_intent)
            return Response(serializer.data)
            
        except Payment.DoesNotExist:
            return Response(
                {"error": "Payment not found or access denied"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

class MarkPaymentPaidView(generics.UpdateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user_leases = Lease.objects.filter(property__manager=self.request.user)
        return Payment.objects.filter(lease__in=user_leases)
    
    def update(self, request, *args, **kwargs):
        payment = self.get_object()
        payment.status = 'paid'
        payment.paid_at = date.today()
        payment.save()
        serializer = self.get_serializer(payment)
        return Response(serializer.data)

@method_decorator(csrf_exempt, name='dispatch')
class StripeWebhookView(APIView):
    """Handle Stripe webhooks for payment status updates"""
    
    def post(self, request):
        # In production, verify Stripe signature
        payload = request.body
        event = None
        
        try:
            event = stripe.Event.construct_from(
                json.loads(payload), stripe.api_key
            )
        except ValueError as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        # Handle specific event types
        if event.type == 'payment_intent.succeeded':
            payment_intent = event.data.object
            self.handle_payment_success(payment_intent)
        elif event.type == 'payment_intent.payment_failed':
            payment_intent = event.data.object
            self.handle_payment_failure(payment_intent)
        
        return Response(status=status.HTTP_200_OK)
    
    def handle_payment_success(self, payment_intent):
        try:
            payment = Payment.objects.get(
                stripe_payment_intent_id=payment_intent.id
            )
            payment.status = 'paid'
            payment.paid_at = date.today()
            payment.save()
            
            # Update payment intent
            PaymentIntent.objects.filter(
                stripe_intent_id=payment_intent.id
            ).update(status='succeeded')
            
        except Payment.DoesNotExist:
            pass
    
    def handle_payment_failure(self, payment_intent):
        try:
            payment = Payment.objects.get(
                stripe_payment_intent_id=payment_intent.id
            )
            payment.status = 'failed'
            payment.save()
            
            PaymentIntent.objects.filter(
                stripe_intent_id=payment_intent.id
            ).update(status='failed')
            
        except Payment.DoesNotExist:
            pass