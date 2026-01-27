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
def admin_user():
    """Create an admin user."""
    return User.objects.create_user(
        username='admin',
        email='admin@example.com',
        password='testpass123',
        role=User.ADMIN,
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


@pytest.fixture
def approval_request_with_multiple_steps(deliverable, planner_user):
    """Create an approval request with multiple steps."""
    request = ApprovalRequest.objects.create(
        deliverable=deliverable,
        requested_by=planner_user,
    )
    ApprovalStep.objects.create(
        approval_request=request,
        step_order=1,
        assigned_role=ApprovalStep.ROLE_APPROVER,
    )
    ApprovalStep.objects.create(
        approval_request=request,
        step_order=2,
        assigned_role=ApprovalStep.ROLE_FINANCE,
    )
    ApprovalStep.objects.create(
        approval_request=request,
        step_order=3,
        assigned_role=ApprovalStep.ROLE_LEGAL,
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
class TestApproveAction:
    """Tests for the approve action."""

    def test_approve_request_success(self, api_client, approver_user, approval_request):
        """Test that an approver can approve a pending request."""
        api_client.force_authenticate(user=approver_user)
        response = api_client.post(f'/api/approvals/{approval_request.id}/approve/')
        assert response.status_code == status.HTTP_200_OK
        approval_request.refresh_from_db()
        assert approval_request.status == ApprovalRequest.APPROVED

    def test_approve_updates_deliverable_status_to_approved(
        self, api_client, approver_user, approval_request
    ):
        """Test that approving a request updates the deliverable status to APPROVED."""
        api_client.force_authenticate(user=approver_user)
        api_client.post(f'/api/approvals/{approval_request.id}/approve/')
        approval_request.deliverable.refresh_from_db()
        assert approval_request.deliverable.status == Deliverable.APPROVED

    def test_approve_updates_step_status_to_approved(
        self, api_client, approver_user, approval_request
    ):
        """Test that approving a request updates the step status to STEP_APPROVED."""
        api_client.force_authenticate(user=approver_user)
        api_client.post(f'/api/approvals/{approval_request.id}/approve/')
        step = approval_request.steps.first()
        step.refresh_from_db()
        assert step.status == ApprovalStep.STEP_APPROVED
        assert step.decided_by == approver_user
        assert step.decided_at is not None

    def test_approve_sets_decided_at_timestamp(
        self, api_client, approver_user, approval_request
    ):
        """Test that approving a request sets the decided_at timestamp."""
        api_client.force_authenticate(user=approver_user)
        api_client.post(f'/api/approvals/{approval_request.id}/approve/')
        approval_request.refresh_from_db()
        assert approval_request.decided_at is not None

    def test_approve_creates_audit_event(
        self, api_client, approver_user, approval_request
    ):
        """Test that approving a request creates an audit event."""
        api_client.force_authenticate(user=approver_user)
        api_client.post(f'/api/approvals/{approval_request.id}/approve/')
        audit_event = AuditEvent.objects.filter(
            verb='approved',
            object_type='ApprovalRequest',
            object_id=str(approval_request.id),
        ).first()
        assert audit_event is not None
        assert audit_event.actor == approver_user
        assert audit_event.payload['deliverable_title'] == 'Test Deliverable'

    def test_approve_already_approved_request_fails(
        self, api_client, approver_user, approval_request
    ):
        """Test that approving an already approved request returns an error."""
        approval_request.status = ApprovalRequest.APPROVED
        approval_request.save()
        api_client.force_authenticate(user=approver_user)
        response = api_client.post(f'/api/approvals/{approval_request.id}/approve/')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'error' in response.data

    def test_approve_rejected_request_fails(
        self, api_client, approver_user, approval_request
    ):
        """Test that approving a rejected request returns an error."""
        approval_request.status = ApprovalRequest.REJECTED
        approval_request.save()
        api_client.force_authenticate(user=approver_user)
        response = api_client.post(f'/api/approvals/{approval_request.id}/approve/')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'error' in response.data

    def test_admin_can_approve(self, api_client, admin_user, approval_request):
        """Test that an admin can approve a request."""
        api_client.force_authenticate(user=admin_user)
        response = api_client.post(f'/api/approvals/{approval_request.id}/approve/')
        assert response.status_code == status.HTTP_200_OK
        approval_request.refresh_from_db()
        assert approval_request.status == ApprovalRequest.APPROVED


@pytest.mark.django_db
class TestRejectAction:
    """Tests for the reject action."""

    def test_reject_request_success(self, api_client, approver_user, approval_request):
        """Test that an approver can reject a pending request."""
        api_client.force_authenticate(user=approver_user)
        response = api_client.post(f'/api/approvals/{approval_request.id}/reject/')
        assert response.status_code == status.HTTP_200_OK
        approval_request.refresh_from_db()
        assert approval_request.status == ApprovalRequest.REJECTED

    def test_reject_updates_deliverable_status_to_rejected(
        self, api_client, approver_user, approval_request
    ):
        """Test that rejecting a request updates the deliverable status to REJECTED."""
        api_client.force_authenticate(user=approver_user)
        api_client.post(f'/api/approvals/{approval_request.id}/reject/')
        approval_request.deliverable.refresh_from_db()
        assert approval_request.deliverable.status == Deliverable.REJECTED

    def test_reject_updates_step_status_to_rejected(
        self, api_client, approver_user, approval_request
    ):
        """Test that rejecting a request updates the step status to STEP_REJECTED."""
        api_client.force_authenticate(user=approver_user)
        api_client.post(f'/api/approvals/{approval_request.id}/reject/')
        step = approval_request.steps.first()
        step.refresh_from_db()
        assert step.status == ApprovalStep.STEP_REJECTED
        assert step.decided_by == approver_user
        assert step.decided_at is not None

    def test_reject_sets_decided_at_timestamp(
        self, api_client, approver_user, approval_request
    ):
        """Test that rejecting a request sets the decided_at timestamp."""
        api_client.force_authenticate(user=approver_user)
        api_client.post(f'/api/approvals/{approval_request.id}/reject/')
        approval_request.refresh_from_db()
        assert approval_request.decided_at is not None

    def test_reject_creates_audit_event(
        self, api_client, approver_user, approval_request
    ):
        """Test that rejecting a request creates an audit event."""
        api_client.force_authenticate(user=approver_user)
        api_client.post(f'/api/approvals/{approval_request.id}/reject/')
        audit_event = AuditEvent.objects.filter(
            verb='rejected',
            object_type='ApprovalRequest',
            object_id=str(approval_request.id),
        ).first()
        assert audit_event is not None
        assert audit_event.actor == approver_user
        assert audit_event.payload['deliverable_title'] == 'Test Deliverable'

    def test_reject_already_rejected_request_fails(
        self, api_client, approver_user, approval_request
    ):
        """Test that rejecting an already rejected request returns an error."""
        approval_request.status = ApprovalRequest.REJECTED
        approval_request.save()
        api_client.force_authenticate(user=approver_user)
        response = api_client.post(f'/api/approvals/{approval_request.id}/reject/')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'error' in response.data

    def test_reject_approved_request_fails(
        self, api_client, approver_user, approval_request
    ):
        """Test that rejecting an approved request returns an error."""
        approval_request.status = ApprovalRequest.APPROVED
        approval_request.save()
        api_client.force_authenticate(user=approver_user)
        response = api_client.post(f'/api/approvals/{approval_request.id}/reject/')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'error' in response.data

    def test_admin_can_reject(self, api_client, admin_user, approval_request):
        """Test that an admin can reject a request."""
        api_client.force_authenticate(user=admin_user)
        response = api_client.post(f'/api/approvals/{approval_request.id}/reject/')
        assert response.status_code == status.HTTP_200_OK
        approval_request.refresh_from_db()
        assert approval_request.status == ApprovalRequest.REJECTED


@pytest.mark.django_db
class TestPermissionEnforcement:
    """Tests for permission enforcement on approve/reject actions."""

    def test_planner_cannot_approve(self, api_client, planner_user, approval_request):
        """Test that a planner cannot approve a request."""
        api_client.force_authenticate(user=planner_user)
        response = api_client.post(f'/api/approvals/{approval_request.id}/approve/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_planner_cannot_reject(self, api_client, planner_user, approval_request):
        """Test that a planner cannot reject a request."""
        api_client.force_authenticate(user=planner_user)
        response = api_client.post(f'/api/approvals/{approval_request.id}/reject/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_viewer_cannot_approve(self, api_client, viewer_user, approval_request):
        """Test that a viewer cannot approve a request."""
        api_client.force_authenticate(user=viewer_user)
        response = api_client.post(f'/api/approvals/{approval_request.id}/approve/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_viewer_cannot_reject(self, api_client, viewer_user, approval_request):
        """Test that a viewer cannot reject a request."""
        api_client.force_authenticate(user=viewer_user)
        response = api_client.post(f'/api/approvals/{approval_request.id}/reject/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_unauthenticated_cannot_approve(self, api_client, approval_request):
        """Test that an unauthenticated user cannot approve a request."""
        response = api_client.post(f'/api/approvals/{approval_request.id}/approve/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_unauthenticated_cannot_reject(self, api_client, approval_request):
        """Test that an unauthenticated user cannot reject a request."""
        response = api_client.post(f'/api/approvals/{approval_request.id}/reject/')
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestSequentialStepProcessing:
    """Tests for sequential step processing in approval workflow."""

    def test_approve_processes_first_pending_step(
        self, api_client, approver_user, approval_request_with_multiple_steps
    ):
        """Test that approving processes the first pending step in order."""
        api_client.force_authenticate(user=approver_user)
        api_client.post(
            f'/api/approvals/{approval_request_with_multiple_steps.id}/approve/'
        )
        steps = approval_request_with_multiple_steps.steps.order_by('step_order')
        step1 = steps[0]
        step2 = steps[1]
        step3 = steps[2]
        step1.refresh_from_db()
        step2.refresh_from_db()
        step3.refresh_from_db()
        assert step1.status == ApprovalStep.STEP_APPROVED
        assert step2.status == ApprovalStep.STEP_PENDING
        assert step3.status == ApprovalStep.STEP_PENDING

    def test_reject_processes_first_pending_step(
        self, api_client, approver_user, approval_request_with_multiple_steps
    ):
        """Test that rejecting processes the first pending step in order."""
        api_client.force_authenticate(user=approver_user)
        api_client.post(
            f'/api/approvals/{approval_request_with_multiple_steps.id}/reject/'
        )
        steps = approval_request_with_multiple_steps.steps.order_by('step_order')
        step1 = steps[0]
        step2 = steps[1]
        step3 = steps[2]
        step1.refresh_from_db()
        step2.refresh_from_db()
        step3.refresh_from_db()
        assert step1.status == ApprovalStep.STEP_REJECTED
        assert step2.status == ApprovalStep.STEP_PENDING
        assert step3.status == ApprovalStep.STEP_PENDING

    def test_step_order_is_respected(
        self, api_client, approver_user, client_obj, planner_user
    ):
        """Test that steps are processed in the correct order based on step_order."""
        deliverable = Deliverable.objects.create(
            title='Ordered Steps Test',
            client=client_obj,
            created_by=planner_user,
            status=Deliverable.SUBMITTED,
        )
        request = ApprovalRequest.objects.create(
            deliverable=deliverable,
            requested_by=planner_user,
        )
        step3 = ApprovalStep.objects.create(
            approval_request=request,
            step_order=3,
            assigned_role=ApprovalStep.ROLE_LEGAL,
        )
        step1 = ApprovalStep.objects.create(
            approval_request=request,
            step_order=1,
            assigned_role=ApprovalStep.ROLE_APPROVER,
        )
        step2 = ApprovalStep.objects.create(
            approval_request=request,
            step_order=2,
            assigned_role=ApprovalStep.ROLE_FINANCE,
        )
        api_client.force_authenticate(user=approver_user)
        api_client.post(f'/api/approvals/{request.id}/approve/')
        step1.refresh_from_db()
        step2.refresh_from_db()
        step3.refresh_from_db()
        assert step1.status == ApprovalStep.STEP_APPROVED
        assert step2.status == ApprovalStep.STEP_PENDING
        assert step3.status == ApprovalStep.STEP_PENDING

