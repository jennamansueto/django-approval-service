"""Request logging and AJAX detection middleware."""
import json
import logging

from django.utils.deprecation import MiddlewareMixin
from django.utils.encoding import force_text

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware(MiddlewareMixin):
    """Middleware to log all incoming requests and responses."""

    def process_request(self, request):
        """Log incoming request details."""
        path = force_text(request.path)
        method = force_text(request.method)
        is_ajax = request.is_ajax()
        
        logger.info(
            "Request: %s %s (AJAX: %s)",
            method,
            path,
            is_ajax,
        )
        
        # Store request info for response logging
        request._request_logged = True

    def process_response(self, request, response):
        """Log response details."""
        if getattr(request, '_request_logged', False):
            path = force_text(request.path)
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
            force_text(request.path),
            force_text(exception),
        )
        return None


class AjaxOnlyMiddleware(MiddlewareMixin):
    """Middleware that adds helper attribute for AJAX detection."""

    def process_request(self, request):
        """Add is_ajax_request attribute to request."""
        request.is_ajax_request = request.is_ajax()
