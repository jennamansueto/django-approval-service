"""Tests for deliverables views."""
import pytest
from rest_framework import status
from rest_framework.test import APIClient

from accounts.models import User
from clients.models import Client
from deliverables.models import Deliverable


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


@pytest.fixture
def deliverable(client_obj, planner_user):
    """Create a test deliverable."""
    return Deliverable.objects.create(
        title='Test Deliverable',
        client=client_obj,
        created_by=planner_user,
    )


@pytest.mark.django_db
class TestDeliverableViewSet:
    """Tests for Deliverable viewset."""

    def test_list_deliverables(self, api_client, planner_user, deliverable):
        """Test listing deliverables."""
        api_client.force_authenticate(user=planner_user)
        response = api_client.get('/api/deliverables/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_unauthenticated_cannot_list_deliverables(self, api_client, deliverable):
        """Test unauthenticated user cannot list deliverables."""
        response = api_client.get('/api/deliverables/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_unauthenticated_cannot_create_deliverable(self, api_client, client_obj):
        """Test unauthenticated user cannot create deliverable."""
        response = api_client.post('/api/deliverables/', {
            'title': 'Test',
            'client': client_obj.id,
        })
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_viewer_cannot_list_deliverables(self, api_client, viewer_user, deliverable):
        """Test VIEWER role cannot list deliverables."""
        api_client.force_authenticate(user=viewer_user)
        response = api_client.get('/api/deliverables/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_approver_cannot_list_deliverables(self, api_client, approver_user, deliverable):
        """Test APPROVER role cannot list deliverables."""
        api_client.force_authenticate(user=approver_user)
        response = api_client.get('/api/deliverables/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_viewer_cannot_create_deliverable(self, api_client, viewer_user, client_obj):
        """Test VIEWER role cannot create deliverable."""
        api_client.force_authenticate(user=viewer_user)
        response = api_client.post('/api/deliverables/', {
            'title': 'Test',
            'client': client_obj.id,
        })
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_approver_cannot_create_deliverable(self, api_client, approver_user, client_obj):
        """Test APPROVER role cannot create deliverable."""
        api_client.force_authenticate(user=approver_user)
        response = api_client.post('/api/deliverables/', {
            'title': 'Test',
            'client': client_obj.id,
        })
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_viewer_cannot_update_deliverable(self, api_client, viewer_user, deliverable):
        """Test VIEWER role cannot update deliverable."""
        api_client.force_authenticate(user=viewer_user)
        response = api_client.put(
            f'/api/deliverables/{deliverable.id}/',
            {'title': 'Updated', 'client': deliverable.client.id},
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_approver_cannot_update_deliverable(self, api_client, approver_user, deliverable):
        """Test APPROVER role cannot update deliverable."""
        api_client.force_authenticate(user=approver_user)
        response = api_client.put(
            f'/api/deliverables/{deliverable.id}/',
            {'title': 'Updated', 'client': deliverable.client.id},
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_viewer_cannot_delete_deliverable(self, api_client, viewer_user, deliverable):
        """Test VIEWER role cannot delete deliverable."""
        api_client.force_authenticate(user=viewer_user)
        response = api_client.delete(f'/api/deliverables/{deliverable.id}/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_approver_cannot_delete_deliverable(self, api_client, approver_user, deliverable):
        """Test APPROVER role cannot delete deliverable."""
        api_client.force_authenticate(user=approver_user)
        response = api_client.delete(f'/api/deliverables/{deliverable.id}/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_viewer_cannot_submit_deliverable(self, api_client, viewer_user, deliverable):
        """Test VIEWER role cannot submit deliverable."""
        api_client.force_authenticate(user=viewer_user)
        response = api_client.post(f'/api/deliverables/{deliverable.id}/submit/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_approver_cannot_submit_deliverable(self, api_client, approver_user, deliverable):
        """Test APPROVER role cannot submit deliverable."""
        api_client.force_authenticate(user=approver_user)
        response = api_client.post(f'/api/deliverables/{deliverable.id}/submit/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_admin_can_list_deliverables(self, api_client, admin_user, deliverable):
        """Test ADMIN role can list deliverables."""
        api_client.force_authenticate(user=admin_user)
        response = api_client.get('/api/deliverables/')
        assert response.status_code == status.HTTP_200_OK

    def test_planner_can_create_deliverable(self, api_client, planner_user, client_obj):
        """Test PLANNER role can create deliverable."""
        api_client.force_authenticate(user=planner_user)
        response = api_client.post('/api/deliverables/', {
            'title': 'New Deliverable',
            'client': client_obj.id,
        })
        assert response.status_code == status.HTTP_201_CREATED

    def test_planner_can_submit_deliverable(self, api_client, planner_user, deliverable):
        """Test PLANNER role can submit deliverable."""
        api_client.force_authenticate(user=planner_user)
        response = api_client.post(f'/api/deliverables/{deliverable.id}/submit/')
        assert response.status_code == status.HTTP_200_OK

