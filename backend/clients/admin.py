"""Admin configuration for clients app."""
from django.contrib import admin

from .models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    """Admin for Client model."""

    list_display = ['id', 'name', 'created_at']
    search_fields = ['name']
