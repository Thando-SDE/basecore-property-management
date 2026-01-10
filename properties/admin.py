from django.contrib import admin
from .models import Property

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('name', 'manager', 'address', 'monthly_rent', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')  # Removed property_type
    search_fields = ('name', 'address', 'description')
    ordering = ('-created_at',)
