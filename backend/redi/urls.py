"""
URL configuration for the REdI Trolley Audit System.
"""

from django.contrib import admin
from django.db import connection
from django.http import JsonResponse
from django.urls import include, path


def health_check(request):
    """Health check endpoint for Docker and monitoring."""
    try:
        connection.ensure_connection()
        db_ok = True
    except Exception:
        db_ok = False

    status = 200 if db_ok else 503
    return JsonResponse({
        'status': 'healthy' if db_ok else 'unhealthy',
        'database': 'connected' if db_ok else 'disconnected',
    }, status=status)


urlpatterns = [
    path('health/', health_check, name='health_check'),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('audit.urls')),
]

# Customize admin site
admin.site.site_header = 'REdI Trolley Audit Administration'
admin.site.site_title = 'REdI Admin'
admin.site.index_title = 'RBWH Resuscitation Trolley Audit System'
