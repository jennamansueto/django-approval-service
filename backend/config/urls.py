"""URL configuration for approval service project."""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('accounts.urls')),
    path('api/v1/clients/', include('clients.urls')),
    path('api/v1/deliverables/', include('deliverables.urls')),
    path('api/v1/approvals/', include('approvals.urls')),
    path('api/v1/audit/', include('audit.urls')),
    # Legacy API routes (deprecated, use v1)
    path('api/auth/', include('accounts.urls')),
    path('api/clients/', include('clients.urls')),
    path('api/deliverables/', include('deliverables.urls')),
    path('api/approvals/', include('approvals.urls')),
    path('api/audit/', include('audit.urls')),
]
