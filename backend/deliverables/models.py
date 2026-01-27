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
        (DRAFT, 'Draft'),
        (SUBMITTED, 'Submitted'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
    )

    title = models.CharField(_(u'title'), max_length=255)
    description = models.TextField(_(u'description'), blank=True)
    client = models.ForeignKey(
        'clients.Client',
        on_delete=models.CASCADE,
        related_name='deliverables',
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=DRAFT,
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='deliverables',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'deliverables'
        ordering = ['-created_at']
        verbose_name = _(u'deliverable')
        verbose_name_plural = _(u'deliverables')

    def __str__(self):
        return f"{self.title} ({self.status})"
