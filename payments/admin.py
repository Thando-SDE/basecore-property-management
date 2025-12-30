from django.contrib import admin
from .models import Payment, PaymentIntent

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'lease', 'amount', 'due_date', 'status', 'paid_at')
    list_filter = ('status', 'due_date')
    search_fields = ('lease__property__name', 'lease__tenant__first_name')

@admin.register(PaymentIntent)
class PaymentIntentAdmin(admin.ModelAdmin):
    list_display = ('id', 'payment', 'status', 'created_at')
    list_filter = ('status',)