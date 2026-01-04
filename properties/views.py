from rest_framework import generics, permissions
from .models import Property
from .serializers import PropertySerializer

class PropertyListCreateView(generics.ListCreateAPIView):
    serializer_class = PropertySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Property.objects.filter(manager=self.request.user)

    def perform_create(self, serializer):
        serializer.save(manager=self.request.user)

class PropertyDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PropertySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Property.objects.filter(manager=self.request.user)