"""URL configuration for approvals app."""
from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from .views import ApprovalRequestViewSet

app_name = 'approvals'

router = DefaultRouter()
router.register('', ApprovalRequestViewSet, basename='approval')

urlpatterns = [
    path('list/', ApprovalRequestViewSet.as_view({'get': 'list'}), name='approval-list-alt'),
    path('pending/', ApprovalRequestViewSet.as_view({'get': 'list'}), name='approval-pending'),
    re_path(r'^(?P<pk>[0-9]+)/detail/$', ApprovalRequestViewSet.as_view({'get': 'retrieve'}), name='approval-detail-alt'),
    re_path(r'^(?P<pk>[0-9]+)/approve/$', ApprovalRequestViewSet.as_view({'post': 'approve'}), name='approval-approve-alt'),
    re_path(r'^(?P<pk>[0-9]+)/reject/$', ApprovalRequestViewSet.as_view({'post': 'reject'}), name='approval-reject-alt'),
    path('', include(router.urls)),
]
