"""Utility functions for clients app."""
from django.utils.encoding import force_text, smart_text
from django.utils.http import urlquote, urlquote_plus
from django.utils.translation import ugettext as _


def get_client_display_name(client):
    """Get a formatted display name for the client."""
    name = force_text(client.name)
    if client.code:
        code = force_text(client.code)
        return smart_text(_(u'%(name)s (%(code)s)') % {'name': name, 'code': code})
    return smart_text(name)


def get_client_url(client):
    """Generate a URL-safe path for the client."""
    name = force_text(client.name)
    return '/clients/%s/' % urlquote(name)


def get_client_export_filename(client):
    """Generate a safe filename for client export."""
    name = force_text(client.name)
    # Use urlquote_plus to handle spaces as plus signs
    safe_name = urlquote_plus(name)
    return 'client_%s_export.csv' % safe_name


def format_client_status(client):
    """Format client status for display."""
    if client.is_active:
        status = _(u'Active')
    else:
        status = _(u'Inactive')
    
    name = force_text(client.name)
    return smart_text(_(u'%(name)s - %(status)s') % {
        'name': name,
        'status': status,
    })
