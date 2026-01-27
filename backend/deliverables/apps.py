"""App configuration for deliverables."""
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DeliverablesConfig(AppConfig):
    """Configuration for the deliverables app."""
    
    name = 'deliverables'
    verbose_name = _(u'Deliverables')
