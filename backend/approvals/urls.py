"""URL configuration for approvals app."""
from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from .views import ApprovalRequestViewSet

app_name = 'approvals'

router = DefaultRouter()
router.register('', ApprovalRequestViewSet, basename='approval')

urlpatterns = [
    url(r'^list/$', ApprovalRequestViewSet.as_view({'get': 'list'}), name='approval-list-alt'),
    url(r'^pending/$', ApprovalRequestViewSet.as_view({'get': 'list'}), name='approval-pending'),
    url(r'^(?P<pk>[0-9]+)/detail/$', ApprovalRequestViewSet.as_view({'get': 'retrieve'}), name='approval-detail-alt'),
    url(r'^(?P<pk>[0-9]+)/approve/$', ApprovalRequestViewSet.as_view({'post': 'approve'}), name='approval-approve-alt'),
    url(r'^(?P<pk>[0-9]+)/reject/$', ApprovalRequestViewSet.as_view({'post': 'reject'}), name='approval-reject-alt'),
    url(r'^', include(router.urls)),
]
