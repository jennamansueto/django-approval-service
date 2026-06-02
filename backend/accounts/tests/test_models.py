"""Tests for accounts models."""
import os

import pytest

from accounts.models import User

_TEST_CRED = os.environ.get("DJANGO_TEST_USER_PASS", "testpass123")


@pytest.mark.django_db
class TestUserModel:
    """Tests for User model."""

    def test_create_user(self):
        """Test creating a user with default role."""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password=_TEST_CRED,
        )
        assert user.username == 'testuser'
        assert user.email == 'test@example.com'
        assert user.role == User.VIEWER  # default role

    def test_create_user_with_role(self):
        """Test creating a user with specific role."""
        user = User.objects.create_user(
            username='planner',
            email='planner@example.com',
            password=_TEST_CRED,
            role=User.PLANNER,
        )
        assert user.role == User.PLANNER

    def test_user_str(self):
        """Test user string representation."""
        user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password=_TEST_CRED,
            role=User.ADMIN,
        )
        assert str(user) == 'admin (ADMIN)'
