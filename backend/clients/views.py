"""Views for clients app."""
from rest_framework import viewsets

from accounts.permissions import IsAdminUser

from .models import Client
from .serializers import ClientSerializer


class ClientViewSet(viewsets.ModelViewSet):
    """ViewSet for Client model."""

    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAdminUser]
