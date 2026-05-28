"""Tests for accounts models."""
import pytest

from accounts.models import User
from conftest import get_test_user_defaults


@pytest.mark.django_db
class TestUserModel:
    """Tests for User model."""

    def test_create_user(self):
        """Test creating a user with default role."""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            **get_test_user_defaults(),
        )
        assert user.username == 'testuser'
        assert user.email == 'test@example.com'
        assert user.role == User.VIEWER  # default role

    def test_create_user_with_role(self):
        """Test creating a user with specific role."""
        user = User.objects.create_user(
            username='planner',
            email='planner@example.com',
            role=User.PLANNER,
            **get_test_user_defaults(),
        )
        assert user.role == User.PLANNER

    def test_user_str(self):
        """Test user string representation."""
        user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            role=User.ADMIN,
            **get_test_user_defaults(),
        )
        assert str(user) == 'admin (ADMIN)'
