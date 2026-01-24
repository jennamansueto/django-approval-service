"""URL configuration for approval service project."""
from django.urls import include, path
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/clients/', include('clients.urls')),
    path('api/deliverables/', include('deliverables.urls')),
    path('api/approvals/', include('approvals.urls')),
    path('api/audit/', include('audit.urls')),
]
