"""Serializers for clients app."""
from django.utils.encoding import force_str, smart_str
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from .models import Client


class ClientSerializer(serializers.ModelSerializer):
    """Serializer for Client model."""

    is_active = serializers.BooleanField(
        required=False,
        allow_null=True,
        label=_('Active Status'),
        help_text=_('Whether the client is currently active'),
    )
    is_priority = serializers.BooleanField(
        required=False,
        allow_null=True,
        label=_('Priority Status'),
        help_text=_('Whether the client has priority status'),
    )
    display_name = serializers.SerializerMethodField()
    status_display = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = [
            'id', 'name', 'code', 'is_active', 'is_priority',
            'contact_email', 'notes', 'display_name', 'status_display',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'display_name', 'status_display', 'created_at', 'updated_at']

    def get_display_name(self, obj):
        """Get formatted display name with code."""
        name = force_str(obj.name)
        if obj.code:
            code = force_str(obj.code)
            return smart_str(_('%(name)s (%(code)s)') % {'name': name, 'code': code})
        return smart_str(name)

    def get_status_display(self, obj):
        """Get human-readable status."""
        if obj.is_active:
            return smart_str(_('Active'))
        return smart_str(_('Inactive'))
