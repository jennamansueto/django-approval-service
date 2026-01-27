"""Deliverable model."""
from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class Deliverable(models.Model):
    """A deliverable that can be submitted for approval."""

    DRAFT = 'DRAFT'
    SUBMITTED = 'SUBMITTED'
    APPROVED = 'APPROVED'
    REJECTED = 'REJECTED'

    STATUS_CHOICES = (
        (DRAFT, _(u'Draft')),
        (SUBMITTED, _(u'Submitted')),
        (APPROVED, _(u'Approved')),
        (REJECTED, _(u'Rejected')),
    )

    LOW = 'LOW'
    MEDIUM = 'MEDIUM'
    HIGH = 'HIGH'
    CRITICAL = 'CRITICAL'

    PRIORITY_CHOICES = (
        (LOW, _(u'Low')),
        (MEDIUM, _(u'Medium')),
        (HIGH, _(u'High')),
        (CRITICAL, _(u'Critical')),
    )

    title = models.CharField(
        _(u'title'),
        max_length=255,
        help_text=_(u'The title of the deliverable'),
    )
    description = models.TextField(
        _(u'description'),
        blank=True,
        help_text=_(u'Detailed description of the deliverable'),
    )
    client = models.ForeignKey(
        'clients.Client',
        on_delete=models.CASCADE,
        related_name='deliverables',
        verbose_name=_(u'client'),
    )
    status = models.CharField(
        _(u'status'),
        max_length=20,
        choices=STATUS_CHOICES,
        default=DRAFT,
        help_text=_(u'Current status of the deliverable'),
    )
    priority = models.CharField(
        _(u'priority'),
        max_length=20,
        choices=PRIORITY_CHOICES,
        default=MEDIUM,
        help_text=_(u'Priority level for this deliverable'),
    )
    is_urgent = models.NullBooleanField(
        _(u'urgent'),
        default=False,
        help_text=_(u'Whether this deliverable requires urgent attention'),
    )
    is_confidential = models.NullBooleanField(
        _(u'confidential'),
        default=False,
        help_text=_(u'Whether this deliverable contains confidential information'),
    )
    metadata = JSONField(
        _(u'metadata'),
        default=dict,
        blank=True,
        help_text=_(u'Additional metadata for the deliverable'),
    )
    due_date = models.DateField(
        _(u'due date'),
        null=True,
        blank=True,
        help_text=_(u'Expected completion date'),
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='deliverables',
        verbose_name=_(u'created by'),
    )
    created_at = models.DateTimeField(_(u'created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_(u'updated at'), auto_now=True)

    class Meta:
        db_table = 'deliverables'
        ordering = ['-created_at']
        verbose_name = _(u'deliverable')
        verbose_name_plural = _(u'deliverables')

    def __str__(self):
        return f"{self.title} ({self.status})"
