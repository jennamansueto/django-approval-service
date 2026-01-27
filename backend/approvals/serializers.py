"""Serializers for approvals app."""
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from .models import ApprovalRequest, ApprovalStep


class ApprovalStepSerializer(serializers.ModelSerializer):
    """Serializer for ApprovalStep model."""

    decided_by_username = serializers.CharField(source='decided_by.username', read_only=True)
    status_display = serializers.SerializerMethodField()
    role_display = serializers.SerializerMethodField()
    is_optional = serializers.BooleanField(
        required=False,
        allow_null=True,
        label=_(u'Optional'),
        help_text=_(u'Whether this step can be skipped'),
    )

    class Meta:
        model = ApprovalStep
        fields = [
            'id', 'step_order', 'assigned_role', 'role_display',
            'status', 'status_display', 'step_notes', 'is_optional',
            'decided_by', 'decided_by_username', 'decided_at',
        ]
        read_only_fields = ['id', 'status_display', 'role_display', 'decided_by', 'decided_at']

    def get_status_display(self, obj):
        """Get human-readable status."""
        return str(obj.get_status_display())

    def get_role_display(self, obj):
        """Get human-readable role."""
        return str(obj.get_assigned_role_display())


class ApprovalRequestSerializer(serializers.ModelSerializer):
    """Serializer for ApprovalRequest model."""

    requested_by_username = serializers.CharField(source='requested_by.username', read_only=True)
    deliverable_title = serializers.CharField(source='deliverable.title', read_only=True)
    steps = ApprovalStepSerializer(many=True, read_only=True)
    status_display = serializers.SerializerMethodField()
    is_expedited = serializers.BooleanField(
        required=False,
        allow_null=True,
        label=_(u'Expedited'),
        help_text=_(u'Whether this request should be expedited'),
    )

    class Meta:
        model = ApprovalRequest
        fields = [
            'id', 'deliverable', 'deliverable_title', 'requested_by',
            'requested_by_username', 'status', 'status_display',
            'comments', 'is_expedited', 'request_metadata',
            'created_at', 'decided_at', 'steps',
        ]
        read_only_fields = [
            'id', 'requested_by', 'status', 'status_display',
            'created_at', 'decided_at',
        ]

    def get_status_display(self, obj):
        """Get human-readable status."""
        return str(obj.get_status_display())
