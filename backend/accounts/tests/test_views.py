"""Tests for accounts views."""
import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from accounts.models import User


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
        role=User.PLANNER,
    )


@pytest.fixture
def admin_user():
    """Create an admin user."""
    return User.objects.create_user(
        username='admin',
        email='admin@example.com',
        password='adminpass123',
        role=User.Role.ADMIN,
    )


@pytest.fixture
def approver_user():
    """Create an approver user."""
    return User.objects.create_user(
        username='approver',
        email='approver@example.com',
        password='approverpass123',
        role=User.Role.APPROVER,
    )


@pytest.fixture
def viewer_user():
    """Create a viewer user."""
    return User.objects.create_user(
        username='viewer',
        email='viewer@example.com',
        password='viewerpass123',
        role=User.Role.VIEWER,
    )


@pytest.mark.django_db
class TestLoginView:
    """Tests for login endpoint."""

    def test_login_success(self, api_client, user):
        """Test successful login."""
        response = api_client.post(
            reverse('accounts:login'),
            {'username': 'testuser', 'password': 'testpass123'},
            format='json',
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data['username'] == 'testuser'
        assert response.data['role'] == 'PLANNER'

    def test_login_invalid_password(self, api_client, user):
        """Test login with wrong password."""
        response = api_client.post(
            reverse('login'),
            {'username': 'testuser', 'password': 'wrongpassword'},
            format='json',
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert 'error' in response.data
        assert response.data['error'] == 'Invalid credentials'

    def test_login_nonexistent_user(self, api_client):
        """Test login with non-existent user."""
        response = api_client.post(
            reverse('login'),
            {'username': 'nonexistent', 'password': 'somepassword'},
            format='json',
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert 'error' in response.data

    def test_login_missing_username(self, api_client):
        """Test login with missing username."""
        response = api_client.post(
            reverse('login'),
            {'password': 'testpass123'},
            format='json',
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_login_missing_password(self, api_client):
        """Test login with missing password."""
        response = api_client.post(
            reverse('login'),
            {'username': 'testuser'},
            format='json',
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_login_empty_credentials(self, api_client):
        """Test login with empty credentials."""
        response = api_client.post(
            reverse('login'),
            {},
            format='json',
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestLogoutView:
    """Tests for logout endpoint."""

    def test_logout_success(self, api_client, user):
        """Test successful logout."""
        api_client.force_authenticate(user=user)
        response = api_client.post(reverse('logout'))
        assert response.status_code == status.HTTP_200_OK
        assert response.data['message'] == 'Logged out successfully'

    def test_logout_unauthenticated(self, api_client):
        """Test logout without authentication."""
        response = api_client.post(reverse('logout'))
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestMeView:
    """Tests for me endpoint."""

    def test_me_authenticated(self, api_client, user):
        """Test getting current user info when authenticated."""
        api_client.force_authenticate(user=user)
        response = api_client.get(reverse('me'))
        assert response.status_code == status.HTTP_200_OK
        assert response.data['username'] == 'testuser'
        assert response.data['email'] == 'test@example.com'
        assert response.data['role'] == 'PLANNER'

    def test_me_unauthenticated(self, api_client):
        """Test getting current user info without authentication."""
        response = api_client.get(reverse('me'))
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_me_returns_correct_role_admin(self, api_client, admin_user):
        """Test me endpoint returns correct role for admin."""
        api_client.force_authenticate(user=admin_user)
        response = api_client.get(reverse('me'))
        assert response.status_code == status.HTTP_200_OK
        assert response.data['role'] == 'ADMIN'

    def test_me_returns_correct_role_approver(self, api_client, approver_user):
        """Test me endpoint returns correct role for approver."""
        api_client.force_authenticate(user=approver_user)
        response = api_client.get(reverse('me'))
        assert response.status_code == status.HTTP_200_OK
        assert response.data['role'] == 'APPROVER'

    def test_me_returns_correct_role_viewer(self, api_client, viewer_user):
        """Test me endpoint returns correct role for viewer."""
        api_client.force_authenticate(user=viewer_user)
        response = api_client.get(reverse('me'))
        assert response.status_code == status.HTTP_200_OK
        assert response.data['role'] == 'VIEWER'

