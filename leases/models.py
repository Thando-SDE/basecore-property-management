from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

class Lease(models.Model):
    LEASE_STATUS = [
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('terminated', 'Terminated'),
    ]
    
    property = models.ForeignKey(
        'properties.Property',
        on_delete=models.CASCADE,
        related_name='leases'
    )
    tenant = models.ForeignKey(
        'tenants.Tenant',
        on_delete=models.CASCADE,
        related_name='leases'
    )
    start_date = models.DateField()
    end_date = models.DateField()
    monthly_rent = models.DecimalField(max_digits=10, decimal_places=2)
    security_deposit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=LEASE_STATUS, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Lease {self.id} - {self.property.name}"
    
    def clean(self):
        """Validate lease dates"""
        if self.end_date <= self.start_date:
            raise ValidationError("End date must be after start date")
        if self.monthly_rent <= 0:
            raise ValidationError("Monthly rent must be positive")
    
    def save(self, *args, **kwargs):
        self.full_clean()  # Run validation before saving
        super().save(*args, **kwargs)