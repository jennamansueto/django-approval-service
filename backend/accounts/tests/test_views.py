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
        password='testpass123',
        role=User.ADMIN,
    )


@pytest.fixture
def planner_user():
    """Create a planner user."""
    return User.objects.create_user(
        username='planner',
        email='planner@example.com',
        password='testpass123',
        role=User.PLANNER,
    )


@pytest.fixture
def approver_user():
    """Create an approver user."""
    return User.objects.create_user(
        username='approver',
        email='approver@example.com',
        password='testpass123',
        role=User.APPROVER,
    )


@pytest.fixture
def viewer_user():
    """Create a viewer user."""
    return User.objects.create_user(
        username='viewer',
        email='viewer@example.com',
        password='testpass123',
        role=User.VIEWER,
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

    def test_login_invalid_credentials(self, api_client, user):
        """Test login with invalid credentials."""
        response = api_client.post(
            reverse('accounts:login'),
            {'username': 'testuser', 'password': 'wrongpassword'},
            format='json',
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_login_allows_unauthenticated(self, api_client):
        """Test that login endpoint allows unauthenticated access."""
        response = api_client.post(
            reverse('accounts:login'),
            {'username': 'nonexistent', 'password': 'password'},
            format='json',
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestLogoutView:
    """Tests for logout endpoint."""

    def test_logout_unauthenticated(self, api_client):
        """Test that logout requires authentication."""
        response = api_client.post(reverse('accounts:logout'))
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_logout_admin(self, api_client, admin_user):
        """Test that admin can logout."""
        api_client.force_authenticate(user=admin_user)
        response = api_client.post(reverse('accounts:logout'))
        assert response.status_code == status.HTTP_200_OK

    def test_logout_planner(self, api_client, planner_user):
        """Test that planner can logout."""
        api_client.force_authenticate(user=planner_user)
        response = api_client.post(reverse('accounts:logout'))
        assert response.status_code == status.HTTP_200_OK

    def test_logout_approver(self, api_client, approver_user):
        """Test that approver can logout."""
        api_client.force_authenticate(user=approver_user)
        response = api_client.post(reverse('accounts:logout'))
        assert response.status_code == status.HTTP_200_OK

    def test_logout_viewer(self, api_client, viewer_user):
        """Test that viewer can logout."""
        api_client.force_authenticate(user=viewer_user)
        response = api_client.post(reverse('accounts:logout'))
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestMeView:
    """Tests for me endpoint."""

    def test_me_unauthenticated(self, api_client):
        """Test that me endpoint requires authentication."""
        response = api_client.get(reverse('accounts:me'))
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_me_admin(self, api_client, admin_user):
        """Test that admin can access me endpoint."""
        api_client.force_authenticate(user=admin_user)
        response = api_client.get(reverse('accounts:me'))
        assert response.status_code == status.HTTP_200_OK
        assert response.data['username'] == 'admin'
        assert response.data['role'] == 'ADMIN'

    def test_me_planner(self, api_client, planner_user):
        """Test that planner can access me endpoint."""
        api_client.force_authenticate(user=planner_user)
        response = api_client.get(reverse('accounts:me'))
        assert response.status_code == status.HTTP_200_OK
        assert response.data['username'] == 'planner'
        assert response.data['role'] == 'PLANNER'

    def test_me_approver(self, api_client, approver_user):
        """Test that approver can access me endpoint."""
        api_client.force_authenticate(user=approver_user)
        response = api_client.get(reverse('accounts:me'))
        assert response.status_code == status.HTTP_200_OK
        assert response.data['username'] == 'approver'
        assert response.data['role'] == 'APPROVER'

    def test_me_viewer(self, api_client, viewer_user):
        """Test that viewer can access me endpoint."""
        api_client.force_authenticate(user=viewer_user)
        response = api_client.get(reverse('accounts:me'))
        assert response.status_code == status.HTTP_200_OK
        assert response.data['username'] == 'viewer'
        assert response.data['role'] == 'VIEWER'

