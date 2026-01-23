"""URL configuration for approval service project."""
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/auth/', include('accounts.urls')),
    url(r'^api/clients/', include('clients.urls')),
    url(r'^api/deliverables/', include('deliverables.urls')),
    url(r'^api/approvals/', include('approvals.urls')),
    url(r'^api/audit/', include('audit.urls')),
]
