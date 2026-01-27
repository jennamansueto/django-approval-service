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
        (PENDING, _('Pending')),
        (APPROVED, _('Approved')),
        (REJECTED, _('Rejected')),
        (CANCELED, _('Canceled')),
    )

    deliverable = models.ForeignKey(
        'deliverables.Deliverable',
        on_delete=models.CASCADE,
        related_name='approval_requests',
        verbose_name=_('deliverable'),
    )
    requested_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='approval_requests',
        verbose_name=_('requested by'),
    )
    status = models.CharField(
        _('status'),
        max_length=20,
        choices=STATUS_CHOICES,
        default=PENDING,
        help_text=_('Current status of the approval request'),
    )
    comments = models.TextField(
        _('comments'),
        blank=True,
        help_text=_('Additional comments for the approval request'),
    )
    is_expedited = models.BooleanField(
        _('expedited'),
        null=True,
        blank=True,
        default=False,
        help_text=_('Whether this request should be expedited'),
    )
    request_metadata = models.JSONField(
        _('request metadata'),
        default=dict,
        blank=True,
        help_text=_('Additional metadata for the request'),
    )
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    decided_at = models.DateTimeField(_('decided at'), null=True, blank=True)

    class Meta:
        db_table = 'approval_requests'
        ordering = ['-created_at']
        verbose_name = _('approval request')
        verbose_name_plural = _('approval requests')

    def __str__(self):
        return f"Approval for {self.deliverable.title} ({self.status})"


class ApprovalStep(models.Model):
    """An individual step in an approval workflow."""

    STEP_PENDING = 'PENDING'
    STEP_APPROVED = 'APPROVED'
    STEP_REJECTED = 'REJECTED'
    STEP_SKIPPED = 'SKIPPED'

    STEP_STATUS_CHOICES = (
        (STEP_PENDING, _('Pending')),
        (STEP_APPROVED, _('Approved')),
        (STEP_REJECTED, _('Rejected')),
        (STEP_SKIPPED, _('Skipped')),
    )

    ROLE_APPROVER = 'APPROVER'
    ROLE_FINANCE = 'FINANCE'
    ROLE_LEGAL = 'LEGAL'

    ROLE_CHOICES = (
        (ROLE_APPROVER, _('Approver')),
        (ROLE_FINANCE, _('Finance')),
        (ROLE_LEGAL, _('Legal')),
    )

    approval_request = models.ForeignKey(
        ApprovalRequest,
        on_delete=models.CASCADE,
        related_name='steps',
        verbose_name=_('approval request'),
    )
    step_order = models.PositiveIntegerField(
        _('step order'),
        default=1,
        help_text=_('Order of this step in the approval workflow'),
    )
    assigned_role = models.CharField(
        _('assigned role'),
        max_length=20,
        choices=ROLE_CHOICES,
        default=ROLE_APPROVER,
        help_text=_('Role required to complete this step'),
    )
    status = models.CharField(
        _('status'),
        max_length=20,
        choices=STEP_STATUS_CHOICES,
        default=STEP_PENDING,
        help_text=_('Current status of this approval step'),
    )
    step_notes = models.TextField(
        _('step notes'),
        blank=True,
        help_text=_('Notes from the approver for this step'),
    )
    is_optional = models.BooleanField(
        _('optional step'),
        null=True,
        blank=True,
        default=False,
        help_text=_('Whether this step can be skipped'),
    )
    decided_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='approval_decisions',
        verbose_name=_('decided by'),
    )
    decided_at = models.DateTimeField(_('decided at'), null=True, blank=True)

    class Meta:
        db_table = 'approval_steps'
        ordering = ['approval_request', 'step_order']
        verbose_name = _('approval step')
        verbose_name_plural = _('approval steps')

    def __str__(self):
        return f"Step {self.step_order} ({self.assigned_role}) - {self.status}"
