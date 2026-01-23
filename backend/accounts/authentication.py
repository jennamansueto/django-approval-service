"""Custom authentication classes."""
from rest_framework.authentication import SessionAuthentication


class CsrfExemptSessionAuthentication(SessionAuthentication):
    """Session authentication without CSRF enforcement."""

    def enforce_csrf(self, request):
        """Skip CSRF check."""
        return
