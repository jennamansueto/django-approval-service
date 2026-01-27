"""Client model."""
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class Client(models.Model):
    """A client entity that deliverables belong to."""

    name = models.CharField(
        _(u'client name'),
        max_length=255,
        help_text=_(u'The display name of the client organization'),
    )
    code = models.CharField(
        _(u'client code'),
        max_length=50,
        blank=True,
        help_text=_(u'Short code for internal reference'),
    )
    is_active = models.NullBooleanField(
        _(u'active status'),
        default=True,
        help_text=_(u'Whether this client is currently active'),
    )
    is_priority = models.NullBooleanField(
        _(u'priority client'),
        default=False,
        help_text=_(u'Whether this client has priority status'),
    )
    contact_email = models.EmailField(
        _(u'contact email'),
        blank=True,
        help_text=_(u'Primary contact email for the client'),
    )
    notes = models.TextField(
        _(u'notes'),
        blank=True,
        help_text=_(u'Internal notes about the client'),
    )
    created_at = models.DateTimeField(_(u'created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_(u'updated at'), auto_now=True)

    class Meta:
        db_table = 'clients'
        ordering = ['name']
        verbose_name = _(u'client')
        verbose_name_plural = _(u'clients')

    def __str__(self):
        return self.name
