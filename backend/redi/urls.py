"""
URL configuration for the REdI Trolley Audit System.
"""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('audit.urls')),
]

# Customize admin site
admin.site.site_header = 'REdI Trolley Audit Administration'
admin.site.site_title = 'REdI Admin'
admin.site.index_title = 'RBWH Resuscitation Trolley Audit System'
