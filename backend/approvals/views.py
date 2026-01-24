"""Views for approvals app."""
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from accounts.permissions import IsAdminOrApprover, IsViewerOrAbove
from audit.models import AuditEvent
from deliverables.models import Deliverable

from .models import ApprovalRequest, ApprovalStep
from .serializers import ApprovalRequestSerializer


class ApprovalRequestViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for ApprovalRequest model."""

    queryset = ApprovalRequest.objects.select_related(
        'deliverable', 'requested_by'
    ).prefetch_related('steps').all()
    serializer_class = ApprovalRequestSerializer
    permission_classes = [IsViewerOrAbove]

    def get_queryset(self):
        queryset = super().get_queryset()
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        return queryset

    @action(detail=True, methods=['post'], permission_classes=[IsAdminOrApprover])
    def approve(self, request, pk=None):
        """Approve an approval request."""
        approval_request = self.get_object()

        if approval_request.status != ApprovalRequest.PENDING:
            return Response(
                {'error': 'Only pending requests can be approved'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        approval_request.status = ApprovalRequest.APPROVED
        approval_request.decided_at = timezone.now()
        approval_request.save()

        pending_step = approval_request.steps.filter(
            status=ApprovalStep.STEP_PENDING
        ).first()
        if pending_step:
            pending_step.status = ApprovalStep.STEP_APPROVED
            pending_step.decided_by = request.user
            pending_step.decided_at = timezone.now()
            pending_step.save()

        deliverable = approval_request.deliverable
        deliverable.status = Deliverable.APPROVED
        deliverable.save()

        AuditEvent.objects.create(
            actor=request.user,
            verb='approved',
            object_type='ApprovalRequest',
            object_id=str(approval_request.id),
            payload={'deliverable_title': deliverable.title},
        )

        return Response(ApprovalRequestSerializer(approval_request).data)

    @action(detail=True, methods=['post'], permission_classes=[IsAdminOrApprover])
    def reject(self, request, pk=None):
        """Reject an approval request."""
        approval_request = self.get_object()

        if approval_request.status != ApprovalRequest.PENDING:
            return Response(
                {'error': 'Only pending requests can be rejected'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        approval_request.status = ApprovalRequest.REJECTED
        approval_request.decided_at = timezone.now()
        approval_request.save()

        pending_step = approval_request.steps.filter(
            status=ApprovalStep.STEP_PENDING
        ).first()
        if pending_step:
            pending_step.status = ApprovalStep.STEP_REJECTED
            pending_step.decided_by = request.user
            pending_step.decided_at = timezone.now()
            pending_step.save()

        deliverable = approval_request.deliverable
        deliverable.status = Deliverable.REJECTED
        deliverable.save()

        AuditEvent.objects.create(
            actor=request.user,
            verb='rejected',
            object_type='ApprovalRequest',
            object_id=str(approval_request.id),
            payload={'deliverable_title': deliverable.title},
        )

        return Response(ApprovalRequestSerializer(approval_request).data)
