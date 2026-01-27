"""App configuration for audit."""
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class AuditConfig(AppConfig):
    """Configuration for the audit app."""
    
    name = 'audit'
    verbose_name = _(u'Audit')
