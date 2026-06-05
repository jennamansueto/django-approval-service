"""Tests for audit views."""
import os

import pytest
from rest_framework import status
from rest_framework.test import APIClient

from accounts.models import User
from audit.models import AuditEvent

TEST_PASSWORD = os.environ.get("DJANGO_TEST_PASSWORD", "testpass123")


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
        password=TEST_PASSWORD,
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

