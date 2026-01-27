"""URL configuration for clients app."""
from django.urls import include, re_path
from rest_framework.routers import DefaultRouter

from .views import ClientViewSet

router = DefaultRouter()
router.register('', ClientViewSet, basename='client')

urlpatterns = [
    re_path(r'^', include(router.urls)),
]
