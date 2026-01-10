from django.utils.deprecation import MiddlewareMixin

class ForceHTMLContentTypeMiddleware(MiddlewareMixin):
    """
    Middleware to force Content-Type: text/html for admin pages
    """
    def process_response(self, request, response):
        path = request.path
        
        # Apply to admin and static admin files
        if path.startswith('/admin/') or path.startswith('/static/admin/'):
            response['Content-Type'] = 'text/html; charset=utf-8'
            # Prevent browsers from sniffing content type
            response['X-Content-Type-Options'] = 'nosniff'
        
        return response

class DebugHeadersMiddleware(MiddlewareMixin):
    """
    Middleware to add debug headers for Railway health checks
    """
    def process_response(self, request, response):
        # Add debugging headers
        response['X-Django-Debug'] = 'true'
        response['X-Request-Path'] = request.path
        return response