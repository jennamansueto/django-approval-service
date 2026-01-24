"""Approval models."""
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class ApprovalRequest(models.Model):
    """A request for approval of a deliverable."""

    PENDING = 'PENDING'
    APPROVED = 'APPROVED'
    REJECTED = 'REJECTED'
    CANCELED = 'CANCELED'

    STATUS_CHOICES = (
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
        (CANCELED, 'Canceled'),
    )

    deliverable = models.ForeignKey(
        'deliverables.Deliverable',
        on_delete=models.CASCADE,
        related_name='approval_requests',
    )
    requested_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='approval_requests',
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=PENDING,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    decided_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'approval_requests'
        ordering = ['-created_at']
        verbose_name = _(u'approval request')
        verbose_name_plural = _(u'approval requests')

    def __str__(self):
        return f"Approval for {self.deliverable.title} ({self.status})"


class ApprovalStep(models.Model):
    """An individual step in an approval workflow."""

    STEP_PENDING = 'PENDING'
    STEP_APPROVED = 'APPROVED'
    STEP_REJECTED = 'REJECTED'
    STEP_SKIPPED = 'SKIPPED'

    STEP_STATUS_CHOICES = (
        (STEP_PENDING, 'Pending'),
        (STEP_APPROVED, 'Approved'),
        (STEP_REJECTED, 'Rejected'),
        (STEP_SKIPPED, 'Skipped'),
    )

    ROLE_APPROVER = 'APPROVER'
    ROLE_FINANCE = 'FINANCE'
    ROLE_LEGAL = 'LEGAL'

    ROLE_CHOICES = (
        (ROLE_APPROVER, 'Approver'),
        (ROLE_FINANCE, 'Finance'),
        (ROLE_LEGAL, 'Legal'),
    )

    approval_request = models.ForeignKey(
        ApprovalRequest,
        on_delete=models.CASCADE,
        related_name='steps',
    )
    step_order = models.PositiveIntegerField(default=1)
    assigned_role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=ROLE_APPROVER,
    )
    status = models.CharField(
        max_length=20,
        choices=STEP_STATUS_CHOICES,
        default=STEP_PENDING,
    )
    decided_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='approval_decisions',
    )
    decided_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'approval_steps'
        ordering = ['approval_request', 'step_order']
        verbose_name = _(u'approval step')
        verbose_name_plural = _(u'approval steps')

    def __str__(self):
        return f"Step {self.step_order} ({self.assigned_role}) - {self.status}"
