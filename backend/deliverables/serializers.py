"""Serializers for deliverables app."""
from rest_framework import serializers

from .models import Deliverable


class DeliverableSerializer(serializers.ModelSerializer):
    """Serializer for Deliverable model."""

    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    client_name = serializers.CharField(source='client.name', read_only=True)

    class Meta:
        model = Deliverable
        fields = [
            'id', 'title', 'description', 'client', 'client_name',
            'status', 'created_by', 'created_by_username', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'status', 'created_by', 'created_at', 'updated_at']


class DeliverableCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating deliverables."""

    class Meta:
        model = Deliverable
        fields = ['id', 'title', 'description', 'client']
        read_only_fields = ['id']
