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


@pytest.mark.django_db
class TestDeliverableViewSetPermissions:
    """Tests for Deliverable viewset permissions (IsAdminOrPlanner)."""

    def test_list_deliverables_unauthenticated(self, api_client, deliverable):
        """Test that unauthenticated users cannot list deliverables."""
        response = api_client.get('/api/deliverables/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_list_deliverables_admin(self, api_client, admin_user, deliverable):
        """Test that admin can list deliverables."""
        api_client.force_authenticate(user=admin_user)
        response = api_client.get('/api/deliverables/')
        assert response.status_code == status.HTTP_200_OK

    def test_list_deliverables_planner(self, api_client, planner_user, deliverable):
        """Test that planner can list deliverables."""
        api_client.force_authenticate(user=planner_user)
        response = api_client.get('/api/deliverables/')
        assert response.status_code == status.HTTP_200_OK

    def test_list_deliverables_approver_denied(self, api_client, approver_user, deliverable):
        """Test that approver cannot list deliverables."""
        api_client.force_authenticate(user=approver_user)
        response = api_client.get('/api/deliverables/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_list_deliverables_viewer_denied(self, api_client, viewer_user, deliverable):
        """Test that viewer cannot list deliverables."""
        api_client.force_authenticate(user=viewer_user)
        response = api_client.get('/api/deliverables/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_retrieve_deliverable_unauthenticated(self, api_client, deliverable):
        """Test that unauthenticated users cannot retrieve a deliverable."""
        response = api_client.get(f'/api/deliverables/{deliverable.id}/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_retrieve_deliverable_admin(self, api_client, admin_user, deliverable):
        """Test that admin can retrieve a deliverable."""
        api_client.force_authenticate(user=admin_user)
        response = api_client.get(f'/api/deliverables/{deliverable.id}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'Test Deliverable'

    def test_retrieve_deliverable_planner(self, api_client, planner_user, deliverable):
        """Test that planner can retrieve a deliverable."""
        api_client.force_authenticate(user=planner_user)
        response = api_client.get(f'/api/deliverables/{deliverable.id}/')
        assert response.status_code == status.HTTP_200_OK

    def test_retrieve_deliverable_approver_denied(self, api_client, approver_user, deliverable):
        """Test that approver cannot retrieve a deliverable."""
        api_client.force_authenticate(user=approver_user)
        response = api_client.get(f'/api/deliverables/{deliverable.id}/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_retrieve_deliverable_viewer_denied(self, api_client, viewer_user, deliverable):
        """Test that viewer cannot retrieve a deliverable."""
        api_client.force_authenticate(user=viewer_user)
        response = api_client.get(f'/api/deliverables/{deliverable.id}/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_deliverable_unauthenticated(self, api_client, client_obj):
        """Test that unauthenticated users cannot create a deliverable."""
        response = api_client.post(
            '/api/deliverables/',
            {'title': 'New Deliverable', 'client': client_obj.id},
            format='json'
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_deliverable_admin(self, api_client, admin_user, client_obj):
        """Test that admin can create a deliverable."""
        api_client.force_authenticate(user=admin_user)
        response = api_client.post(
            '/api/deliverables/',
            {'title': 'New Deliverable', 'client': client_obj.id},
            format='json'
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['title'] == 'New Deliverable'

    def test_create_deliverable_planner(self, api_client, planner_user, client_obj):
        """Test that planner can create a deliverable."""
        api_client.force_authenticate(user=planner_user)
        response = api_client.post(
            '/api/deliverables/',
            {'title': 'New Deliverable', 'client': client_obj.id},
            format='json'
        )
        assert response.status_code == status.HTTP_201_CREATED

    def test_create_deliverable_approver_denied(self, api_client, approver_user, client_obj):
        """Test that approver cannot create a deliverable."""
        api_client.force_authenticate(user=approver_user)
        response = api_client.post(
            '/api/deliverables/',
            {'title': 'New Deliverable', 'client': client_obj.id},
            format='json'
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_deliverable_viewer_denied(self, api_client, viewer_user, client_obj):
        """Test that viewer cannot create a deliverable."""
        api_client.force_authenticate(user=viewer_user)
        response = api_client.post(
            '/api/deliverables/',
            {'title': 'New Deliverable', 'client': client_obj.id},
            format='json'
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_deliverable_unauthenticated(self, api_client, deliverable, client_obj):
        """Test that unauthenticated users cannot update a deliverable."""
        response = api_client.put(
            f'/api/deliverables/{deliverable.id}/',
            {'title': 'Updated Deliverable', 'client': client_obj.id},
            format='json'
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_deliverable_admin(self, api_client, admin_user, deliverable, client_obj):
        """Test that admin can update a deliverable."""
        api_client.force_authenticate(user=admin_user)
        response = api_client.put(
            f'/api/deliverables/{deliverable.id}/',
            {'title': 'Updated Deliverable', 'client': client_obj.id},
            format='json'
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'Updated Deliverable'

    def test_update_deliverable_planner(self, api_client, planner_user, deliverable, client_obj):
        """Test that planner can update a deliverable."""
        api_client.force_authenticate(user=planner_user)
        response = api_client.put(
            f'/api/deliverables/{deliverable.id}/',
            {'title': 'Updated Deliverable', 'client': client_obj.id},
            format='json'
        )
        assert response.status_code == status.HTTP_200_OK

    def test_update_deliverable_approver_denied(self, api_client, approver_user, deliverable, client_obj):
        """Test that approver cannot update a deliverable."""
        api_client.force_authenticate(user=approver_user)
        response = api_client.put(
            f'/api/deliverables/{deliverable.id}/',
            {'title': 'Updated Deliverable', 'client': client_obj.id},
            format='json'
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_deliverable_viewer_denied(self, api_client, viewer_user, deliverable, client_obj):
        """Test that viewer cannot update a deliverable."""
        api_client.force_authenticate(user=viewer_user)
        response = api_client.put(
            f'/api/deliverables/{deliverable.id}/',
            {'title': 'Updated Deliverable', 'client': client_obj.id},
            format='json'
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_deliverable_unauthenticated(self, api_client, deliverable):
        """Test that unauthenticated users cannot delete a deliverable."""
        response = api_client.delete(f'/api/deliverables/{deliverable.id}/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_deliverable_admin(self, api_client, admin_user, deliverable):
        """Test that admin can delete a deliverable."""
        api_client.force_authenticate(user=admin_user)
        response = api_client.delete(f'/api/deliverables/{deliverable.id}/')
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_deliverable_planner(self, api_client, planner_user, deliverable):
        """Test that planner can delete a deliverable."""
        api_client.force_authenticate(user=planner_user)
        response = api_client.delete(f'/api/deliverables/{deliverable.id}/')
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_deliverable_approver_denied(self, api_client, approver_user, deliverable):
        """Test that approver cannot delete a deliverable."""
        api_client.force_authenticate(user=approver_user)
        response = api_client.delete(f'/api/deliverables/{deliverable.id}/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_deliverable_viewer_denied(self, api_client, viewer_user, deliverable):
        """Test that viewer cannot delete a deliverable."""
        api_client.force_authenticate(user=viewer_user)
        response = api_client.delete(f'/api/deliverables/{deliverable.id}/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_submit_deliverable_unauthenticated(self, api_client, deliverable):
        """Test that unauthenticated users cannot submit a deliverable."""
        response = api_client.post(f'/api/deliverables/{deliverable.id}/submit/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_submit_deliverable_admin(self, api_client, admin_user, client_obj):
        """Test that admin can submit a deliverable."""
        deliverable = Deliverable.objects.create(
            title='Admin Deliverable',
            client=client_obj,
            created_by=admin_user,
            status=Deliverable.DRAFT,
        )
        api_client.force_authenticate(user=admin_user)
        response = api_client.post(f'/api/deliverables/{deliverable.id}/submit/')
        assert response.status_code == status.HTTP_200_OK

    def test_submit_deliverable_planner(self, api_client, planner_user, deliverable):
        """Test that planner can submit a deliverable."""
        api_client.force_authenticate(user=planner_user)
        response = api_client.post(f'/api/deliverables/{deliverable.id}/submit/')
        assert response.status_code == status.HTTP_200_OK

    def test_submit_deliverable_approver_denied(self, api_client, approver_user, deliverable):
        """Test that approver cannot submit a deliverable."""
        api_client.force_authenticate(user=approver_user)
        response = api_client.post(f'/api/deliverables/{deliverable.id}/submit/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_submit_deliverable_viewer_denied(self, api_client, viewer_user, deliverable):
        """Test that viewer cannot submit a deliverable."""
        api_client.force_authenticate(user=viewer_user)
        response = api_client.post(f'/api/deliverables/{deliverable.id}/submit/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

