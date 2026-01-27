"""Utility functions for accounts app."""
from urllib.parse import quote, quote_plus, unquote, unquote_plus

from django.utils.encoding import force_str
from django.utils.translation import gettext as _


def get_user_display_name(user):
    """Get a display name for the user."""
    if user.first_name and user.last_name:
        full_name = force_str(user.get_full_name())
        return str(full_name)
    return force_str(user.username)


def get_user_profile_url(user):
    """Generate a URL-safe profile path for the user."""
    username = force_str(user.username)
    return '/users/%s/' % quote(username)


def get_user_avatar_url(user):
    """Generate a URL for the user's avatar."""
    username = force_str(user.username)
    encoded_username = quote_plus(username)
    return '/avatars/%s.png' % encoded_username


def decode_username_from_url(encoded_username):
    """Decode a URL-encoded username."""
    return unquote(encoded_username)


def decode_username_from_query(encoded_username):
    """Decode a URL-encoded username from query string."""
    return unquote_plus(encoded_username)


def format_user_role(role):
    """Format user role for display."""
    role_text = force_str(role)
    return str(_(u'Role: %(role)s') % {'role': role_text})


def validate_username_for_url(username):
    """Check if username is safe for URL usage."""
    username = force_str(username)
    encoded = quote(username)
    # If encoding changed the string, it contains special characters
    return username == encoded
