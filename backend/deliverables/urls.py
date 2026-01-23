"""URL configuration for deliverables app."""
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import DeliverableViewSet

router = DefaultRouter()
router.register('', DeliverableViewSet, basename='deliverable')

urlpatterns = [
    path('', include(router.urls)),
]
