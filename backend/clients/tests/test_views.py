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
class TestClientViewSetPermissions:
    """Tests for Client viewset permissions."""

    def test_list_clients_unauthenticated(self, api_client, client_obj):
        """Test that unauthenticated users cannot list clients."""
        response = api_client.get('/api/clients/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_list_clients_admin(self, api_client, admin_user, client_obj):
        """Test that admin can list clients."""
        api_client.force_authenticate(user=admin_user)
        response = api_client.get('/api/clients/')
        assert response.status_code == status.HTTP_200_OK

    def test_list_clients_planner(self, api_client, planner_user, client_obj):
        """Test that planner can list clients."""
        api_client.force_authenticate(user=planner_user)
        response = api_client.get('/api/clients/')
        assert response.status_code == status.HTTP_200_OK

    def test_list_clients_approver(self, api_client, approver_user, client_obj):
        """Test that approver can list clients."""
        api_client.force_authenticate(user=approver_user)
        response = api_client.get('/api/clients/')
        assert response.status_code == status.HTTP_200_OK

    def test_list_clients_viewer(self, api_client, viewer_user, client_obj):
        """Test that viewer can list clients."""
        api_client.force_authenticate(user=viewer_user)
        response = api_client.get('/api/clients/')
        assert response.status_code == status.HTTP_200_OK

    def test_retrieve_client_unauthenticated(self, api_client, client_obj):
        """Test that unauthenticated users cannot retrieve a client."""
        response = api_client.get(f'/api/clients/{client_obj.id}/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_retrieve_client_admin(self, api_client, admin_user, client_obj):
        """Test that admin can retrieve a client."""
        api_client.force_authenticate(user=admin_user)
        response = api_client.get(f'/api/clients/{client_obj.id}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == 'Test Client'

    def test_retrieve_client_viewer(self, api_client, viewer_user, client_obj):
        """Test that viewer can retrieve a client."""
        api_client.force_authenticate(user=viewer_user)
        response = api_client.get(f'/api/clients/{client_obj.id}/')
        assert response.status_code == status.HTTP_200_OK

    def test_create_client_unauthenticated(self, api_client):
        """Test that unauthenticated users cannot create a client."""
        response = api_client.post('/api/clients/', {'name': 'New Client'}, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_client_admin(self, api_client, admin_user):
        """Test that admin can create a client."""
        api_client.force_authenticate(user=admin_user)
        response = api_client.post('/api/clients/', {'name': 'New Client'}, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['name'] == 'New Client'

    def test_create_client_planner(self, api_client, planner_user):
        """Test that planner can create a client."""
        api_client.force_authenticate(user=planner_user)
        response = api_client.post('/api/clients/', {'name': 'New Client'}, format='json')
        assert response.status_code == status.HTTP_201_CREATED

    def test_create_client_approver(self, api_client, approver_user):
        """Test that approver can create a client."""
        api_client.force_authenticate(user=approver_user)
        response = api_client.post('/api/clients/', {'name': 'New Client'}, format='json')
        assert response.status_code == status.HTTP_201_CREATED

    def test_create_client_viewer(self, api_client, viewer_user):
        """Test that viewer can create a client."""
        api_client.force_authenticate(user=viewer_user)
        response = api_client.post('/api/clients/', {'name': 'New Client'}, format='json')
        assert response.status_code == status.HTTP_201_CREATED

    def test_update_client_unauthenticated(self, api_client, client_obj):
        """Test that unauthenticated users cannot update a client."""
        response = api_client.put(
            f'/api/clients/{client_obj.id}/',
            {'name': 'Updated Client'},
            format='json'
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_client_admin(self, api_client, admin_user, client_obj):
        """Test that admin can update a client."""
        api_client.force_authenticate(user=admin_user)
        response = api_client.put(
            f'/api/clients/{client_obj.id}/',
            {'name': 'Updated Client'},
            format='json'
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == 'Updated Client'

    def test_update_client_viewer(self, api_client, viewer_user, client_obj):
        """Test that viewer can update a client."""
        api_client.force_authenticate(user=viewer_user)
        response = api_client.put(
            f'/api/clients/{client_obj.id}/',
            {'name': 'Updated Client'},
            format='json'
        )
        assert response.status_code == status.HTTP_200_OK

    def test_delete_client_unauthenticated(self, api_client, client_obj):
        """Test that unauthenticated users cannot delete a client."""
        response = api_client.delete(f'/api/clients/{client_obj.id}/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_client_admin(self, api_client, admin_user, client_obj):
        """Test that admin can delete a client."""
        api_client.force_authenticate(user=admin_user)
        response = api_client.delete(f'/api/clients/{client_obj.id}/')
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_client_viewer(self, api_client, viewer_user, client_obj):
        """Test that viewer can delete a client."""
        api_client.force_authenticate(user=viewer_user)
        response = api_client.delete(f'/api/clients/{client_obj.id}/')
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_toggle_active_unauthenticated(self, api_client, client_obj):
        """Test that unauthenticated users cannot toggle client active status."""
        response = api_client.post(f'/api/clients/{client_obj.id}/toggle_active/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_toggle_active_admin(self, api_client, admin_user, client_obj):
        """Test that admin can toggle client active status."""
        api_client.force_authenticate(user=admin_user)
        response = api_client.post(f'/api/clients/{client_obj.id}/toggle_active/')
        assert response.status_code == status.HTTP_200_OK

    def test_toggle_active_planner(self, api_client, planner_user, client_obj):
        """Test that planner can toggle client active status."""
        api_client.force_authenticate(user=planner_user)
        response = api_client.post(f'/api/clients/{client_obj.id}/toggle_active/')
        assert response.status_code == status.HTTP_200_OK

    def test_toggle_active_approver(self, api_client, approver_user, client_obj):
        """Test that approver can toggle client active status."""
        api_client.force_authenticate(user=approver_user)
        response = api_client.post(f'/api/clients/{client_obj.id}/toggle_active/')
        assert response.status_code == status.HTTP_200_OK

    def test_toggle_active_viewer(self, api_client, viewer_user, client_obj):
        """Test that viewer can toggle client active status."""
        api_client.force_authenticate(user=viewer_user)
        response = api_client.post(f'/api/clients/{client_obj.id}/toggle_active/')
        assert response.status_code == status.HTTP_200_OK

