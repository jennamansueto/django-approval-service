"""Client model."""
from django.db import models
from django.utils.translation import gettext_lazy as _


class Client(models.Model):
    """A client entity that deliverables belong to."""

    name = models.CharField(_('client name'), max_length=255)
    is_active = models.BooleanField(_('active status'), null=True, blank=True, default=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        db_table = 'clients'
        ordering = ['name']
        verbose_name = _('client')
        verbose_name_plural = _('clients')

    def __str__(self):
        return self.name
