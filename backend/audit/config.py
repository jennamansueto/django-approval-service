"""Audit configuration and retention policy models."""
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class AuditConfig(models.Model):
    """Configuration settings for the audit system."""

    id = models.AutoField(primary_key=True)
    
    key = models.CharField(
        _(u'configuration key'),
        max_length=100,
        unique=True,
        help_text=_(u'Unique key for this configuration setting'),
    )
    value = models.TextField(
        _(u'configuration value'),
        help_text=_(u'Value for this configuration setting'),
    )
    is_enabled = models.BooleanField(
        _(u'enabled'),
        null=True,
        default=True,
        help_text=_(u'Whether this configuration is active'),
    )
    created_at = models.DateTimeField(_(u'created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_(u'updated at'), auto_now=True)

    class Meta:
        db_table = 'audit_config'
        verbose_name = _(u'Audit Configuration')
        verbose_name_plural = _(u'Audit Configurations')

    def __str__(self):
        return f"{self.key}: {self.value[:50]}"


class AuditRetentionPolicy(models.Model):
    """Defines how long audit events should be retained."""

    id = models.AutoField(primary_key=True)
    
    name = models.CharField(
        _(u'policy name'),
        max_length=100,
        help_text=_(u'Name of this retention policy'),
    )
    retention_days = models.PositiveIntegerField(
        _(u'retention days'),
        default=90,
        help_text=_(u'Number of days to retain audit events'),
    )
    applies_to_verb = models.CharField(
        _(u'applies to verb'),
        max_length=50,
        blank=True,
        help_text=_(u'Specific verb this policy applies to, or blank for all'),
    )
    is_active = models.BooleanField(
        _(u'active'),
        null=True,
        default=True,
        help_text=_(u'Whether this policy is currently active'),
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_(u'created by'),
    )

    class Meta:
        db_table = 'audit_retention_policies'
        verbose_name = _(u'Audit Retention Policy')
        verbose_name_plural = _(u'Audit Retention Policies')

    def __str__(self):
        return f"{self.name} ({self.retention_days} days)"
