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
def planner_user():
    """Create a planner user."""
    return User.objects.create_user(
        username='planner',
        email='planner@example.com',
        password='testpass123',
        role=User.PLANNER,
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
def approver_user():
    """Create an approver user."""
    return User.objects.create_user(
        username='approver',
        email='approver@example.com',
        password='testpass123',
        role=User.APPROVER,
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
class TestDeliverablePermissions:
    """Tests for deliverable creation permissions."""

    def test_admin_can_create_deliverable(self, api_client, admin_user, client_obj):
        """Test that Admin can POST /api/deliverables/."""
        api_client.force_authenticate(user=admin_user)
        response = api_client.post('/api/deliverables/', {
            'title': 'New Deliverable',
            'client': client_obj.id,
        }, format='json')
        assert response.status_code == status.HTTP_201_CREATED

    def test_planner_can_create_deliverable(self, api_client, planner_user, client_obj):
        """Test that Planner can POST /api/deliverables/."""
        api_client.force_authenticate(user=planner_user)
        response = api_client.post('/api/deliverables/', {
            'title': 'New Deliverable',
            'client': client_obj.id,
        }, format='json')
        assert response.status_code == status.HTTP_201_CREATED

    def test_approver_cannot_create_deliverable(self, api_client, approver_user, client_obj):
        """Test that Approver gets 403 when calling POST /api/deliverables/."""
        api_client.force_authenticate(user=approver_user)
        response = api_client.post('/api/deliverables/', {
            'title': 'New Deliverable',
            'client': client_obj.id,
        }, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_viewer_cannot_create_deliverable(self, api_client, viewer_user, client_obj):
        """Test that Viewer gets 403 when calling POST /api/deliverables/."""
        api_client.force_authenticate(user=viewer_user)
        response = api_client.post('/api/deliverables/', {
            'title': 'New Deliverable',
            'client': client_obj.id,
        }, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN

