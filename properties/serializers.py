from rest_framework import serializers
from .models import Property

class PropertySerializer(serializers.ModelSerializer):
    manager_name = serializers.CharField(source='manager.username', read_only=True)
    
    class Meta:
        model = Property
        fields = ('id', 'name', 'address', 'monthly_rent', 'description', 
                 'is_active', 'manager', 'manager_name', 'created_at')
        read_only_fields = ('manager', 'created_at', 'updated_at')  
        extra_kwargs = {
            'manager': {'required': False} 
        }