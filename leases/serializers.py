from rest_framework import serializers
from .models import Lease
from properties.serializers import PropertySerializer
from tenants.serializers import TenantSerializer

class LeaseSerializer(serializers.ModelSerializer):
    property_detail = PropertySerializer(source='property', read_only=True)
    tenant_detail = TenantSerializer(source='tenant', read_only=True)
    days_remaining = serializers.SerializerMethodField()
    
    class Meta:
        model = Lease
        fields = ('id', 'property', 'property_detail', 'tenant', 'tenant_detail',
                 'start_date', 'end_date', 'monthly_rent', 'security_deposit',
                 'status', 'days_remaining', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at', 'status')
    
    def get_days_remaining(self, obj):
        from datetime import date
        if obj.end_date and obj.status == 'active':
            remaining = (obj.end_date - date.today()).days
            return max(0, remaining)
        return 0
    
    def validate(self, data):
        # Check if property belongs to logged-in user
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user = request.user
            if 'property' in data and data['property'].manager != user:
                raise serializers.ValidationError(
                    "You can only create leases for your own properties."
                )
            
            # Check if tenant belongs to the property
            if 'tenant' in data and 'property' in data:
                if data['tenant'].property != data['property']:
                    raise serializers.ValidationError(
                        "Tenant must belong to the selected property."
                    )
        
        # Date validation
        if 'end_date' in data and 'start_date' in data:
            if data['end_date'] <= data['start_date']:
                raise serializers.ValidationError(
                    "End date must be after start date."
                )
        
        return data