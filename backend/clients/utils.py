"""Utility functions for clients app."""
from urllib.parse import quote, quote_plus

from django.utils.encoding import force_str, smart_str
from django.utils.translation import gettext as _


def get_client_display_name(client):
    """Get a formatted display name for the client."""
    name = force_str(client.name)
    if client.code:
        code = force_str(client.code)
        return smart_str(_('%(name)s (%(code)s)') % {'name': name, 'code': code})
    return smart_str(name)


def get_client_url(client):
    """Generate a URL-safe path for the client."""
    name = force_str(client.name)
    return '/clients/%s/' % quote(name)


def get_client_export_filename(client):
    """Generate a safe filename for client export."""
    name = force_str(client.name)
    # Use quote_plus to handle spaces as plus signs
    safe_name = quote_plus(name)
    return 'client_%s_export.csv' % safe_name


def format_client_status(client):
    """Format client status for display."""
    if client.is_active:
        status = _('Active')
    else:
        status = _('Inactive')
    
    name = force_str(client.name)
    return smart_str(_('%(name)s - %(status)s') % {
        'name': name,
        'status': status,
    })
