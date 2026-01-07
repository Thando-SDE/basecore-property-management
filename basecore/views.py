"""Views for basecore project"""
from django.http import JsonResponse
from django.views.decorators.http import require_GET

@require_GET
def health_check(request):
    """Health check endpoint for Railway"""
    return JsonResponse({
        "status": "healthy",
        "service": "BaseCore Property Management API",
        "version": "1.0.0",
        "database": "connected"
    })
