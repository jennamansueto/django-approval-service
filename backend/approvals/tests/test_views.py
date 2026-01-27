"""Tests for approvals views."""
import pytest
from rest_framework import status
from rest_framework.test import APIClient

from accounts.models import User
from approvals.models import ApprovalRequest, ApprovalStep
from clients.models import Client
from deliverables.models import Deliverable


@pytest.fixture
def api_client():
    """Return API client."""
    return APIClient()


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
def approver_user():
    """Create an approver user."""
    return User.objects.create_user(
        username='approver',
        email='approver@example.com',
        password='testpass123',
        role=User.APPROVER,
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
def viewer_user():
    """Create a viewer user."""
    return User.objects.create_user(
        username='viewer',
        email='viewer@example.com',
        password='testpass123',
        role=User.VIEWER,
    )


@pytest.fixture
def client_obj():
    """Create a test client."""
    return Client.objects.create(name='Test Client')


@pytest.fixture
def deliverable(client_obj, planner_user):
    """Create a submitted deliverable."""
    return Deliverable.objects.create(
        title='Test Deliverable',
        client=client_obj,
        created_by=planner_user,
        status=Deliverable.SUBMITTED,
    )


@pytest.fixture
def approval_request(deliverable, planner_user):
    """Create an approval request with a step."""
    request = ApprovalRequest.objects.create(
        deliverable=deliverable,
        requested_by=planner_user,
    )
    ApprovalStep.objects.create(
        approval_request=request,
        step_order=1,
        assigned_role=ApprovalStep.ROLE_APPROVER,
    )
    return request


@pytest.mark.django_db
class TestApprovalRequestViewSet:
    """Tests for ApprovalRequest viewset."""

    def test_list_approvals(self, api_client, approver_user, approval_request):
        """Test listing approval requests."""
        api_client.force_authenticate(user=approver_user)
        response = api_client.get('/api/approvals/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1


@pytest.mark.django_db
class TestApprovalPermissions:
    """Tests for approval request permission enforcement."""

    def test_admin_can_approve(self, api_client, admin_user, approval_request):
        """Test that ADMIN role can approve approval requests."""
        api_client.force_authenticate(user=admin_user)
        response = api_client.post(f'/api/approvals/{approval_request.id}/approve/')
        assert response.status_code == status.HTTP_200_OK

    def test_admin_can_reject(
        self, api_client, admin_user, planner_user, client_obj
    ):
        """Test that ADMIN role can reject approval requests."""
        deliverable = Deliverable.objects.create(
            title='Test Deliverable for Reject',
            client=client_obj,
            created_by=planner_user,
            status=Deliverable.SUBMITTED,
        )
        request = ApprovalRequest.objects.create(
            deliverable=deliverable,
            requested_by=planner_user,
        )
        ApprovalStep.objects.create(
            approval_request=request,
            step_order=1,
            assigned_role=ApprovalStep.ROLE_APPROVER,
        )
        api_client.force_authenticate(user=admin_user)
        response = api_client.post(f'/api/approvals/{request.id}/reject/')
        assert response.status_code == status.HTTP_200_OK

    def test_approver_can_approve(self, api_client, approver_user, approval_request):
        """Test that APPROVER role can approve approval requests."""
        api_client.force_authenticate(user=approver_user)
        response = api_client.post(f'/api/approvals/{approval_request.id}/approve/')
        assert response.status_code == status.HTTP_200_OK

    def test_approver_can_reject(
        self, api_client, approver_user, planner_user, client_obj
    ):
        """Test that APPROVER role can reject approval requests."""
        deliverable = Deliverable.objects.create(
            title='Test Deliverable for Approver Reject',
            client=client_obj,
            created_by=planner_user,
            status=Deliverable.SUBMITTED,
        )
        request = ApprovalRequest.objects.create(
            deliverable=deliverable,
            requested_by=planner_user,
        )
        ApprovalStep.objects.create(
            approval_request=request,
            step_order=1,
            assigned_role=ApprovalStep.ROLE_APPROVER,
        )
        api_client.force_authenticate(user=approver_user)
        response = api_client.post(f'/api/approvals/{request.id}/reject/')
        assert response.status_code == status.HTTP_200_OK

    def test_planner_cannot_approve(self, api_client, planner_user, approval_request):
        """Test that PLANNER role cannot approve approval requests."""
        api_client.force_authenticate(user=planner_user)
        response = api_client.post(f'/api/approvals/{approval_request.id}/approve/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_planner_cannot_reject(self, api_client, planner_user, approval_request):
        """Test that PLANNER role cannot reject approval requests."""
        api_client.force_authenticate(user=planner_user)
        response = api_client.post(f'/api/approvals/{approval_request.id}/reject/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_viewer_cannot_approve(self, api_client, viewer_user, approval_request):
        """Test that VIEWER role cannot approve approval requests."""
        api_client.force_authenticate(user=viewer_user)
        response = api_client.post(f'/api/approvals/{approval_request.id}/approve/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_viewer_cannot_reject(self, api_client, viewer_user, approval_request):
        """Test that VIEWER role cannot reject approval requests."""
        api_client.force_authenticate(user=viewer_user)
        response = api_client.post(f'/api/approvals/{approval_request.id}/reject/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_unauthenticated_cannot_approve(self, api_client, approval_request):
        """Test that unauthenticated users cannot approve approval requests."""
        response = api_client.post(f'/api/approvals/{approval_request.id}/approve/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_unauthenticated_cannot_reject(self, api_client, approval_request):
        """Test that unauthenticated users cannot reject approval requests."""
        response = api_client.post(f'/api/approvals/{approval_request.id}/reject/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_viewer_can_list_approvals(self, api_client, viewer_user, approval_request):
        """Test that VIEWER role can list approval requests (read-only access)."""
        api_client.force_authenticate(user=viewer_user)
        response = api_client.get('/api/approvals/')
        assert response.status_code == status.HTTP_200_OK

    def test_viewer_can_retrieve_approval(
        self, api_client, viewer_user, approval_request
    ):
        """Test that VIEWER role can retrieve a single approval request."""
        api_client.force_authenticate(user=viewer_user)
        response = api_client.get(f'/api/approvals/{approval_request.id}/')
        assert response.status_code == status.HTTP_200_OK

