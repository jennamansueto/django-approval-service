"""Tests for audit models."""
import os

import pytest

from accounts.models import User
from audit.models import AuditEvent

TEST_PASSWORD = os.environ.get("DJANGO_TEST_PASSWORD", "testpass123")


@pytest.fixture
def user():
    """Create a test user."""
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password=TEST_PASSWORD,
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

