"""Serializers for audit app."""
from django.utils.encoding import force_str, smart_str
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from .models import AuditEvent


class AuditEventSerializer(serializers.ModelSerializer):
    """Serializer for AuditEvent model."""

    actor_username = serializers.CharField(source='actor.username', read_only=True)
    actor_display = serializers.SerializerMethodField()
    event_description = serializers.SerializerMethodField()

    class Meta:
        model = AuditEvent
        fields = [
            'id', 'actor', 'actor_username', 'actor_display',
            'verb', 'object_type', 'object_id', 'payload',
            'ip_address', 'user_agent', 'is_system_event',
            'event_description', 'created_at',
        ]
        read_only_fields = fields

    def get_actor_display(self, obj):
        """Get formatted actor display name."""
        if obj.actor:
            if obj.actor.first_name and obj.actor.last_name:
                return smart_str(force_str(obj.actor.get_full_name()))
            return force_str(obj.actor.username)
        return smart_str(_('System'))

    def get_event_description(self, obj):
        """Get human-readable event description."""
        actor = self.get_actor_display(obj)
        verb = force_str(obj.verb)
        object_type = force_str(obj.object_type)
        object_id = force_str(obj.object_id)
        
        description = _('%(actor)s %(verb)s %(object_type)s #%(object_id)s') % {
            'actor': actor,
            'verb': verb,
            'object_type': object_type,
            'object_id': object_id,
        }
        return smart_str(description)
