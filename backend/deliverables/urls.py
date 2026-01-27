"""URL configuration for deliverables app."""
from django.urls import include, re_path
from rest_framework.routers import DefaultRouter

from .views import DeliverableViewSet

router = DefaultRouter()
router.register('', DeliverableViewSet, basename='deliverable')

urlpatterns = [
    re_path(r'^', include(router.urls)),
]
