"""Audit configuration and retention policy models."""
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class AuditConfig(models.Model):
    """Configuration settings for the audit system."""

    id = models.AutoField(primary_key=True)
    
    key = models.CharField(
        _('configuration key'),
        max_length=100,
        unique=True,
        help_text=_('Unique key for this configuration setting'),
    )
    value = models.TextField(
        _('configuration value'),
        help_text=_('Value for this configuration setting'),
    )
    is_enabled = models.BooleanField(
        _('enabled'),
        null=True,
        blank=True,
        default=True,
        help_text=_('Whether this configuration is active'),
    )
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        db_table = 'audit_config'
        verbose_name = _('Audit Configuration')
        verbose_name_plural = _('Audit Configurations')

    def __str__(self):
        return f"{self.key}: {self.value[:50]}"


class AuditRetentionPolicy(models.Model):
    """Defines how long audit events should be retained."""

    id = models.AutoField(primary_key=True)
    
    name = models.CharField(
        _('policy name'),
        max_length=100,
        help_text=_('Name of this retention policy'),
    )
    retention_days = models.PositiveIntegerField(
        _('retention days'),
        default=90,
        help_text=_('Number of days to retain audit events'),
    )
    applies_to_verb = models.CharField(
        _('applies to verb'),
        max_length=50,
        blank=True,
        help_text=_('Specific verb this policy applies to, or blank for all'),
    )
    is_active = models.BooleanField(
        _('active'),
        null=True,
        blank=True,
        default=True,
        help_text=_('Whether this policy is currently active'),
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('created by'),
    )

    class Meta:
        db_table = 'audit_retention_policies'
        verbose_name = _('Audit Retention Policy')
        verbose_name_plural = _('Audit Retention Policies')

    def __str__(self):
        return f"{self.name} ({self.retention_days} days)"
