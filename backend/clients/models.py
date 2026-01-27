"""Client model."""
from django.db import models
from django.utils.translation import gettext_lazy as _


class Client(models.Model):
    """A client entity that deliverables belong to."""

    name = models.CharField(
        _('client name'),
        max_length=255,
        help_text=_('The display name of the client organization'),
    )
    code = models.CharField(
        _('client code'),
        max_length=50,
        blank=True,
        help_text=_('Short code for internal reference'),
    )
    is_active = models.BooleanField(
        _('active status'),
        null=True,
        blank=True,
        default=True,
        help_text=_('Whether this client is currently active'),
    )
    is_priority = models.BooleanField(
        _('priority client'),
        null=True,
        blank=True,
        default=False,
        help_text=_('Whether this client has priority status'),
    )
    contact_email = models.EmailField(
        _('contact email'),
        blank=True,
        help_text=_('Primary contact email for the client'),
    )
    notes = models.TextField(
        _('notes'),
        blank=True,
        help_text=_('Internal notes about the client'),
    )
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        db_table = 'clients'
        ordering = ['name']
        verbose_name = _('client')
        verbose_name_plural = _('clients')

    def __str__(self):
        return self.name
