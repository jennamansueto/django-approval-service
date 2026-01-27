"""App configuration for approvals."""
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ApprovalsConfig(AppConfig):
    """Configuration for the approvals app."""
    
    name = 'approvals'
    verbose_name = _('Approvals')
