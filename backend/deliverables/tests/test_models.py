"""Tests for deliverables models."""
import pytest

from accounts.models import User
from clients.models import Client
from deliverables.models import Deliverable


@pytest.fixture
def user():
    """Create a test user."""
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123',
    )


@pytest.fixture
def client_obj():
    """Create a test client."""
    return Client.objects.create(name='Test Client')


@pytest.mark.django_db
class TestDeliverableModel:
    """Tests for Deliverable model."""

    def test_create_deliverable(self, user, client_obj):
        """Test creating a deliverable."""
        deliverable = Deliverable.objects.create(
            title='Q1 Report',
            description='Quarterly report',
            client=client_obj,
            created_by=user,
        )
        assert deliverable.title == 'Q1 Report'
        assert deliverable.status == Deliverable.Status.DRAFT

    def test_deliverable_str(self, user, client_obj):
        """Test deliverable string representation."""
        deliverable = Deliverable.objects.create(
            title='Test Report',
            client=client_obj,
            created_by=user,
        )
        assert str(deliverable) == 'Test Report (DRAFT)'
