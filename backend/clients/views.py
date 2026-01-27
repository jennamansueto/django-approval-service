"""Views for clients app."""
from django.utils.encoding import force_str
from django.utils.translation import gettext as _
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Client
from .serializers import ClientSerializer


class ClientViewSet(viewsets.ModelViewSet):
    """ViewSet for Client model."""

    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter queryset based on request parameters."""
        queryset = super().get_queryset()
        
        # Filter by name if provided
        name = self.request.query_params.get('name')
        if name:
            name = force_str(name)
            queryset = queryset.filter(name__icontains=name)
        
        # Filter by active status
        is_active = self.request.query_params.get('is_active')
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        
        return queryset

    def list(self, request, *args, **kwargs):
        """List clients with AJAX-aware response."""
        response = super().list(request, *args, **kwargs)
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return Response({
                'success': True,
                'count': len(response.data),
                'results': response.data,
                'message': str(_(u'Clients retrieved successfully')),
            })
        return response

    @action(detail=True, methods=['post'])
    def toggle_active(self, request, pk=None):
        """Toggle the active status of a client."""
        client = self.get_object()
        client.is_active = not client.is_active
        client.save()
        
        status_text = _(u'activated') if client.is_active else _(u'deactivated')
        message = _(u'Client %(name)s has been %(status)s') % {
            'name': force_str(client.name),
            'status': str(status_text),
        }
        
        return Response({
            'success': True,
            'message': str(message),
            'client': ClientSerializer(client).data,
        })
