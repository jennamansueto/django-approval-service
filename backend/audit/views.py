"""Views for audit app."""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import AuditEvent
from .serializers import AuditEventSerializer


class AuditEventViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for AuditEvent model (read-only)."""

    queryset = AuditEvent.objects.select_related('actor').all()
    serializer_class = AuditEventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        object_type = self.request.query_params.get('object_type')
        object_id = self.request.query_params.get('object_id')
        if object_type:
            queryset = queryset.filter(object_type=object_type)
        if object_id:
            queryset = queryset.filter(object_id=object_id)
        return queryset
