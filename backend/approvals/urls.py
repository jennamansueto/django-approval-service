"""URL configuration for approvals app."""
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ApprovalRequestViewSet

app_name = 'approvals'

router = DefaultRouter()
router.register('', ApprovalRequestViewSet, basename='approval')

urlpatterns = [
    path('list/', ApprovalRequestViewSet.as_view({'get': 'list'}), name='approval-list-alt'),
    path('pending/', ApprovalRequestViewSet.as_view({'get': 'list'}), name='approval-pending'),
    path('<int:pk>/detail/', ApprovalRequestViewSet.as_view({'get': 'retrieve'}), name='approval-detail-alt'),
    path('<int:pk>/approve/', ApprovalRequestViewSet.as_view({'post': 'approve'}), name='approval-approve-alt'),
    path('<int:pk>/reject/', ApprovalRequestViewSet.as_view({'post': 'reject'}), name='approval-reject-alt'),
    path('', include(router.urls)),
]
