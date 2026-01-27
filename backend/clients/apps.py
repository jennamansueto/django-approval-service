"""App configuration for clients."""
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ClientsConfig(AppConfig):
    """Configuration for the clients app."""
    
    name = 'clients'
    verbose_name = _(u'Clients')
