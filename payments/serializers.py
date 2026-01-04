from rest_framework import serializers
from datetime import date
from .models import Payment, PaymentIntent
from leases.serializers import LeaseSerializer

class PaymentSerializer(serializers.ModelSerializer):
    lease_detail = LeaseSerializer(source='lease', read_only=True)
    is_overdue = serializers.SerializerMethodField()
    
    class Meta:
        model = Payment
        fields = ('id', 'lease', 'lease_detail', 'amount', 'due_date', 
                 'status', 'stripe_payment_intent_id', 'paid_at', 
                 'is_overdue', 'created_at', 'updated_at')
        read_only_fields = ('status', 'stripe_payment_intent_id', 'paid_at', 
                           'created_at', 'updated_at')
    
    def get_is_overdue(self, obj):
        return obj.status == 'overdue' or (
            obj.status == 'pending' and obj.due_date < date.today()
        )
    
    def validate(self, data):
        # Check if lease belongs to logged-in user
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user = request.user
            if 'lease' in data and data['lease'].property.manager != user:
                raise serializers.ValidationError(
                    "You can only create payments for your own properties."
                )
        
        # Amount validation
        if 'amount' in data and data['amount'] <= 0:
            raise serializers.ValidationError(
                "Payment amount must be positive."
            )
        
        return data

class PaymentIntentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentIntent
        fields = ('id', 'payment', 'stripe_intent_id', 'client_secret', 
                 'status', 'created_at')
        read_only_fields = ('stripe_intent_id', 'client_secret', 'status', 
                           'created_at')