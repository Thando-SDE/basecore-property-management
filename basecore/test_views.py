from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def test_headers(request):
    """Test endpoint to check what headers are being sent"""
    html = """
    <!DOCTYPE html>
    <html>
    <head><title>Test</title></head>
    <body>
        <h1>Test Page</h1>
        <p>If you can see this styled, HTML is working.</p>
    </body>
    </html>
    """
    response = HttpResponse(html)
    # Explicitly set content type
    response['Content-Type'] = 'text/html; charset=utf-8'
    return response

@csrf_exempt 
def test_admin_simulation(request):
    """Simulate admin page without admin templates"""
    from django.contrib.auth.models import User
    from django.contrib.auth.models import Group
    
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Admin Sim</title>
        <style>
            body { font-family: Arial; margin: 20px; }
            h1 { color: #333; }
            table { border-collapse: collapse; width: 100%; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            th { background-color: #f2f2f2; }
        </style>
    </head>
    <body>
        <h1>Admin Simulation</h1>
        <p>If this shows as styled HTML, templates work.</p>
        <table>
            <tr><th>Model</th><th>Count</th></tr>
            <tr><td>Users</td><td>%d</td></tr>
            <tr><td>Groups</td><td>%d</td></tr>
        </table>
    </body>
    </html>
    """ % (User.objects.count(), Group.objects.count())
    
    response = HttpResponse(html)
    response['Content-Type'] = 'text/html; charset=utf-8'
    return response
