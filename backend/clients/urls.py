"""URL configuration for clients app."""
from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from .views import ClientViewSet

router = DefaultRouter()
router.register('', ClientViewSet, basename='client')

urlpatterns = [
    url(r'^', include(router.urls)),
]
