"""Views for deliverables app."""
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from accounts.permissions import IsAdminOrPlanner
from approvals.models import ApprovalRequest, ApprovalStep
from audit.models import AuditEvent

from .models import Deliverable
from .serializers import DeliverableCreateSerializer, DeliverableSerializer


class DeliverableViewSet(viewsets.ModelViewSet):
    """ViewSet for Deliverable model."""

    queryset = Deliverable.objects.select_related('client', 'created_by').all()
    permission_classes = [IsAdminOrPlanner]

    def get_serializer_class(self):
        if self.action == 'create':
            return DeliverableCreateSerializer
        return DeliverableSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        """Submit a deliverable for approval."""
        deliverable = self.get_object()

        if deliverable.status != Deliverable.Status.DRAFT:
            return Response(
                {'error': 'Only draft deliverables can be submitted'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        deliverable.status = Deliverable.Status.SUBMITTED
        deliverable.save()

        approval_request = ApprovalRequest.objects.create(
            deliverable=deliverable,
            requested_by=request.user,
        )

        ApprovalStep.objects.create(
            approval_request=approval_request,
            step_order=1,
            assigned_role=ApprovalStep.AssignedRole.APPROVER,
        )

        AuditEvent.objects.create(
            actor=request.user,
            verb='submitted',
            object_type='Deliverable',
            object_id=str(deliverable.id),
            payload={'title': deliverable.title},
        )

        return Response(DeliverableSerializer(deliverable).data)
