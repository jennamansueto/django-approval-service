"""URL configuration for audit app."""
from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from .views import AuditEventViewSet

app_name = 'audit'

router = DefaultRouter()
router.register('', AuditEventViewSet, basename='audit')

urlpatterns = [
    url(r'^list/$', AuditEventViewSet.as_view({'get': 'list'}), name='audit-list-alt'),
    url(r'^events/$', AuditEventViewSet.as_view({'get': 'list'}), name='audit-events'),
    url(r'^(?P<pk>[0-9]+)/detail/$', AuditEventViewSet.as_view({'get': 'retrieve'}), name='audit-detail-alt'),
    url(r'^by-type/(?P<object_type>[\w-]+)/$', AuditEventViewSet.as_view({'get': 'list'}), name='audit-by-type'),
    url(r'^by-object/(?P<object_type>[\w-]+)/(?P<object_id>[0-9]+)/$', AuditEventViewSet.as_view({'get': 'list'}), name='audit-by-object'),
    url(r'^', include(router.urls)),
]
