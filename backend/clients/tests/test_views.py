"""Tests for clients views."""
import pytest
from rest_framework import status
from rest_framework.test import APIClient

from accounts.models import User
from clients.models import Client
from conftest import TEST_USER_CREDENTIAL


@pytest.fixture
def api_client():
    """Return API client."""
    return APIClient()


@pytest.fixture
def admin_user():
    """Create an admin user."""
    return User.objects.create_user(
        username='admin',
        email='admin@example.com',
        password=TEST_USER_CREDENTIAL,
        role=User.ADMIN,
    )


@pytest.fixture
def client_obj():
    """Create a test client."""
    return Client.objects.create(name='Test Client')


@pytest.mark.django_db
class TestClientViewSet:
    """Tests for Client viewset."""

    def test_list_clients(self, api_client, admin_user, client_obj):
        """Test listing clients."""
        api_client.force_authenticate(user=admin_user)
        response = api_client.get('/api/clients/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['name'] == 'Test Client'

