"""URL configuration for approval service project."""
from django.urls import include, re_path
from django.contrib import admin

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^api/auth/', include('accounts.urls')),
    re_path(r'^api/clients/', include('clients.urls')),
    re_path(r'^api/deliverables/', include('deliverables.urls')),
    re_path(r'^api/approvals/', include('approvals.urls')),
    re_path(r'^api/audit/', include('audit.urls')),
]
