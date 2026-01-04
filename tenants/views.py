from rest_framework import generics, permissions
from .models import Tenant
from .serializers import TenantSerializer
from properties.models import Property

class TenantListCreateView(generics.ListCreateAPIView):
    serializer_class = TenantSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user_properties = Property.objects.filter(manager=self.request.user)
        return Tenant.objects.filter(property__in=user_properties)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    def perform_create(self, serializer):
        property_obj = serializer.validated_data['property']
        if property_obj.manager != self.request.user:
            raise permissions.PermissionDenied(
                "You can only add tenants to your own properties."
            )
        serializer.save()

class TenantDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TenantSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user_properties = Property.objects.filter(manager=self.request.user)
        return Tenant.objects.filter(property__in=user_properties)