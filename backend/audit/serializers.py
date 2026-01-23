"""Serializers for audit app."""
from rest_framework import serializers

from .models import AuditEvent


class AuditEventSerializer(serializers.ModelSerializer):
    """Serializer for AuditEvent model."""

    actor_username = serializers.CharField(source='actor.username', read_only=True)

    class Meta:
        model = AuditEvent
        fields = [
            'id', 'actor', 'actor_username', 'verb',
            'object_type', 'object_id', 'payload', 'created_at'
        ]
        read_only_fields = fields
