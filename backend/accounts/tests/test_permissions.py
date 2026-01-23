"""Tests for accounts permission classes."""
import pytest
from rest_framework.test import APIRequestFactory

from accounts.models import User
from accounts.permissions import (
    IsAdminUser,
    IsAdminOrPlanner,
    IsAdminOrApprover,
    IsViewerOrAbove,
)


@pytest.fixture
def request_factory():
    """Return API request factory."""
    return APIRequestFactory()


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
def planner_user():
    """Create a planner user."""
    return User.objects.create_user(
        username='planner',
        email='planner@example.com',
        password='plannerpass123',
        role=User.Role.PLANNER,
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
class TestIsAdminUser:
    """Tests for IsAdminUser permission class."""

    def test_admin_has_permission(self, request_factory, admin_user):
        """Test that admin user has permission."""
        request = request_factory.get('/')
        request.user = admin_user
        permission = IsAdminUser()
        assert permission.has_permission(request, None) is True

    def test_planner_denied(self, request_factory, planner_user):
        """Test that planner user is denied."""
        request = request_factory.get('/')
        request.user = planner_user
        permission = IsAdminUser()
        assert permission.has_permission(request, None) is False

    def test_approver_denied(self, request_factory, approver_user):
        """Test that approver user is denied."""
        request = request_factory.get('/')
        request.user = approver_user
        permission = IsAdminUser()
        assert permission.has_permission(request, None) is False

    def test_viewer_denied(self, request_factory, viewer_user):
        """Test that viewer user is denied."""
        request = request_factory.get('/')
        request.user = viewer_user
        permission = IsAdminUser()
        assert permission.has_permission(request, None) is False

    def test_unauthenticated_denied(self, request_factory):
        """Test that unauthenticated user is denied."""
        from django.contrib.auth.models import AnonymousUser
        request = request_factory.get('/')
        request.user = AnonymousUser()
        permission = IsAdminUser()
        assert permission.has_permission(request, None) is False


@pytest.mark.django_db
class TestIsAdminOrPlanner:
    """Tests for IsAdminOrPlanner permission class."""

    def test_admin_has_permission(self, request_factory, admin_user):
        """Test that admin user has permission."""
        request = request_factory.get('/')
        request.user = admin_user
        permission = IsAdminOrPlanner()
        assert permission.has_permission(request, None) is True

    def test_planner_has_permission(self, request_factory, planner_user):
        """Test that planner user has permission."""
        request = request_factory.get('/')
        request.user = planner_user
        permission = IsAdminOrPlanner()
        assert permission.has_permission(request, None) is True

    def test_approver_denied(self, request_factory, approver_user):
        """Test that approver user is denied."""
        request = request_factory.get('/')
        request.user = approver_user
        permission = IsAdminOrPlanner()
        assert permission.has_permission(request, None) is False

    def test_viewer_denied(self, request_factory, viewer_user):
        """Test that viewer user is denied."""
        request = request_factory.get('/')
        request.user = viewer_user
        permission = IsAdminOrPlanner()
        assert permission.has_permission(request, None) is False

    def test_unauthenticated_denied(self, request_factory):
        """Test that unauthenticated user is denied."""
        from django.contrib.auth.models import AnonymousUser
        request = request_factory.get('/')
        request.user = AnonymousUser()
        permission = IsAdminOrPlanner()
        assert permission.has_permission(request, None) is False


@pytest.mark.django_db
class TestIsAdminOrApprover:
    """Tests for IsAdminOrApprover permission class."""

    def test_admin_has_permission(self, request_factory, admin_user):
        """Test that admin user has permission."""
        request = request_factory.get('/')
        request.user = admin_user
        permission = IsAdminOrApprover()
        assert permission.has_permission(request, None) is True

    def test_approver_has_permission(self, request_factory, approver_user):
        """Test that approver user has permission."""
        request = request_factory.get('/')
        request.user = approver_user
        permission = IsAdminOrApprover()
        assert permission.has_permission(request, None) is True

    def test_planner_denied(self, request_factory, planner_user):
        """Test that planner user is denied."""
        request = request_factory.get('/')
        request.user = planner_user
        permission = IsAdminOrApprover()
        assert permission.has_permission(request, None) is False

    def test_viewer_denied(self, request_factory, viewer_user):
        """Test that viewer user is denied."""
        request = request_factory.get('/')
        request.user = viewer_user
        permission = IsAdminOrApprover()
        assert permission.has_permission(request, None) is False

    def test_unauthenticated_denied(self, request_factory):
        """Test that unauthenticated user is denied."""
        from django.contrib.auth.models import AnonymousUser
        request = request_factory.get('/')
        request.user = AnonymousUser()
        permission = IsAdminOrApprover()
        assert permission.has_permission(request, None) is False


@pytest.mark.django_db
class TestIsViewerOrAbove:
    """Tests for IsViewerOrAbove permission class."""

    def test_admin_has_permission(self, request_factory, admin_user):
        """Test that admin user has permission."""
        request = request_factory.get('/')
        request.user = admin_user
        permission = IsViewerOrAbove()
        assert permission.has_permission(request, None) is True

    def test_planner_has_permission(self, request_factory, planner_user):
        """Test that planner user has permission."""
        request = request_factory.get('/')
        request.user = planner_user
        permission = IsViewerOrAbove()
        assert permission.has_permission(request, None) is True

    def test_approver_has_permission(self, request_factory, approver_user):
        """Test that approver user has permission."""
        request = request_factory.get('/')
        request.user = approver_user
        permission = IsViewerOrAbove()
        assert permission.has_permission(request, None) is True

    def test_viewer_has_permission(self, request_factory, viewer_user):
        """Test that viewer user has permission."""
        request = request_factory.get('/')
        request.user = viewer_user
        permission = IsViewerOrAbove()
        assert permission.has_permission(request, None) is True

    def test_unauthenticated_denied(self, request_factory):
        """Test that unauthenticated user is denied."""
        from django.contrib.auth.models import AnonymousUser
        request = request_factory.get('/')
        request.user = AnonymousUser()
        permission = IsViewerOrAbove()
        assert permission.has_permission(request, None) is False
