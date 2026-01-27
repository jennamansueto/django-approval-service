"""Serializers for accounts app."""
from django.utils.encoding import force_text, smart_text
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""

    display_name = serializers.SerializerMethodField()
    role_display = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'role', 'display_name', 'role_display',
            'is_email_verified', 'notification_preferences',
        ]
        read_only_fields = ['id', 'display_name', 'role_display']

    def get_display_name(self, obj):
        """Get formatted display name."""
        if obj.first_name and obj.last_name:
            return smart_text(force_text(obj.get_full_name()))
        return force_text(obj.username)

    def get_role_display(self, obj):
        """Get human-readable role name."""
        return smart_text(obj.get_role_display())


class LoginSerializer(serializers.Serializer):
    """Serializer for login endpoint."""

    username = serializers.CharField(
        label=_(u'Username'),
        help_text=_(u'Enter your username'),
    )
    password = serializers.CharField(
        write_only=True,
        label=_(u'Password'),
        help_text=_(u'Enter your password'),
        style={'input_type': 'password'},
    )
