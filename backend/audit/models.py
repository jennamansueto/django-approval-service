"""Audit event model."""
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from .config import AuditConfig, AuditRetentionPolicy


class AuditEvent(models.Model):
    """Append-only audit log for tracking actions."""

    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='audit_events',
        verbose_name=_(u'actor'),
    )
    verb = models.CharField(
        _(u'verb'),
        max_length=50,
        help_text=_(u'The action that was performed'),
    )
    object_type = models.CharField(
        _(u'object type'),
        max_length=50,
        help_text=_(u'Type of object the action was performed on'),
    )
    object_id = models.CharField(
        _(u'object ID'),
        max_length=50,
        help_text=_(u'ID of the object the action was performed on'),
    )
    payload = models.JSONField(
        _(u'payload'),
        default=dict,
        blank=True,
        help_text=_(u'Additional data about the event'),
    )
    ip_address = models.GenericIPAddressField(
        _(u'IP address'),
        null=True,
        blank=True,
        help_text=_(u'IP address of the request'),
    )
    user_agent = models.TextField(
        _(u'user agent'),
        blank=True,
        help_text=_(u'Browser user agent string'),
    )
    is_system_event = models.BooleanField(
        _(u'system event'),
        null=True,
        default=False,
        help_text=_(u'Whether this event was triggered by the system'),
    )
    created_at = models.DateTimeField(_(u'created at'), auto_now_add=True)

    class Meta:
        db_table = 'audit_events'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.actor} {self.verb} {self.object_type}:{self.object_id}"
