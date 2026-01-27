"""URL configuration for deliverables app."""
from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from .views import DeliverableViewSet

app_name = 'deliverables'

router = DefaultRouter()
router.register('', DeliverableViewSet, basename='deliverable')

urlpatterns = [
    url(r'^list/$', DeliverableViewSet.as_view({'get': 'list'}), name='deliverable-list-alt'),
    url(r'^drafts/$', DeliverableViewSet.as_view({'get': 'list'}), name='deliverable-drafts'),
    url(r'^submitted/$', DeliverableViewSet.as_view({'get': 'list'}), name='deliverable-submitted'),
    url(r'^(?P<pk>[0-9]+)/detail/$', DeliverableViewSet.as_view({'get': 'retrieve'}), name='deliverable-detail-alt'),
    url(r'^(?P<pk>[0-9]+)/submit/$', DeliverableViewSet.as_view({'post': 'submit'}), name='deliverable-submit-alt'),
    url(r'^', include(router.urls)),
]
