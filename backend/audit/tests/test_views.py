"""Tests for audit views."""
import pytest
from rest_framework import status
from rest_framework.test import APIClient

from accounts.models import User
from audit.models import AuditEvent


@pytest.fixture
def api_client():
    """Return API client."""
    return APIClient()


@pytest.fixture
def user():
    """Create a test user."""
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123',
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
def audit_event(user):
    """Create a test audit event."""
    return AuditEvent.objects.create(
        actor=user,
        verb='submitted',
        object_type='Deliverable',
        object_id='1',
    )


@pytest.mark.django_db
class TestAuditEventViewSet:
    """Tests for AuditEvent viewset."""

    def test_list_audit_events(self, api_client, user, audit_event):
        """Test listing audit events."""
        api_client.force_authenticate(user=user)
        response = api_client.get('/api/audit/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1


@pytest.mark.django_db
class TestAuditEventViewSetPermissions:
    """Tests for AuditEvent viewset permissions (IsAuthenticated)."""

    def test_list_audit_events_unauthenticated(self, api_client, audit_event):
        """Test that unauthenticated users cannot list audit events."""
        response = api_client.get('/api/audit/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_list_audit_events_admin(self, api_client, admin_user, audit_event):
        """Test that admin can list audit events."""
        api_client.force_authenticate(user=admin_user)
        response = api_client.get('/api/audit/')
        assert response.status_code == status.HTTP_200_OK

    def test_list_audit_events_planner(self, api_client, planner_user, audit_event):
        """Test that planner can list audit events."""
        api_client.force_authenticate(user=planner_user)
        response = api_client.get('/api/audit/')
        assert response.status_code == status.HTTP_200_OK

    def test_list_audit_events_approver(self, api_client, approver_user, audit_event):
        """Test that approver can list audit events."""
        api_client.force_authenticate(user=approver_user)
        response = api_client.get('/api/audit/')
        assert response.status_code == status.HTTP_200_OK

    def test_list_audit_events_viewer(self, api_client, viewer_user, audit_event):
        """Test that viewer can list audit events."""
        api_client.force_authenticate(user=viewer_user)
        response = api_client.get('/api/audit/')
        assert response.status_code == status.HTTP_200_OK

    def test_retrieve_audit_event_unauthenticated(self, api_client, audit_event):
        """Test that unauthenticated users cannot retrieve an audit event."""
        response = api_client.get(f'/api/audit/{audit_event.id}/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_retrieve_audit_event_admin(self, api_client, admin_user, audit_event):
        """Test that admin can retrieve an audit event."""
        api_client.force_authenticate(user=admin_user)
        response = api_client.get(f'/api/audit/{audit_event.id}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['verb'] == 'submitted'

    def test_retrieve_audit_event_planner(self, api_client, planner_user, audit_event):
        """Test that planner can retrieve an audit event."""
        api_client.force_authenticate(user=planner_user)
        response = api_client.get(f'/api/audit/{audit_event.id}/')
        assert response.status_code == status.HTTP_200_OK

    def test_retrieve_audit_event_approver(self, api_client, approver_user, audit_event):
        """Test that approver can retrieve an audit event."""
        api_client.force_authenticate(user=approver_user)
        response = api_client.get(f'/api/audit/{audit_event.id}/')
        assert response.status_code == status.HTTP_200_OK

    def test_retrieve_audit_event_viewer(self, api_client, viewer_user, audit_event):
        """Test that viewer can retrieve an audit event."""
        api_client.force_authenticate(user=viewer_user)
        response = api_client.get(f'/api/audit/{audit_event.id}/')
        assert response.status_code == status.HTTP_200_OK

    def test_audit_is_read_only_post(self, api_client, admin_user):
        """Test that audit events cannot be created via API (read-only viewset)."""
        api_client.force_authenticate(user=admin_user)
        response = api_client.post(
            '/api/audit/',
            {'verb': 'test', 'object_type': 'Test', 'object_id': '1'},
            format='json'
        )
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_audit_is_read_only_put(self, api_client, admin_user, audit_event):
        """Test that audit events cannot be updated via API (read-only viewset)."""
        api_client.force_authenticate(user=admin_user)
        response = api_client.put(
            f'/api/audit/{audit_event.id}/',
            {'verb': 'updated', 'object_type': 'Test', 'object_id': '1'},
            format='json'
        )
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_audit_is_read_only_delete(self, api_client, admin_user, audit_event):
        """Test that audit events cannot be deleted via API (read-only viewset)."""
        api_client.force_authenticate(user=admin_user)
        response = api_client.delete(f'/api/audit/{audit_event.id}/')
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

