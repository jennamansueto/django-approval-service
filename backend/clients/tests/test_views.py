"""Tests for clients views."""
import pytest
from rest_framework import status
from rest_framework.test import APIClient

from accounts.models import User
from clients.models import Client


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
        password='testpass123',
        role=User.ADMIN,
    )


@pytest.fixture
def planner_user():
    """Create a planner user."""
    return User.objects.create_user(
        username='planner',
        email='planner@example.com',
        password='testpass123',
        role=User.PLANNER,
    )


@pytest.fixture
def approver_user():
    """Create an approver user."""
    return User.objects.create_user(
        username='approver',
        email='approver@example.com',
        password='testpass123',
        role=User.APPROVER,
    )


@pytest.fixture
def viewer_user():
    """Create a viewer user."""
    return User.objects.create_user(
        username='viewer',
        email='viewer@example.com',
        password='testpass123',
        role=User.VIEWER,
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

    def test_unauthenticated_cannot_list_clients(self, api_client, client_obj):
        """Test unauthenticated user cannot list clients."""
        response = api_client.get('/api/clients/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_unauthenticated_cannot_create_client(self, api_client):
        """Test unauthenticated user cannot create client."""
        response = api_client.post('/api/clients/', {'name': 'New Client'})
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_viewer_cannot_list_clients(self, api_client, viewer_user, client_obj):
        """Test VIEWER role cannot list clients."""
        api_client.force_authenticate(user=viewer_user)
        response = api_client.get('/api/clients/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_planner_cannot_list_clients(self, api_client, planner_user, client_obj):
        """Test PLANNER role cannot list clients."""
        api_client.force_authenticate(user=planner_user)
        response = api_client.get('/api/clients/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_approver_cannot_list_clients(self, api_client, approver_user, client_obj):
        """Test APPROVER role cannot list clients."""
        api_client.force_authenticate(user=approver_user)
        response = api_client.get('/api/clients/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_viewer_cannot_create_client(self, api_client, viewer_user):
        """Test VIEWER role cannot create client."""
        api_client.force_authenticate(user=viewer_user)
        response = api_client.post('/api/clients/', {'name': 'New Client'})
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_planner_cannot_create_client(self, api_client, planner_user):
        """Test PLANNER role cannot create client."""
        api_client.force_authenticate(user=planner_user)
        response = api_client.post('/api/clients/', {'name': 'New Client'})
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_approver_cannot_create_client(self, api_client, approver_user):
        """Test APPROVER role cannot create client."""
        api_client.force_authenticate(user=approver_user)
        response = api_client.post('/api/clients/', {'name': 'New Client'})
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_viewer_cannot_update_client(self, api_client, viewer_user, client_obj):
        """Test VIEWER role cannot update client."""
        api_client.force_authenticate(user=viewer_user)
        response = api_client.put(
            f'/api/clients/{client_obj.id}/',
            {'name': 'Updated Client'},
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_planner_cannot_update_client(self, api_client, planner_user, client_obj):
        """Test PLANNER role cannot update client."""
        api_client.force_authenticate(user=planner_user)
        response = api_client.put(
            f'/api/clients/{client_obj.id}/',
            {'name': 'Updated Client'},
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_approver_cannot_update_client(self, api_client, approver_user, client_obj):
        """Test APPROVER role cannot update client."""
        api_client.force_authenticate(user=approver_user)
        response = api_client.put(
            f'/api/clients/{client_obj.id}/',
            {'name': 'Updated Client'},
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_viewer_cannot_delete_client(self, api_client, viewer_user, client_obj):
        """Test VIEWER role cannot delete client."""
        api_client.force_authenticate(user=viewer_user)
        response = api_client.delete(f'/api/clients/{client_obj.id}/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_planner_cannot_delete_client(self, api_client, planner_user, client_obj):
        """Test PLANNER role cannot delete client."""
        api_client.force_authenticate(user=planner_user)
        response = api_client.delete(f'/api/clients/{client_obj.id}/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_approver_cannot_delete_client(self, api_client, approver_user, client_obj):
        """Test APPROVER role cannot delete client."""
        api_client.force_authenticate(user=approver_user)
        response = api_client.delete(f'/api/clients/{client_obj.id}/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

