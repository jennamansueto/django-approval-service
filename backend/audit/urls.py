"""URL configuration for audit app."""
from django.urls import include, re_path
from rest_framework.routers import DefaultRouter

from .views import AuditEventViewSet

router = DefaultRouter()
router.register('', AuditEventViewSet, basename='audit')

urlpatterns = [
    re_path(r'^', include(router.urls)),
]
