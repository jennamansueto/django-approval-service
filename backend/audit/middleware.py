"""Request logging and AJAX detection middleware."""
import logging

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware:
    """Middleware to log all incoming requests and responses."""

    def __init__(self, get_response):
        """Initialize the middleware with the get_response callable."""
        self.get_response = get_response

    def __call__(self, request):
        """Process the request and response."""
        path = str(request.path)
        method = str(request.method)
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        
        logger.info(
            "Request: %s %s (AJAX: %s)",
            method,
            path,
            is_ajax,
        )
        
        # Store request info for response logging
        request._request_logged = True

        response = self.get_response(request)

        if getattr(request, '_request_logged', False):
            logger.info(
                "Response: %s %s -> %d",
                request.method,
                path,
                response.status_code,
            )

        return response

    def process_exception(self, request, exception):
        """Log exceptions."""
        logger.error(
            "Exception on %s %s: %s",
            request.method,
            str(request.path),
            str(exception),
        )
        return None


class AjaxOnlyMiddleware:
    """Middleware that adds helper attribute for AJAX detection."""

    def __init__(self, get_response):
        """Initialize the middleware with the get_response callable."""
        self.get_response = get_response

    def __call__(self, request):
        """Process the request."""
        request.is_ajax_request = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        return self.get_response(request)
