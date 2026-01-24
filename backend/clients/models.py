"""Client model."""
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Client(models.Model):
    """A client entity that deliverables belong to."""

    name = models.CharField(_(u'client name'), max_length=255)
    is_active = models.NullBooleanField(_(u'active status'), default=True)
    created_at = models.DateTimeField(_(u'created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_(u'updated at'), auto_now=True)

    class Meta:
        db_table = 'clients'
        ordering = ['name']
        verbose_name = _(u'client')
        verbose_name_plural = _(u'clients')

    def __str__(self):
        return self.name
