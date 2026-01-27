"""Tests for approvals views."""
import pytest
from rest_framework import status
from rest_framework.test import APIClient

from accounts.models import User
from approvals.models import ApprovalRequest, ApprovalStep
from audit.models import AuditEvent
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
        role=User.Role.ADMIN,
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
        role=User.Role.VIEWER,
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

    def test_list_approvals_unauthenticated(self, api_client, approval_request):
        """Test listing approval requests without authentication."""
        response = api_client.get('/api/approvals/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_list_approvals_with_status_filter(
        self, api_client, approver_user, client_obj, planner_user
    ):
        """Test filtering approval requests by status."""
        deliverable1 = Deliverable.objects.create(
            title='Deliverable 1',
            client=client_obj,
            created_by=planner_user,
            status=Deliverable.Status.SUBMITTED,
        )
        deliverable2 = Deliverable.objects.create(
            title='Deliverable 2',
            client=client_obj,
            created_by=planner_user,
            status=Deliverable.Status.APPROVED,
        )
        ApprovalRequest.objects.create(
            deliverable=deliverable1,
            requested_by=planner_user,
            status=ApprovalRequest.Status.PENDING,
        )
        ApprovalRequest.objects.create(
            deliverable=deliverable2,
            requested_by=planner_user,
            status=ApprovalRequest.Status.APPROVED,
        )

        api_client.force_authenticate(user=approver_user)

        response = api_client.get('/api/approvals/?status=PENDING')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['status'] == 'PENDING'

        response = api_client.get('/api/approvals/?status=APPROVED')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['status'] == 'APPROVED'

    def test_retrieve_approval_request(self, api_client, approver_user, approval_request):
        """Test retrieving a single approval request."""
        api_client.force_authenticate(user=approver_user)
        response = api_client.get(f'/api/approvals/{approval_request.id}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == approval_request.id
        assert response.data['deliverable_title'] == 'Test Deliverable'
        assert response.data['requested_by_username'] == 'planner'
        assert 'steps' in response.data
        assert len(response.data['steps']) == 1

    def test_retrieve_nonexistent_approval_request(self, api_client, approver_user):
        """Test retrieving a non-existent approval request."""
        api_client.force_authenticate(user=approver_user)
        response = api_client.get('/api/approvals/99999/')
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestApproveAction:
    """Tests for approve action."""

    def test_approve_success(self, api_client, approver_user, approval_request):
        """Test successful approval."""
        api_client.force_authenticate(user=approver_user)
        response = api_client.post(f'/api/approvals/{approval_request.id}/approve/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['status'] == 'APPROVED'

        approval_request.refresh_from_db()
        assert approval_request.status == ApprovalRequest.Status.APPROVED
        assert approval_request.decided_at is not None

        approval_request.deliverable.refresh_from_db()
        assert approval_request.deliverable.status == Deliverable.Status.APPROVED

        step = approval_request.steps.first()
        step.refresh_from_db()
        assert step.status == ApprovalStep.Status.APPROVED
        assert step.decided_by == approver_user
        assert step.decided_at is not None

    def test_approve_creates_audit_event(self, api_client, approver_user, approval_request):
        """Test that approval creates an audit event."""
        initial_count = AuditEvent.objects.count()
        api_client.force_authenticate(user=approver_user)
        api_client.post(f'/api/approvals/{approval_request.id}/approve/')

        assert AuditEvent.objects.count() == initial_count + 1
        event = AuditEvent.objects.latest('created_at')
        assert event.actor == approver_user
        assert event.verb == 'approved'
        assert event.object_type == 'ApprovalRequest'
        assert event.object_id == str(approval_request.id)

    def test_approve_admin_success(self, api_client, admin_user, approval_request):
        """Test that admin can approve."""
        api_client.force_authenticate(user=admin_user)
        response = api_client.post(f'/api/approvals/{approval_request.id}/approve/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['status'] == 'APPROVED'

    def test_approve_non_pending_request(self, api_client, approver_user, approval_request):
        """Test approving a non-pending request."""
        approval_request.status = ApprovalRequest.Status.APPROVED
        approval_request.save()

        api_client.force_authenticate(user=approver_user)
        response = api_client.post(f'/api/approvals/{approval_request.id}/approve/')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'error' in response.data
        assert 'pending' in response.data['error'].lower()

    def test_approve_rejected_request(self, api_client, approver_user, approval_request):
        """Test approving a rejected request."""
        approval_request.status = ApprovalRequest.Status.REJECTED
        approval_request.save()

        api_client.force_authenticate(user=approver_user)
        response = api_client.post(f'/api/approvals/{approval_request.id}/approve/')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_approve_permission_denied_viewer(self, api_client, viewer_user, approval_request):
        """Test that viewer cannot approve."""
        api_client.force_authenticate(user=viewer_user)
        response = api_client.post(f'/api/approvals/{approval_request.id}/approve/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_approve_permission_denied_planner(self, api_client, planner_user, approval_request):
        """Test that planner cannot approve."""
        api_client.force_authenticate(user=planner_user)
        response = api_client.post(f'/api/approvals/{approval_request.id}/approve/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_approve_unauthenticated(self, api_client, approval_request):
        """Test approving without authentication."""
        response = api_client.post(f'/api/approvals/{approval_request.id}/approve/')
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestRejectAction:
    """Tests for reject action."""

    def test_reject_success(self, api_client, approver_user, approval_request):
        """Test successful rejection."""
        api_client.force_authenticate(user=approver_user)
        response = api_client.post(f'/api/approvals/{approval_request.id}/reject/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['status'] == 'REJECTED'

        approval_request.refresh_from_db()
        assert approval_request.status == ApprovalRequest.Status.REJECTED
        assert approval_request.decided_at is not None

        approval_request.deliverable.refresh_from_db()
        assert approval_request.deliverable.status == Deliverable.Status.REJECTED

        step = approval_request.steps.first()
        step.refresh_from_db()
        assert step.status == ApprovalStep.Status.REJECTED
        assert step.decided_by == approver_user
        assert step.decided_at is not None

    def test_reject_creates_audit_event(self, api_client, approver_user, approval_request):
        """Test that rejection creates an audit event."""
        initial_count = AuditEvent.objects.count()
        api_client.force_authenticate(user=approver_user)
        api_client.post(f'/api/approvals/{approval_request.id}/reject/')

        assert AuditEvent.objects.count() == initial_count + 1
        event = AuditEvent.objects.latest('created_at')
        assert event.actor == approver_user
        assert event.verb == 'rejected'
        assert event.object_type == 'ApprovalRequest'
        assert event.object_id == str(approval_request.id)

    def test_reject_admin_success(self, api_client, admin_user, approval_request):
        """Test that admin can reject."""
        api_client.force_authenticate(user=admin_user)
        response = api_client.post(f'/api/approvals/{approval_request.id}/reject/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['status'] == 'REJECTED'

    def test_reject_non_pending_request(self, api_client, approver_user, approval_request):
        """Test rejecting a non-pending request."""
        approval_request.status = ApprovalRequest.Status.APPROVED
        approval_request.save()

        api_client.force_authenticate(user=approver_user)
        response = api_client.post(f'/api/approvals/{approval_request.id}/reject/')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'error' in response.data
        assert 'pending' in response.data['error'].lower()

    def test_reject_already_rejected_request(self, api_client, approver_user, approval_request):
        """Test rejecting an already rejected request."""
        approval_request.status = ApprovalRequest.Status.REJECTED
        approval_request.save()

        api_client.force_authenticate(user=approver_user)
        response = api_client.post(f'/api/approvals/{approval_request.id}/reject/')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_reject_permission_denied_viewer(self, api_client, viewer_user, approval_request):
        """Test that viewer cannot reject."""
        api_client.force_authenticate(user=viewer_user)
        response = api_client.post(f'/api/approvals/{approval_request.id}/reject/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_reject_permission_denied_planner(self, api_client, planner_user, approval_request):
        """Test that planner cannot reject."""
        api_client.force_authenticate(user=planner_user)
        response = api_client.post(f'/api/approvals/{approval_request.id}/reject/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_reject_unauthenticated(self, api_client, approval_request):
        """Test rejecting without authentication."""
        response = api_client.post(f'/api/approvals/{approval_request.id}/reject/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

