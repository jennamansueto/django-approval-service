"""Tests for approvals models."""
import os

import pytest

from accounts.models import User
from approvals.models import ApprovalRequest, ApprovalStep
from clients.models import Client
from deliverables.models import Deliverable

TEST_USER_PASSWORD = os.environ.get('TEST_USER_PASSWORD', 'testpass123')


@pytest.fixture
def user():
    """Create a test user."""
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password=TEST_USER_PASSWORD,
    )


@pytest.fixture
def client_obj():
    """Create a test client."""
    return Client.objects.create(name='Test Client')


@pytest.fixture
def deliverable(client_obj, user):
    """Create a test deliverable."""
    return Deliverable.objects.create(
        title='Test Deliverable',
        client=client_obj,
        created_by=user,
    )


@pytest.mark.django_db
class TestApprovalRequestModel:
    """Tests for ApprovalRequest model."""

    def test_create_approval_request(self, deliverable, user):
        """Test creating an approval request."""
        request = ApprovalRequest.objects.create(
            deliverable=deliverable,
            requested_by=user,
        )
        assert request.status == ApprovalRequest.PENDING
        assert request.deliverable == deliverable

    def test_approval_request_str(self, deliverable, user):
        """Test approval request string representation."""
        request = ApprovalRequest.objects.create(
            deliverable=deliverable,
            requested_by=user,
        )
        assert 'Test Deliverable' in str(request)
        assert 'PENDING' in str(request)
