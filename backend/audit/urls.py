"""URL configuration for audit app."""
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AuditEventViewSet

router = DefaultRouter()
router.register('', AuditEventViewSet, basename='audit')

urlpatterns = [
    path('', include(router.urls)),
]
