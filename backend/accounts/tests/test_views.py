"""Tests for accounts views."""
import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from accounts.models import User
from conftest import get_test_user_defaults


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
        role=User.PLANNER,
        **get_test_user_defaults(),
    )


@pytest.mark.django_db
class TestLoginView:
    """Tests for login endpoint."""

    def test_login_success(self, api_client, user):
        """Test successful login."""
        response = api_client.post(
            reverse('accounts:login'),
            {'username': 'testuser', **get_test_user_defaults()},
            format='json',
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data['username'] == 'testuser'
        assert response.data['role'] == 'PLANNER'
