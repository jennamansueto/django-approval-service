"""URL configuration for clients app."""
from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from .views import ClientViewSet

app_name = 'clients'

router = DefaultRouter()
router.register('', ClientViewSet, basename='client')

urlpatterns = [
    url(r'^list/$', ClientViewSet.as_view({'get': 'list'}), name='client-list-alt'),
    url(r'^active/$', ClientViewSet.as_view({'get': 'list'}), name='client-active'),
    url(r'^(?P<pk>[0-9]+)/detail/$', ClientViewSet.as_view({'get': 'retrieve'}), name='client-detail-alt'),
    url(r'^(?P<pk>[0-9]+)/toggle/$', ClientViewSet.as_view({'post': 'toggle_active'}), name='client-toggle'),
    url(r'^', include(router.urls)),
]
