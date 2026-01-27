"""Serializers for clients app."""
from rest_framework import serializers

from .models import Client


class ClientSerializer(serializers.ModelSerializer):
    """Serializer for Client model."""

    is_active = serializers.BooleanField(required=False, allow_null=True)

    class Meta:
        model = Client
        fields = ['id', 'name', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
