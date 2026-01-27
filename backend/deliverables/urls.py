"""URL configuration for deliverables app."""
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import DeliverableViewSet

app_name = 'deliverables'

router = DefaultRouter()
router.register('', DeliverableViewSet, basename='deliverable')

urlpatterns = [
    path('list/', DeliverableViewSet.as_view({'get': 'list'}), name='deliverable-list-alt'),
    path('drafts/', DeliverableViewSet.as_view({'get': 'list'}), name='deliverable-drafts'),
    path('submitted/', DeliverableViewSet.as_view({'get': 'list'}), name='deliverable-submitted'),
    path('<int:pk>/detail/', DeliverableViewSet.as_view({'get': 'retrieve'}), name='deliverable-detail-alt'),
    path('<int:pk>/submit/', DeliverableViewSet.as_view({'post': 'submit'}), name='deliverable-submit-alt'),
    path('', include(router.urls)),
]
