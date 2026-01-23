"""URL configuration for audit app."""
from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from .views import AuditEventViewSet

router = DefaultRouter()
router.register('', AuditEventViewSet, basename='audit')

urlpatterns = [
    url(r'^', include(router.urls)),
]
