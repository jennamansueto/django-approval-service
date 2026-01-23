"""Tests for audit models."""
import pytest

from accounts.models import User
from audit.models import AuditEvent


@pytest.fixture
def user():
    """Create a test user."""
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123',
    )


@pytest.mark.django_db
class TestAuditEventModel:
    """Tests for AuditEvent model."""

    def test_create_audit_event(self, user):
        """Test creating an audit event."""
        event = AuditEvent.objects.create(
            actor=user,
            verb='created',
            object_type='Deliverable',
            object_id='1',
            payload={'title': 'Test'},
        )
        assert event.verb == 'created'
        assert event.object_type == 'Deliverable'

    def test_audit_event_str(self, user):
        """Test audit event string representation."""
        event = AuditEvent.objects.create(
            actor=user,
            verb='submitted',
            object_type='Deliverable',
            object_id='42',
        )
        assert 'testuser' in str(event)
        assert 'submitted' in str(event)
        assert 'Deliverable' in str(event)
        assert '42' in str(event)

    def test_audit_event_created_at(self, user):
        """Test that created_at is set automatically."""
        event = AuditEvent.objects.create(
            actor=user,
            verb='created',
            object_type='Deliverable',
            object_id='1',
        )
        assert event.created_at is not None

    def test_audit_event_default_payload(self, user):
        """Test that default payload is empty dict."""
        event = AuditEvent.objects.create(
            actor=user,
            verb='created',
            object_type='Deliverable',
            object_id='1',
        )
        assert event.payload == {}

    def test_audit_event_with_payload(self, user):
        """Test audit event with payload."""
        payload = {'title': 'Test Deliverable', 'status': 'SUBMITTED'}
        event = AuditEvent.objects.create(
            actor=user,
            verb='submitted',
            object_type='Deliverable',
            object_id='1',
            payload=payload,
        )
        assert event.payload == payload
        assert event.payload['title'] == 'Test Deliverable'
        assert event.payload['status'] == 'SUBMITTED'

    def test_audit_event_null_actor(self):
        """Test audit event with null actor (deleted user)."""
        event = AuditEvent.objects.create(
            actor=None,
            verb='system_action',
            object_type='System',
            object_id='1',
        )
        assert event.actor is None

    def test_audit_event_ordering(self, user):
        """Test that audit events are ordered by created_at descending."""
        event1 = AuditEvent.objects.create(
            actor=user,
            verb='first',
            object_type='Deliverable',
            object_id='1',
        )
        event2 = AuditEvent.objects.create(
            actor=user,
            verb='second',
            object_type='Deliverable',
            object_id='1',
        )
        event3 = AuditEvent.objects.create(
            actor=user,
            verb='third',
            object_type='Deliverable',
            object_id='1',
        )

        events = list(AuditEvent.objects.all())
        assert events[0].verb == 'third'
        assert events[1].verb == 'second'
        assert events[2].verb == 'first'

