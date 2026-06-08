"""Tests for accounts models."""
import pytest

from accounts.models import User


@pytest.mark.django_db
class TestUserModel:
    """Tests for User model."""

    def test_create_user(self, test_user_password):
        """Test creating a user with default role."""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password=test_user_password,
        )
        assert user.username == 'testuser'
        assert user.email == 'test@example.com'
        assert user.role == User.VIEWER  # default role

    def test_create_user_with_role(self, test_user_password):
        """Test creating a user with specific role."""
        user = User.objects.create_user(
            username='planner',
            email='planner@example.com',
            password=test_user_password,
            role=User.PLANNER,
        )
        assert user.role == User.PLANNER

    def test_user_str(self, test_user_password):
        """Test user string representation."""
        user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password=test_user_password,
            role=User.ADMIN,
        )
        assert str(user) == 'admin (ADMIN)'
