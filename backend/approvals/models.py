"""Approval models."""
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


class ApprovalRequest(models.Model):
    """A request for approval of a deliverable."""

    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        APPROVED = 'APPROVED', 'Approved'
        REJECTED = 'REJECTED', 'Rejected'
        CANCELED = 'CANCELED', 'Canceled'

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
        choices=Status.choices,
        default=Status.PENDING,
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

    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        APPROVED = 'APPROVED', 'Approved'
        REJECTED = 'REJECTED', 'Rejected'
        SKIPPED = 'SKIPPED', 'Skipped'

    class AssignedRole(models.TextChoices):
        APPROVER = 'APPROVER', 'Approver'
        FINANCE = 'FINANCE', 'Finance'
        LEGAL = 'LEGAL', 'Legal'

    approval_request = models.ForeignKey(
        ApprovalRequest,
        on_delete=models.CASCADE,
        related_name='steps',
    )
    step_order = models.PositiveIntegerField(default=1)
    assigned_role = models.CharField(
        max_length=20,
        choices=AssignedRole.choices,
        default=AssignedRole.APPROVER,
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
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
