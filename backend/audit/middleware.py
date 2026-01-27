"""Request logging and AJAX detection middleware."""
import logging

from django.utils.encoding import force_str

logger = logging.getLogger(__name__)


def is_ajax(request):
    """Check if request is an AJAX request (replacement for deprecated request.is_ajax())."""
    return request.headers.get('X-Requested-With') == 'XMLHttpRequest'


class RequestLoggingMiddleware:
    """Middleware to log all incoming requests and responses."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        """Process the request and response."""
        path = force_str(request.path)
        method = force_str(request.method)
        ajax = is_ajax(request)

        logger.info(
            "Request: %s %s (AJAX: %s)",
            method,
            path,
            ajax,
        )

        # Store request info for response logging
        request._request_logged = True

        response = self.get_response(request)

        if getattr(request, '_request_logged', False):
            status = response.status_code

            logger.info(
                "Response: %s %s -> %d",
                request.method,
                path,
                status,
            )

        return response

    def process_exception(self, request, exception):
        """Log exceptions."""
        logger.error(
            "Exception on %s %s: %s",
            request.method,
            force_str(request.path),
            force_str(exception),
        )
        return None


class AjaxOnlyMiddleware:
    """Middleware that adds helper attribute for AJAX detection."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        """Add is_ajax_request attribute to request and process."""
        request.is_ajax_request = is_ajax(request)
        return self.get_response(request)
