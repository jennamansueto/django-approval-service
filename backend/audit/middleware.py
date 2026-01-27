"""Request logging and AJAX detection middleware."""
import logging

from django.utils.encoding import force_str

logger = logging.getLogger(__name__)


def _is_ajax(request):
    """Check if request is AJAX (replacement for deprecated request.is_ajax())."""
    return request.headers.get('X-Requested-With') == 'XMLHttpRequest'


class RequestLoggingMiddleware:
    """Middleware to log all incoming requests and responses."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        """Process request and response."""
        path = force_str(request.path)
        method = force_str(request.method)
        is_ajax = _is_ajax(request)

        logger.info(
            "Request: %s %s (AJAX: %s)",
            method,
            path,
            is_ajax,
        )

        request._request_logged = True

        try:
            response = self.get_response(request)
        except Exception as exception:
            logger.error(
                "Exception on %s %s: %s",
                request.method,
                force_str(request.path),
                force_str(exception),
            )
            raise

        if getattr(request, '_request_logged', False):
            path = force_str(request.path)
            status = response.status_code

            logger.info(
                "Response: %s %s -> %d",
                request.method,
                path,
                status,
            )

        return response


class AjaxOnlyMiddleware:
    """Middleware that adds helper attribute for AJAX detection."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        """Add is_ajax_request attribute to request."""
        request.is_ajax_request = _is_ajax(request)
        return self.get_response(request)
