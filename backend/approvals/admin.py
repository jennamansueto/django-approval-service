"""Admin configuration for approvals app."""
from django.contrib import admin

from .models import ApprovalRequest, ApprovalStep


class ApprovalStepInline(admin.TabularInline):
    """Inline for ApprovalStep."""

    model = ApprovalStep
    extra = 0


@admin.register(ApprovalRequest)
class ApprovalRequestAdmin(admin.ModelAdmin):
    """Admin for ApprovalRequest model."""

    list_display = ['id', 'deliverable', 'requested_by', 'status', 'created_at']
    list_filter = ['status']
    inlines = [ApprovalStepInline]
