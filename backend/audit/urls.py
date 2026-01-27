"""URL configuration for audit app."""
from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from .views import AuditEventViewSet

app_name = 'audit'

router = DefaultRouter()
router.register('', AuditEventViewSet, basename='audit')

urlpatterns = [
    path('list/', AuditEventViewSet.as_view({'get': 'list'}), name='audit-list-alt'),
    path('events/', AuditEventViewSet.as_view({'get': 'list'}), name='audit-events'),
    re_path(r'^(?P<pk>[0-9]+)/detail/$', AuditEventViewSet.as_view({'get': 'retrieve'}), name='audit-detail-alt'),
    re_path(r'^by-type/(?P<object_type>[\w-]+)/$', AuditEventViewSet.as_view({'get': 'list'}), name='audit-by-type'),
    re_path(r'^by-object/(?P<object_type>[\w-]+)/(?P<object_id>[0-9]+)/$', AuditEventViewSet.as_view({'get': 'list'}), name='audit-by-object'),
    path('', include(router.urls)),
]
