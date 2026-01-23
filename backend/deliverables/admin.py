"""Admin configuration for deliverables app."""
from django.contrib import admin

from .models import Deliverable


@admin.register(Deliverable)
class DeliverableAdmin(admin.ModelAdmin):
    """Admin for Deliverable model."""

    list_display = ['id', 'title', 'client', 'status', 'created_by', 'created_at']
    list_filter = ['status', 'client']
    search_fields = ['title']
