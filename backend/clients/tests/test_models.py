"""Tests for clients models."""
import pytest

from clients.models import Client


@pytest.mark.django_db
class TestClientModel:
    """Tests for Client model."""

    def test_create_client(self):
        """Test creating a client."""
        client = Client.objects.create(name='Acme Corp')
        assert client.name == 'Acme Corp'
        assert client.created_at is not None

    def test_client_str(self):
        """Test client string representation."""
        client = Client.objects.create(name='Test Company')
        assert str(client) == 'Test Company'
