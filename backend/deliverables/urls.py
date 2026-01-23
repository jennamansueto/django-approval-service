"""URL configuration for deliverables app."""
from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from .views import DeliverableViewSet

router = DefaultRouter()
router.register('', DeliverableViewSet, basename='deliverable')

urlpatterns = [
    url(r'^', include(router.urls)),
]
