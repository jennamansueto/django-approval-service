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
        verbose_name=_('actor'),
    )
    verb = models.CharField(
        _('verb'),
        max_length=50,
        help_text=_('The action that was performed'),
    )
    object_type = models.CharField(
        _('object type'),
        max_length=50,
        help_text=_('Type of object the action was performed on'),
    )
    object_id = models.CharField(
        _('object ID'),
        max_length=50,
        help_text=_('ID of the object the action was performed on'),
    )
    payload = models.JSONField(
        _('payload'),
        default=dict,
        blank=True,
        help_text=_('Additional data about the event'),
    )
    ip_address = models.GenericIPAddressField(
        _('IP address'),
        null=True,
        blank=True,
        help_text=_('IP address of the request'),
    )
    user_agent = models.TextField(
        _('user agent'),
        blank=True,
        help_text=_('Browser user agent string'),
    )
    is_system_event = models.BooleanField(
        _('system event'),
        null=True,
        blank=True,
        default=False,
        help_text=_('Whether this event was triggered by the system'),
    )
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)

    class Meta:
        db_table = 'audit_events'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.actor} {self.verb} {self.object_type}:{self.object_id}"
