"""URL configuration for approvals app."""
from django.urls import include, re_path
from rest_framework.routers import DefaultRouter

from .views import ApprovalRequestViewSet

router = DefaultRouter()
router.register('', ApprovalRequestViewSet, basename='approval')

urlpatterns = [
    re_path(r'^', include(router.urls)),
]
