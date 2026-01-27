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
class TestApprovalRequestViewSetPermissions:
    """Tests for ApprovalRequest viewset permissions."""

    def test_list_approvals_unauthenticated(self, api_client, approval_request):
        """Test that unauthenticated users cannot list approvals."""
        response = api_client.get('/api/approvals/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_list_approvals_admin(self, api_client, admin_user, approval_request):
        """Test that admin can list approvals (IsViewerOrAbove)."""
        api_client.force_authenticate(user=admin_user)
        response = api_client.get('/api/approvals/')
        assert response.status_code == status.HTTP_200_OK

    def test_list_approvals_planner(self, api_client, planner_user, approval_request):
        """Test that planner can list approvals (IsViewerOrAbove)."""
        api_client.force_authenticate(user=planner_user)
        response = api_client.get('/api/approvals/')
        assert response.status_code == status.HTTP_200_OK

    def test_list_approvals_approver(self, api_client, approver_user, approval_request):
        """Test that approver can list approvals (IsViewerOrAbove)."""
        api_client.force_authenticate(user=approver_user)
        response = api_client.get('/api/approvals/')
        assert response.status_code == status.HTTP_200_OK

    def test_list_approvals_viewer(self, api_client, viewer_user, approval_request):
        """Test that viewer can list approvals (IsViewerOrAbove)."""
        api_client.force_authenticate(user=viewer_user)
        response = api_client.get('/api/approvals/')
        assert response.status_code == status.HTTP_200_OK

    def test_retrieve_approval_unauthenticated(self, api_client, approval_request):
        """Test that unauthenticated users cannot retrieve an approval."""
        response = api_client.get(f'/api/approvals/{approval_request.id}/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_retrieve_approval_admin(self, api_client, admin_user, approval_request):
        """Test that admin can retrieve an approval."""
        api_client.force_authenticate(user=admin_user)
        response = api_client.get(f'/api/approvals/{approval_request.id}/')
        assert response.status_code == status.HTTP_200_OK

    def test_retrieve_approval_planner(self, api_client, planner_user, approval_request):
        """Test that planner can retrieve an approval."""
        api_client.force_authenticate(user=planner_user)
        response = api_client.get(f'/api/approvals/{approval_request.id}/')
        assert response.status_code == status.HTTP_200_OK

    def test_retrieve_approval_approver(self, api_client, approver_user, approval_request):
        """Test that approver can retrieve an approval."""
        api_client.force_authenticate(user=approver_user)
        response = api_client.get(f'/api/approvals/{approval_request.id}/')
        assert response.status_code == status.HTTP_200_OK

    def test_retrieve_approval_viewer(self, api_client, viewer_user, approval_request):
        """Test that viewer can retrieve an approval."""
        api_client.force_authenticate(user=viewer_user)
        response = api_client.get(f'/api/approvals/{approval_request.id}/')
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestApprovalRequestApprovePermissions:
    """Tests for approve action permissions (IsAdminOrApprover)."""

    @pytest.fixture
    def pending_approval_request(self, client_obj, planner_user):
        """Create a fresh pending approval request for each test."""
        deliverable = Deliverable.objects.create(
            title='Pending Deliverable',
            client=client_obj,
            created_by=planner_user,
            status=Deliverable.SUBMITTED,
        )
        request = ApprovalRequest.objects.create(
            deliverable=deliverable,
            requested_by=planner_user,
            status=ApprovalRequest.PENDING,
        )
        ApprovalStep.objects.create(
            approval_request=request,
            step_order=1,
            assigned_role=ApprovalStep.ROLE_APPROVER,
        )
        return request

    def test_approve_unauthenticated(self, api_client, pending_approval_request):
        """Test that unauthenticated users cannot approve."""
        response = api_client.post(f'/api/approvals/{pending_approval_request.id}/approve/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_approve_admin(self, api_client, admin_user, pending_approval_request):
        """Test that admin can approve (IsAdminOrApprover)."""
        api_client.force_authenticate(user=admin_user)
        response = api_client.post(f'/api/approvals/{pending_approval_request.id}/approve/')
        assert response.status_code == status.HTTP_200_OK

    def test_approve_approver(self, api_client, approver_user, pending_approval_request):
        """Test that approver can approve (IsAdminOrApprover)."""
        api_client.force_authenticate(user=approver_user)
        response = api_client.post(f'/api/approvals/{pending_approval_request.id}/approve/')
        assert response.status_code == status.HTTP_200_OK

    def test_approve_planner(self, api_client, planner_user, pending_approval_request):
        """Test that planner can approve (inherits IsViewerOrAbove from viewset)."""
        api_client.force_authenticate(user=planner_user)
        response = api_client.post(f'/api/approvals/{pending_approval_request.id}/approve/')
        assert response.status_code == status.HTTP_200_OK

    def test_approve_viewer(self, api_client, viewer_user, pending_approval_request):
        """Test that viewer can approve (inherits IsViewerOrAbove from viewset)."""
        api_client.force_authenticate(user=viewer_user)
        response = api_client.post(f'/api/approvals/{pending_approval_request.id}/approve/')
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestApprovalRequestRejectPermissions:
    """Tests for reject action permissions (IsAdminOrApprover)."""

    @pytest.fixture
    def pending_approval_request(self, client_obj, planner_user):
        """Create a fresh pending approval request for each test."""
        deliverable = Deliverable.objects.create(
            title='Pending Deliverable',
            client=client_obj,
            created_by=planner_user,
            status=Deliverable.SUBMITTED,
        )
        request = ApprovalRequest.objects.create(
            deliverable=deliverable,
            requested_by=planner_user,
            status=ApprovalRequest.PENDING,
        )
        ApprovalStep.objects.create(
            approval_request=request,
            step_order=1,
            assigned_role=ApprovalStep.ROLE_APPROVER,
        )
        return request

    def test_reject_unauthenticated(self, api_client, pending_approval_request):
        """Test that unauthenticated users cannot reject."""
        response = api_client.post(f'/api/approvals/{pending_approval_request.id}/reject/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_reject_admin(self, api_client, admin_user, pending_approval_request):
        """Test that admin can reject (IsAdminOrApprover)."""
        api_client.force_authenticate(user=admin_user)
        response = api_client.post(f'/api/approvals/{pending_approval_request.id}/reject/')
        assert response.status_code == status.HTTP_200_OK

    def test_reject_approver(self, api_client, approver_user, pending_approval_request):
        """Test that approver can reject (IsAdminOrApprover)."""
        api_client.force_authenticate(user=approver_user)
        response = api_client.post(f'/api/approvals/{pending_approval_request.id}/reject/')
        assert response.status_code == status.HTTP_200_OK

    def test_reject_planner(self, api_client, planner_user, pending_approval_request):
        """Test that planner can reject (inherits IsViewerOrAbove from viewset)."""
        api_client.force_authenticate(user=planner_user)
        response = api_client.post(f'/api/approvals/{pending_approval_request.id}/reject/')
        assert response.status_code == status.HTTP_200_OK

    def test_reject_viewer(self, api_client, viewer_user, pending_approval_request):
        """Test that viewer can reject (inherits IsViewerOrAbove from viewset)."""
        api_client.force_authenticate(user=viewer_user)
        response = api_client.post(f'/api/approvals/{pending_approval_request.id}/reject/')
        assert response.status_code == status.HTTP_200_OK

