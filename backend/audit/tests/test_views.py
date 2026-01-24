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

    def test_unauthenticated_cannot_list_audit_events(self, api_client, audit_event):
        """Test unauthenticated user cannot list audit events."""
        response = api_client.get('/api/audit/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_unauthenticated_cannot_retrieve_audit_event(self, api_client, audit_event):
        """Test unauthenticated user cannot retrieve audit event."""
        response = api_client.get(f'/api/audit/{audit_event.id}/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_viewer_can_list_audit_events(self, api_client, viewer_user, audit_event):
        """Test VIEWER role can list audit events."""
        api_client.force_authenticate(user=viewer_user)
        response = api_client.get('/api/audit/')
        assert response.status_code == status.HTTP_200_OK

    def test_planner_can_list_audit_events(self, api_client, planner_user, audit_event):
        """Test PLANNER role can list audit events."""
        api_client.force_authenticate(user=planner_user)
        response = api_client.get('/api/audit/')
        assert response.status_code == status.HTTP_200_OK

    def test_approver_can_list_audit_events(self, api_client, approver_user, audit_event):
        """Test APPROVER role can list audit events."""
        api_client.force_authenticate(user=approver_user)
        response = api_client.get('/api/audit/')
        assert response.status_code == status.HTTP_200_OK

    def test_admin_can_list_audit_events(self, api_client, admin_user, audit_event):
        """Test ADMIN role can list audit events."""
        api_client.force_authenticate(user=admin_user)
        response = api_client.get('/api/audit/')
        assert response.status_code == status.HTTP_200_OK

    def test_viewer_can_retrieve_audit_event(self, api_client, viewer_user, audit_event):
        """Test VIEWER role can retrieve audit event."""
        api_client.force_authenticate(user=viewer_user)
        response = api_client.get(f'/api/audit/{audit_event.id}/')
        assert response.status_code == status.HTTP_200_OK

    def test_audit_is_read_only(self, api_client, admin_user, audit_event):
        """Test audit endpoint is read-only (no POST allowed)."""
        api_client.force_authenticate(user=admin_user)
        response = api_client.post('/api/audit/', {
            'verb': 'test',
            'object_type': 'Test',
            'object_id': '1',
        })
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_audit_cannot_be_updated(self, api_client, admin_user, audit_event):
        """Test audit events cannot be updated."""
        api_client.force_authenticate(user=admin_user)
        response = api_client.put(f'/api/audit/{audit_event.id}/', {
            'verb': 'updated',
            'object_type': 'Test',
            'object_id': '1',
        })
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_audit_cannot_be_deleted(self, api_client, admin_user, audit_event):
        """Test audit events cannot be deleted."""
        api_client.force_authenticate(user=admin_user)
        response = api_client.delete(f'/api/audit/{audit_event.id}/')
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

