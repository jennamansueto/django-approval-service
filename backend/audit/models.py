"""Audit event model."""
from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models


class AuditEvent(models.Model):
    """Append-only audit log for tracking actions."""

    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='audit_events',
    )
    verb = models.CharField(max_length=50)
    object_type = models.CharField(max_length=50)
    object_id = models.CharField(max_length=50)
    payload = JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'audit_events'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.actor} {self.verb} {self.object_type}:{self.object_id}"
