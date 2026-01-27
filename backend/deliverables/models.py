"""Deliverable model."""
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Deliverable(models.Model):
    """A deliverable that can be submitted for approval."""

    DRAFT = 'DRAFT'
    SUBMITTED = 'SUBMITTED'
    APPROVED = 'APPROVED'
    REJECTED = 'REJECTED'

    STATUS_CHOICES = (
        (DRAFT, _('Draft')),
        (SUBMITTED, _('Submitted')),
        (APPROVED, _('Approved')),
        (REJECTED, _('Rejected')),
    )

    LOW = 'LOW'
    MEDIUM = 'MEDIUM'
    HIGH = 'HIGH'
    CRITICAL = 'CRITICAL'

    PRIORITY_CHOICES = (
        (LOW, _('Low')),
        (MEDIUM, _('Medium')),
        (HIGH, _('High')),
        (CRITICAL, _('Critical')),
    )

    title = models.CharField(
        _('title'),
        max_length=255,
        help_text=_('The title of the deliverable'),
    )
    description = models.TextField(
        _('description'),
        blank=True,
        help_text=_('Detailed description of the deliverable'),
    )
    client = models.ForeignKey(
        'clients.Client',
        on_delete=models.CASCADE,
        related_name='deliverables',
        verbose_name=_('client'),
    )
    status = models.CharField(
        _('status'),
        max_length=20,
        choices=STATUS_CHOICES,
        default=DRAFT,
        help_text=_('Current status of the deliverable'),
    )
    priority = models.CharField(
        _('priority'),
        max_length=20,
        choices=PRIORITY_CHOICES,
        default=MEDIUM,
        help_text=_('Priority level for this deliverable'),
    )
    is_urgent = models.BooleanField(
        _('urgent'),
        null=True,
        blank=True,
        default=False,
        help_text=_('Whether this deliverable requires urgent attention'),
    )
    is_confidential = models.BooleanField(
        _('confidential'),
        null=True,
        blank=True,
        default=False,
        help_text=_('Whether this deliverable contains confidential information'),
    )
    metadata = models.JSONField(
        _('metadata'),
        default=dict,
        blank=True,
        help_text=_('Additional metadata for the deliverable'),
    )
    due_date = models.DateField(
        _('due date'),
        null=True,
        blank=True,
        help_text=_('Expected completion date'),
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='deliverables',
        verbose_name=_('created by'),
    )
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        db_table = 'deliverables'
        ordering = ['-created_at']
        verbose_name = _('deliverable')
        verbose_name_plural = _('deliverables')

    def __str__(self):
        return f"{self.title} ({self.status})"
