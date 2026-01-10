"""Simple views for testing"""
from django.http import JsonResponse
from django.views.decorators.http import require_GET

@require_GET
def health_check(request):
    """Ultra-simple health check"""
    return JsonResponse({
        "status": "ok",
        "app": "BaseCore",
        "simple": True
    })

@require_GET  
def test_jwt(request):
    """Test if JWT is importable"""
    try:
        from rest_framework_simplejwt.views import TokenObtainPairView
        return JsonResponse({"jwt": "importable", "status": "ok"})
    except ImportError as e:
        return JsonResponse({"jwt": "not_importable", "error": str(e)})
