from django.http import JsonResponse
from django.views.decorators.http import require_GET

@require_GET
def simple_health(request):
    """Simple health check that always works"""
    return JsonResponse({"status": "ok", "message": "API is running"})
