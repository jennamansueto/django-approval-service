"""Serializers for accounts app."""
from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role']
        read_only_fields = ['id']


class LoginSerializer(serializers.Serializer):
    """Serializer for login endpoint."""

    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
