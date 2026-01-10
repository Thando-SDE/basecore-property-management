from django.contrib import admin
from .models import Payment, PaymentIntent

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'lease', 'amount', 'due_date', 'status', 'paid_at', 'created_at')
    list_filter = ('status', 'due_date')
    search_fields = ('lease__property__name', 'lease__tenant__first_name')
    ordering = ('-created_at',)

@admin.register(PaymentIntent)
class PaymentIntentAdmin(admin.ModelAdmin):
    list_display = ('id', 'payment', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('payment__lease__property__name',)
    ordering = ('-created_at',)
