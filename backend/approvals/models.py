"""Approval models."""
from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class ApprovalRequest(models.Model):
    """A request for approval of a deliverable."""

    PENDING = 'PENDING'
    APPROVED = 'APPROVED'
    REJECTED = 'REJECTED'
    CANCELED = 'CANCELED'

    STATUS_CHOICES = (
        (PENDING, _(u'Pending')),
        (APPROVED, _(u'Approved')),
        (REJECTED, _(u'Rejected')),
        (CANCELED, _(u'Canceled')),
    )

    deliverable = models.ForeignKey(
        'deliverables.Deliverable',
        on_delete=models.CASCADE,
        related_name='approval_requests',
        verbose_name=_(u'deliverable'),
    )
    requested_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='approval_requests',
        verbose_name=_(u'requested by'),
    )
    status = models.CharField(
        _(u'status'),
        max_length=20,
        choices=STATUS_CHOICES,
        default=PENDING,
        help_text=_(u'Current status of the approval request'),
    )
    comments = models.TextField(
        _(u'comments'),
        blank=True,
        help_text=_(u'Additional comments for the approval request'),
    )
    is_expedited = models.NullBooleanField(
        _(u'expedited'),
        default=False,
        help_text=_(u'Whether this request should be expedited'),
    )
    request_metadata = JSONField(
        _(u'request metadata'),
        default=dict,
        blank=True,
        help_text=_(u'Additional metadata for the request'),
    )
    created_at = models.DateTimeField(_(u'created at'), auto_now_add=True)
    decided_at = models.DateTimeField(_(u'decided at'), null=True, blank=True)

    class Meta:
        db_table = 'approval_requests'
        ordering = ['-created_at']
        verbose_name = _(u'approval request')
        verbose_name_plural = _(u'approval requests')

    def __str__(self):
        return f"Approval for {self.deliverable.title} ({self.status})"


@python_2_unicode_compatible
class ApprovalStep(models.Model):
    """An individual step in an approval workflow."""

    STEP_PENDING = 'PENDING'
    STEP_APPROVED = 'APPROVED'
    STEP_REJECTED = 'REJECTED'
    STEP_SKIPPED = 'SKIPPED'

    STEP_STATUS_CHOICES = (
        (STEP_PENDING, _(u'Pending')),
        (STEP_APPROVED, _(u'Approved')),
        (STEP_REJECTED, _(u'Rejected')),
        (STEP_SKIPPED, _(u'Skipped')),
    )

    ROLE_APPROVER = 'APPROVER'
    ROLE_FINANCE = 'FINANCE'
    ROLE_LEGAL = 'LEGAL'

    ROLE_CHOICES = (
        (ROLE_APPROVER, _(u'Approver')),
        (ROLE_FINANCE, _(u'Finance')),
        (ROLE_LEGAL, _(u'Legal')),
    )

    approval_request = models.ForeignKey(
        ApprovalRequest,
        on_delete=models.CASCADE,
        related_name='steps',
        verbose_name=_(u'approval request'),
    )
    step_order = models.PositiveIntegerField(
        _(u'step order'),
        default=1,
        help_text=_(u'Order of this step in the approval workflow'),
    )
    assigned_role = models.CharField(
        _(u'assigned role'),
        max_length=20,
        choices=ROLE_CHOICES,
        default=ROLE_APPROVER,
        help_text=_(u'Role required to complete this step'),
    )
    status = models.CharField(
        _(u'status'),
        max_length=20,
        choices=STEP_STATUS_CHOICES,
        default=STEP_PENDING,
        help_text=_(u'Current status of this approval step'),
    )
    step_notes = models.TextField(
        _(u'step notes'),
        blank=True,
        help_text=_(u'Notes from the approver for this step'),
    )
    is_optional = models.NullBooleanField(
        _(u'optional step'),
        default=False,
        help_text=_(u'Whether this step can be skipped'),
    )
    decided_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='approval_decisions',
        verbose_name=_(u'decided by'),
    )
    decided_at = models.DateTimeField(_(u'decided at'), null=True, blank=True)

    class Meta:
        db_table = 'approval_steps'
        ordering = ['approval_request', 'step_order']
        verbose_name = _(u'approval step')
        verbose_name_plural = _(u'approval steps')

    def __str__(self):
        return f"Step {self.step_order} ({self.assigned_role}) - {self.status}"
