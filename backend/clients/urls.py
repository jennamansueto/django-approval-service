"""URL configuration for clients app."""
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ClientViewSet

app_name = 'clients'

router = DefaultRouter()
router.register('', ClientViewSet, basename='client')

urlpatterns = [
    path('list/', ClientViewSet.as_view({'get': 'list'}), name='client-list-alt'),
    path('active/', ClientViewSet.as_view({'get': 'list'}), name='client-active'),
    path('<int:pk>/detail/', ClientViewSet.as_view({'get': 'retrieve'}), name='client-detail-alt'),
    path('<int:pk>/toggle/', ClientViewSet.as_view({'post': 'toggle_active'}), name='client-toggle'),
    path('', include(router.urls)),
]
