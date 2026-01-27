"""Utility functions for accounts app."""
from django.utils.encoding import force_text, smart_text
from django.utils.http import urlquote, urlquote_plus, urlunquote, urlunquote_plus
from django.utils.translation import ugettext as _


def get_user_display_name(user):
    """Get a display name for the user."""
    if user.first_name and user.last_name:
        full_name = force_text(user.get_full_name())
        return smart_text(full_name)
    return force_text(user.username)


def get_user_profile_url(user):
    """Generate a URL-safe profile path for the user."""
    username = force_text(user.username)
    return '/users/%s/' % urlquote(username)


def get_user_avatar_url(user):
    """Generate a URL for the user's avatar."""
    username = force_text(user.username)
    encoded_username = urlquote_plus(username)
    return '/avatars/%s.png' % encoded_username


def decode_username_from_url(encoded_username):
    """Decode a URL-encoded username."""
    return urlunquote(encoded_username)


def decode_username_from_query(encoded_username):
    """Decode a URL-encoded username from query string."""
    return urlunquote_plus(encoded_username)


def format_user_role(role):
    """Format user role for display."""
    role_text = force_text(role)
    return smart_text(_(u'Role: %(role)s') % {'role': role_text})


def validate_username_for_url(username):
    """Check if username is safe for URL usage."""
    username = force_text(username)
    encoded = urlquote(username)
    # If encoding changed the string, it contains special characters
    return username == encoded
