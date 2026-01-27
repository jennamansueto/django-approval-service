"""Serializers for deliverables app."""
from django.utils.encoding import force_text, smart_text
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from .models import Deliverable


class DeliverableSerializer(serializers.ModelSerializer):
    """Serializer for Deliverable model."""

    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    client_name = serializers.CharField(source='client.name', read_only=True)
    status_display = serializers.SerializerMethodField()
    priority_display = serializers.SerializerMethodField()
    is_urgent = serializers.NullBooleanField(
        required=False,
        label=_(u'Urgent'),
        help_text=_(u'Whether this deliverable requires urgent attention'),
    )
    is_confidential = serializers.NullBooleanField(
        required=False,
        label=_(u'Confidential'),
        help_text=_(u'Whether this deliverable contains confidential information'),
    )

    class Meta:
        model = Deliverable
        fields = [
            'id', 'title', 'description', 'client', 'client_name',
            'status', 'status_display', 'priority', 'priority_display',
            'is_urgent', 'is_confidential', 'metadata', 'due_date',
            'created_by', 'created_by_username', 'created_at', 'updated_at',
        ]
        read_only_fields = [
            'id', 'status', 'status_display', 'priority_display',
            'created_by', 'created_at', 'updated_at',
        ]

    def get_status_display(self, obj):
        """Get human-readable status."""
        return smart_text(obj.get_status_display())

    def get_priority_display(self, obj):
        """Get human-readable priority."""
        return smart_text(obj.get_priority_display())


class DeliverableCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating deliverables."""

    title = serializers.CharField(
        label=_(u'Title'),
        help_text=_(u'Enter the deliverable title'),
    )
    description = serializers.CharField(
        required=False,
        allow_blank=True,
        label=_(u'Description'),
        help_text=_(u'Enter a detailed description'),
    )

    class Meta:
        model = Deliverable
        fields = ['id', 'title', 'description', 'client', 'priority', 'is_urgent', 'is_confidential', 'due_date']
        read_only_fields = ['id']
