"""URL configuration for approvals app."""
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ApprovalRequestViewSet

router = DefaultRouter()
router.register('', ApprovalRequestViewSet, basename='approval')

urlpatterns = [
    path('', include(router.urls)),
]
