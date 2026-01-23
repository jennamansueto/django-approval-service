"""Serializers for approvals app."""
from rest_framework import serializers

from .models import ApprovalRequest, ApprovalStep


class ApprovalStepSerializer(serializers.ModelSerializer):
    """Serializer for ApprovalStep model."""

    decided_by_username = serializers.CharField(source='decided_by.username', read_only=True)

    class Meta:
        model = ApprovalStep
        fields = [
            'id', 'step_order', 'assigned_role', 'status',
            'decided_by', 'decided_by_username', 'decided_at'
        ]
        read_only_fields = ['id', 'decided_by', 'decided_at']


class ApprovalRequestSerializer(serializers.ModelSerializer):
    """Serializer for ApprovalRequest model."""

    requested_by_username = serializers.CharField(source='requested_by.username', read_only=True)
    deliverable_title = serializers.CharField(source='deliverable.title', read_only=True)
    steps = ApprovalStepSerializer(many=True, read_only=True)

    class Meta:
        model = ApprovalRequest
        fields = [
            'id', 'deliverable', 'deliverable_title', 'requested_by',
            'requested_by_username', 'status', 'created_at', 'decided_at', 'steps'
        ]
        read_only_fields = ['id', 'requested_by', 'status', 'created_at', 'decided_at']
