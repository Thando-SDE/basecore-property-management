from rest_framework import serializers
from .models import Tenant
from properties.models import Property
from properties.serializers import PropertySerializer

class TenantSerializer(serializers.ModelSerializer):
    property_detail = PropertySerializer(source='property', read_only=True)
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Tenant
        fields = ('id', 'property', 'property_detail', 'first_name', 'last_name', 
                 'full_name', 'email', 'phone', 'emergency_contact', 
                 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    
    def validate(self, data):
        # Check if property belongs to the logged-in user
        user = self.context['request'].user
        if 'property' in data and data['property'].manager != user:
            raise serializers.ValidationError(
                "You can only add tenants to your own properties."
            )
        
        # Check for duplicate email in same property
        if 'property' in data and 'email' in data:
            if Tenant.objects.filter(
                property=data['property'], 
                email=data['email']
            ).exists():
                raise serializers.ValidationError(
                    "A tenant with this email already exists in this property."
                )
        
        return data