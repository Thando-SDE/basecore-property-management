from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.utils import timezone
from datetime import date
from .models import Lease
from .serializers import LeaseSerializer
from properties.models import Property

class LeaseListCreateView(generics.ListCreateAPIView):
    serializer_class = LeaseSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Users can only see leases for THEIR properties
        user_properties = Property.objects.filter(manager=self.request.user)
        return Lease.objects.filter(property__in=user_properties)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    def perform_create(self, serializer):
        # Automatically set property manager validation is in serializer
        serializer.save()

class LeaseDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LeaseSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user_properties = Property.objects.filter(manager=self.request.user)
        return Lease.objects.filter(property__in=user_properties)

class LeaseTerminateView(generics.UpdateAPIView):
    serializer_class = LeaseSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user_properties = Property.objects.filter(manager=self.request.user)
        return Lease.objects.filter(property__in=user_properties)
    
    def update(self, request, *args, **kwargs):
        lease = self.get_object()
        lease.status = 'terminated'
        lease.save()
        serializer = self.get_serializer(lease)
        return Response(serializer.data)

class LeaseRenewView(generics.UpdateAPIView):
    serializer_class = LeaseSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user_properties = Property.objects.filter(manager=self.request.user)
        return Lease.objects.filter(property__in=user_properties)
    
    def update(self, request, *args, **kwargs):
        lease = self.get_object()
        new_end_date = request.data.get('new_end_date')
        
        if not new_end_date:
            return Response(
                {"error": "new_end_date is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            from datetime import datetime
            new_end = datetime.strptime(new_end_date, '%Y-%m-%d').date()
            if new_end <= lease.end_date:
                return Response(
                    {"error": "New end date must be after current end date"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            lease.end_date = new_end
            lease.save()
            serializer = self.get_serializer(lease)
            return Response(serializer.data)
            
        except ValueError:
            return Response(
                {"error": "Invalid date format. Use YYYY-MM-DD"},
                status=status.HTTP_400_BAD_REQUEST
            )