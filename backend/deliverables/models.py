"""Deliverable model."""
from django.conf import settings
from django.db import models


class Deliverable(models.Model):
    """A deliverable that can be submitted for approval."""

    class Status(models.TextChoices):
        DRAFT = 'DRAFT', 'Draft'
        SUBMITTED = 'SUBMITTED', 'Submitted'
        APPROVED = 'APPROVED', 'Approved'
        REJECTED = 'REJECTED', 'Rejected'

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    client = models.ForeignKey(
        'clients.Client',
        on_delete=models.CASCADE,
        related_name='deliverables',
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
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

    def __str__(self):
        return f"{self.title} ({self.status})"
