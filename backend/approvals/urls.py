"""URL configuration for approvals app."""
from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from .views import ApprovalRequestViewSet

router = DefaultRouter()
router.register('', ApprovalRequestViewSet, basename='approval')

urlpatterns = [
    url(r'^', include(router.urls)),
]
