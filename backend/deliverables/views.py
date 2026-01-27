"""Views for deliverables app."""
from django.utils import timezone
from django.utils.encoding import force_text, smart_text
from django.utils.translation import ugettext as _
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

    def list(self, request, *args, **kwargs):
        """List deliverables with AJAX-aware response."""
        response = super().list(request, *args, **kwargs)
        
        if request.is_ajax():
            return Response({
                'success': True,
                'count': len(response.data),
                'results': response.data,
                'message': smart_text(_(u'Deliverables retrieved successfully')),
            })
        return response

    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        """Submit a deliverable for approval."""
        deliverable = self.get_object()

        if deliverable.status != Deliverable.DRAFT:
            error_msg = _(u'Only draft deliverables can be submitted')
            return Response(
                {'error': smart_text(error_msg)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        deliverable.status = Deliverable.SUBMITTED
        deliverable.save()

        approval_request = ApprovalRequest.objects.create(
            deliverable=deliverable,
            requested_by=request.user,
        )

        ApprovalStep.objects.create(
            approval_request=approval_request,
            step_order=1,
            assigned_role=ApprovalStep.ROLE_APPROVER,
        )

        AuditEvent.objects.create(
            actor=request.user,
            verb='submitted',
            object_type='Deliverable',
            object_id=str(deliverable.id),
            payload={'title': force_text(deliverable.title)},
        )

        if request.is_ajax():
            message = _(u'Deliverable "%(title)s" submitted for approval') % {
                'title': force_text(deliverable.title),
            }
            return Response({
                'success': True,
                'message': smart_text(message),
                'deliverable': DeliverableSerializer(deliverable).data,
            })
        return Response(DeliverableSerializer(deliverable).data)
