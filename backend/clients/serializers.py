"""Serializers for clients app."""
from django.utils.encoding import force_text, smart_text
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from .models import Client


class ClientSerializer(serializers.ModelSerializer):
    """Serializer for Client model."""

    is_active = serializers.NullBooleanField(
        required=False,
        label=_(u'Active Status'),
        help_text=_(u'Whether the client is currently active'),
    )
    is_priority = serializers.NullBooleanField(
        required=False,
        label=_(u'Priority Status'),
        help_text=_(u'Whether the client has priority status'),
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
        name = force_text(obj.name)
        if obj.code:
            code = force_text(obj.code)
            return smart_text(_(u'%(name)s (%(code)s)') % {'name': name, 'code': code})
        return smart_text(name)

    def get_status_display(self, obj):
        """Get human-readable status."""
        if obj.is_active:
            return smart_text(_(u'Active'))
        return smart_text(_(u'Inactive'))
