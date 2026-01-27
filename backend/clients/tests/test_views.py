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


@pytest.mark.django_db
class TestClientPermissions:
    """Tests for client permission enforcement."""

    def test_admin_can_list_clients(self, api_client, admin_user, client_obj):
        """Test that ADMIN role can list clients."""
        api_client.force_authenticate(user=admin_user)
        response = api_client.get('/api/clients/')
        assert response.status_code == status.HTTP_200_OK

    def test_admin_can_create_client(self, api_client, admin_user):
        """Test that ADMIN role can create clients."""
        api_client.force_authenticate(user=admin_user)
        response = api_client.post('/api/clients/', {'name': 'New Client'})
        assert response.status_code == status.HTTP_201_CREATED

    def test_admin_can_update_client(self, api_client, admin_user, client_obj):
        """Test that ADMIN role can update clients."""
        api_client.force_authenticate(user=admin_user)
        response = api_client.patch(
            f'/api/clients/{client_obj.id}/',
            {'name': 'Updated Client'}
        )
        assert response.status_code == status.HTTP_200_OK

    def test_admin_can_delete_client(self, api_client, admin_user, client_obj):
        """Test that ADMIN role can delete clients."""
        api_client.force_authenticate(user=admin_user)
        response = api_client.delete(f'/api/clients/{client_obj.id}/')
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_planner_can_list_clients(self, api_client, planner_user, client_obj):
        """Test that PLANNER role can list clients."""
        api_client.force_authenticate(user=planner_user)
        response = api_client.get('/api/clients/')
        assert response.status_code == status.HTTP_200_OK

    def test_planner_can_create_client(self, api_client, planner_user):
        """Test that PLANNER role can create clients."""
        api_client.force_authenticate(user=planner_user)
        response = api_client.post('/api/clients/', {'name': 'Planner Client'})
        assert response.status_code == status.HTTP_201_CREATED

    def test_approver_can_list_clients(self, api_client, approver_user, client_obj):
        """Test that APPROVER role can list clients."""
        api_client.force_authenticate(user=approver_user)
        response = api_client.get('/api/clients/')
        assert response.status_code == status.HTTP_200_OK

    def test_approver_can_create_client(self, api_client, approver_user):
        """Test that APPROVER role can create clients."""
        api_client.force_authenticate(user=approver_user)
        response = api_client.post('/api/clients/', {'name': 'Approver Client'})
        assert response.status_code == status.HTTP_201_CREATED

    def test_viewer_can_list_clients(self, api_client, viewer_user, client_obj):
        """Test that VIEWER role can list clients."""
        api_client.force_authenticate(user=viewer_user)
        response = api_client.get('/api/clients/')
        assert response.status_code == status.HTTP_200_OK

    def test_viewer_can_create_client(self, api_client, viewer_user):
        """Test that VIEWER role can create clients."""
        api_client.force_authenticate(user=viewer_user)
        response = api_client.post('/api/clients/', {'name': 'Viewer Client'})
        assert response.status_code == status.HTTP_201_CREATED

    def test_unauthenticated_cannot_list_clients(self, api_client, client_obj):
        """Test that unauthenticated users cannot list clients."""
        response = api_client.get('/api/clients/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_unauthenticated_cannot_create_client(self, api_client):
        """Test that unauthenticated users cannot create clients."""
        response = api_client.post('/api/clients/', {'name': 'Unauthenticated Client'})
        assert response.status_code == status.HTTP_403_FORBIDDEN

