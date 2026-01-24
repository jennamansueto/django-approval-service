"""Audit configuration and retention policy models."""
from django.conf import settings
from django.db import models


class AuditConfig(models.Model):
    """Configuration settings for the audit system."""

    id = models.AutoField(primary_key=True)
    
    key = models.CharField(max_length=100, unique=True)
    value = models.TextField()
    is_enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'audit_config'
        verbose_name = 'Audit Configuration'
        verbose_name_plural = 'Audit Configurations'

    def __str__(self):
        return f"{self.key}: {self.value[:50]}"


class AuditRetentionPolicy(models.Model):
    """Defines how long audit events should be retained."""

    id = models.AutoField(primary_key=True)
    
    name = models.CharField(max_length=100)
    retention_days = models.PositiveIntegerField(default=90)
    applies_to_verb = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    class Meta:
        db_table = 'audit_retention_policies'
        verbose_name = 'Audit Retention Policy'
        verbose_name_plural = 'Audit Retention Policies'

    def __str__(self):
        return f"{self.name} ({self.retention_days} days)"
