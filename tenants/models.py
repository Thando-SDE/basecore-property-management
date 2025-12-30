from django.db import models
from django.conf import settings

class Tenant(models.Model):
    property = models.ForeignKey(
        'properties.Property',
        on_delete=models.CASCADE,
        related_name='tenants'
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    emergency_contact = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        unique_together = ['property', 'email']  # Same email can't be in same property twice