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
        role=User.Role.PLANNER,
    )


@pytest.fixture
def approver_user():
    """Create an approver user."""
    return User.objects.create_user(
        username='approver',
        email='approver@example.com',
        password='testpass123',
        role=User.Role.APPROVER,
    )


@pytest.fixture
def viewer_user():
    """Create a viewer user."""
    return User.objects.create_user(
        username='viewer',
        email='viewer@example.com',
        password='testpass123',
        role=User.Role.VIEWER,
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

    def test_list_clients_unauthenticated(self, api_client, client_obj):
        """Test listing clients without authentication."""
        response = api_client.get('/api/clients/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_list_clients_multiple(self, api_client, admin_user):
        """Test listing multiple clients."""
        Client.objects.create(name='Client A')
        Client.objects.create(name='Client B')
        Client.objects.create(name='Client C')

        api_client.force_authenticate(user=admin_user)
        response = api_client.get('/api/clients/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 3

    def test_list_clients_ordered_by_name(self, api_client, admin_user):
        """Test that clients are ordered by name."""
        Client.objects.create(name='Zebra Corp')
        Client.objects.create(name='Alpha Inc')
        Client.objects.create(name='Beta LLC')

        api_client.force_authenticate(user=admin_user)
        response = api_client.get('/api/clients/')
        assert response.status_code == status.HTTP_200_OK
        names = [c['name'] for c in response.data]
        assert names == ['Alpha Inc', 'Beta LLC', 'Zebra Corp']


@pytest.mark.django_db
class TestClientCreate:
    """Tests for creating clients."""

    def test_create_client(self, api_client, admin_user):
        """Test creating a client."""
        api_client.force_authenticate(user=admin_user)
        response = api_client.post(
            '/api/clients/',
            {'name': 'New Client'},
            format='json',
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['name'] == 'New Client'
        assert 'id' in response.data
        assert 'created_at' in response.data
        assert 'updated_at' in response.data

    def test_create_client_planner(self, api_client, planner_user):
        """Test that planner can create a client."""
        api_client.force_authenticate(user=planner_user)
        response = api_client.post(
            '/api/clients/',
            {'name': 'Planner Client'},
            format='json',
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['name'] == 'Planner Client'

    def test_create_client_approver(self, api_client, approver_user):
        """Test that approver can create a client."""
        api_client.force_authenticate(user=approver_user)
        response = api_client.post(
            '/api/clients/',
            {'name': 'Approver Client'},
            format='json',
        )
        assert response.status_code == status.HTTP_201_CREATED

    def test_create_client_viewer(self, api_client, viewer_user):
        """Test that viewer can create a client."""
        api_client.force_authenticate(user=viewer_user)
        response = api_client.post(
            '/api/clients/',
            {'name': 'Viewer Client'},
            format='json',
        )
        assert response.status_code == status.HTTP_201_CREATED

    def test_create_client_unauthenticated(self, api_client):
        """Test creating a client without authentication."""
        response = api_client.post(
            '/api/clients/',
            {'name': 'New Client'},
            format='json',
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_client_missing_name(self, api_client, admin_user):
        """Test creating a client without name."""
        api_client.force_authenticate(user=admin_user)
        response = api_client.post(
            '/api/clients/',
            {},
            format='json',
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_client_empty_name(self, api_client, admin_user):
        """Test creating a client with empty name."""
        api_client.force_authenticate(user=admin_user)
        response = api_client.post(
            '/api/clients/',
            {'name': ''},
            format='json',
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestClientRetrieve:
    """Tests for retrieving a single client."""

    def test_retrieve_client(self, api_client, admin_user, client_obj):
        """Test retrieving a single client."""
        api_client.force_authenticate(user=admin_user)
        response = api_client.get(f'/api/clients/{client_obj.id}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == client_obj.id
        assert response.data['name'] == 'Test Client'

    def test_retrieve_client_unauthenticated(self, api_client, client_obj):
        """Test retrieving a client without authentication."""
        response = api_client.get(f'/api/clients/{client_obj.id}/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_retrieve_nonexistent_client(self, api_client, admin_user):
        """Test retrieving a non-existent client."""
        api_client.force_authenticate(user=admin_user)
        response = api_client.get('/api/clients/99999/')
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestClientUpdate:
    """Tests for updating clients."""

    def test_update_client(self, api_client, admin_user, client_obj):
        """Test updating a client."""
        api_client.force_authenticate(user=admin_user)
        response = api_client.put(
            f'/api/clients/{client_obj.id}/',
            {'name': 'Updated Client'},
            format='json',
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == 'Updated Client'

        client_obj.refresh_from_db()
        assert client_obj.name == 'Updated Client'

    def test_partial_update_client(self, api_client, admin_user, client_obj):
        """Test partial update of a client."""
        api_client.force_authenticate(user=admin_user)
        response = api_client.patch(
            f'/api/clients/{client_obj.id}/',
            {'name': 'Patched Client'},
            format='json',
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == 'Patched Client'

    def test_update_client_unauthenticated(self, api_client, client_obj):
        """Test updating a client without authentication."""
        response = api_client.put(
            f'/api/clients/{client_obj.id}/',
            {'name': 'Updated Client'},
            format='json',
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_nonexistent_client(self, api_client, admin_user):
        """Test updating a non-existent client."""
        api_client.force_authenticate(user=admin_user)
        response = api_client.put(
            '/api/clients/99999/',
            {'name': 'Updated Client'},
            format='json',
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestClientDelete:
    """Tests for deleting clients."""

    def test_delete_client(self, api_client, admin_user, client_obj):
        """Test deleting a client."""
        client_id = client_obj.id
        api_client.force_authenticate(user=admin_user)
        response = api_client.delete(f'/api/clients/{client_id}/')
        assert response.status_code == status.HTTP_204_NO_CONTENT

        assert not Client.objects.filter(id=client_id).exists()

    def test_delete_client_unauthenticated(self, api_client, client_obj):
        """Test deleting a client without authentication."""
        response = api_client.delete(f'/api/clients/{client_obj.id}/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_nonexistent_client(self, api_client, admin_user):
        """Test deleting a non-existent client."""
        api_client.force_authenticate(user=admin_user)
        response = api_client.delete('/api/clients/99999/')
        assert response.status_code == status.HTTP_404_NOT_FOUND

