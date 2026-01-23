"""Admin configuration for audit app."""
from django.contrib import admin

from .models import AuditEvent


@admin.register(AuditEvent)
class AuditEventAdmin(admin.ModelAdmin):
    """Admin for AuditEvent model."""

    list_display = ['id', 'actor', 'verb', 'object_type', 'object_id', 'created_at']
    list_filter = ['verb', 'object_type']
    readonly_fields = ['actor', 'verb', 'object_type', 'object_id', 'payload', 'created_at']
