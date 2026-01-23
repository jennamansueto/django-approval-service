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
        role=User.Role.ADMIN,
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

    def test_list_audit_events_unauthenticated(self, api_client, audit_event):
        """Test listing audit events without authentication."""
        response = api_client.get('/api/audit/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_list_audit_events_multiple(self, api_client, user):
        """Test listing multiple audit events."""
        AuditEvent.objects.create(
            actor=user,
            verb='created',
            object_type='Deliverable',
            object_id='1',
        )
        AuditEvent.objects.create(
            actor=user,
            verb='submitted',
            object_type='Deliverable',
            object_id='1',
        )
        AuditEvent.objects.create(
            actor=user,
            verb='approved',
            object_type='ApprovalRequest',
            object_id='1',
        )

        api_client.force_authenticate(user=user)
        response = api_client.get('/api/audit/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 3


@pytest.mark.django_db
class TestAuditEventFiltering:
    """Tests for audit event filtering."""

    def test_filter_by_object_type(self, api_client, user):
        """Test filtering audit events by object_type."""
        AuditEvent.objects.create(
            actor=user,
            verb='submitted',
            object_type='Deliverable',
            object_id='1',
        )
        AuditEvent.objects.create(
            actor=user,
            verb='approved',
            object_type='ApprovalRequest',
            object_id='1',
        )

        api_client.force_authenticate(user=user)

        response = api_client.get('/api/audit/?object_type=Deliverable')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['object_type'] == 'Deliverable'

        response = api_client.get('/api/audit/?object_type=ApprovalRequest')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['object_type'] == 'ApprovalRequest'

    def test_filter_by_object_id(self, api_client, user):
        """Test filtering audit events by object_id."""
        AuditEvent.objects.create(
            actor=user,
            verb='submitted',
            object_type='Deliverable',
            object_id='1',
        )
        AuditEvent.objects.create(
            actor=user,
            verb='submitted',
            object_type='Deliverable',
            object_id='2',
        )

        api_client.force_authenticate(user=user)

        response = api_client.get('/api/audit/?object_id=1')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['object_id'] == '1'

        response = api_client.get('/api/audit/?object_id=2')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['object_id'] == '2'

    def test_filter_by_object_type_and_object_id(self, api_client, user):
        """Test filtering audit events by both object_type and object_id."""
        AuditEvent.objects.create(
            actor=user,
            verb='submitted',
            object_type='Deliverable',
            object_id='1',
        )
        AuditEvent.objects.create(
            actor=user,
            verb='approved',
            object_type='ApprovalRequest',
            object_id='1',
        )
        AuditEvent.objects.create(
            actor=user,
            verb='submitted',
            object_type='Deliverable',
            object_id='2',
        )

        api_client.force_authenticate(user=user)

        response = api_client.get('/api/audit/?object_type=Deliverable&object_id=1')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['object_type'] == 'Deliverable'
        assert response.data[0]['object_id'] == '1'

    def test_filter_no_results(self, api_client, user, audit_event):
        """Test filtering with no matching results."""
        api_client.force_authenticate(user=user)
        response = api_client.get('/api/audit/?object_type=NonExistent')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 0


@pytest.mark.django_db
class TestAuditEventRetrieve:
    """Tests for retrieving a single audit event."""

    def test_retrieve_audit_event(self, api_client, user, audit_event):
        """Test retrieving a single audit event."""
        api_client.force_authenticate(user=user)
        response = api_client.get(f'/api/audit/{audit_event.id}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == audit_event.id
        assert response.data['verb'] == 'submitted'
        assert response.data['object_type'] == 'Deliverable'
        assert response.data['actor_username'] == 'testuser'

    def test_retrieve_audit_event_unauthenticated(self, api_client, audit_event):
        """Test retrieving an audit event without authentication."""
        response = api_client.get(f'/api/audit/{audit_event.id}/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_retrieve_nonexistent_audit_event(self, api_client, user):
        """Test retrieving a non-existent audit event."""
        api_client.force_authenticate(user=user)
        response = api_client.get('/api/audit/99999/')
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestAuditEventReadOnly:
    """Tests to verify audit events are read-only."""

    def test_create_audit_event_not_allowed(self, api_client, user):
        """Test that creating audit events via API is not allowed."""
        api_client.force_authenticate(user=user)
        response = api_client.post(
            '/api/audit/',
            {
                'verb': 'created',
                'object_type': 'Deliverable',
                'object_id': '1',
            },
            format='json',
        )
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_update_audit_event_not_allowed(self, api_client, user, audit_event):
        """Test that updating audit events via API is not allowed."""
        api_client.force_authenticate(user=user)
        response = api_client.put(
            f'/api/audit/{audit_event.id}/',
            {
                'verb': 'updated',
                'object_type': 'Deliverable',
                'object_id': '1',
            },
            format='json',
        )
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_partial_update_audit_event_not_allowed(self, api_client, user, audit_event):
        """Test that partial update of audit events via API is not allowed."""
        api_client.force_authenticate(user=user)
        response = api_client.patch(
            f'/api/audit/{audit_event.id}/',
            {'verb': 'patched'},
            format='json',
        )
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_delete_audit_event_not_allowed(self, api_client, user, audit_event):
        """Test that deleting audit events via API is not allowed."""
        api_client.force_authenticate(user=user)
        response = api_client.delete(f'/api/audit/{audit_event.id}/')
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

        assert AuditEvent.objects.filter(id=audit_event.id).exists()

