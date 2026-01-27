"""Tests for approvals models."""
import pytest

from accounts.models import User
from approvals.models import ApprovalRequest, ApprovalStep
from clients.models import Client
from deliverables.models import Deliverable


@pytest.fixture
def user():
    """Create a test user."""
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123',
    )


@pytest.fixture
def approver_user():
    """Create an approver user."""
    return User.objects.create_user(
        username='approver',
        email='approver@example.com',
        password='testpass123',
        role=User.Role.APPROVER,
    )


@pytest.fixture
def client_obj():
    """Create a test client."""
    return Client.objects.create(name='Test Client')


@pytest.fixture
def deliverable(client_obj, user):
    """Create a test deliverable."""
    return Deliverable.objects.create(
        title='Test Deliverable',
        client=client_obj,
        created_by=user,
    )


@pytest.fixture
def approval_request(deliverable, user):
    """Create an approval request."""
    return ApprovalRequest.objects.create(
        deliverable=deliverable,
        requested_by=user,
    )


@pytest.mark.django_db
class TestApprovalRequestModel:
    """Tests for ApprovalRequest model."""

    def test_create_approval_request(self, deliverable, user):
        """Test creating an approval request."""
        request = ApprovalRequest.objects.create(
            deliverable=deliverable,
            requested_by=user,
        )
        assert request.status == ApprovalRequest.PENDING
        assert request.deliverable == deliverable

    def test_approval_request_str(self, deliverable, user):
        """Test approval request string representation."""
        request = ApprovalRequest.objects.create(
            deliverable=deliverable,
            requested_by=user,
        )
        assert 'Test Deliverable' in str(request)
        assert 'PENDING' in str(request)

    def test_approval_request_default_status(self, deliverable, user):
        """Test that default status is PENDING."""
        request = ApprovalRequest.objects.create(
            deliverable=deliverable,
            requested_by=user,
        )
        assert request.status == ApprovalRequest.Status.PENDING

    def test_approval_request_created_at(self, deliverable, user):
        """Test that created_at is set automatically."""
        request = ApprovalRequest.objects.create(
            deliverable=deliverable,
            requested_by=user,
        )
        assert request.created_at is not None

    def test_approval_request_decided_at_null_by_default(self, deliverable, user):
        """Test that decided_at is null by default."""
        request = ApprovalRequest.objects.create(
            deliverable=deliverable,
            requested_by=user,
        )
        assert request.decided_at is None

    def test_approval_request_all_statuses(self, deliverable, user):
        """Test all possible statuses for approval request."""
        for status_choice in ApprovalRequest.Status.choices:
            request = ApprovalRequest.objects.create(
                deliverable=deliverable,
                requested_by=user,
                status=status_choice[0],
            )
            assert request.status == status_choice[0]
            request.delete()


@pytest.mark.django_db
class TestApprovalStepModel:
    """Tests for ApprovalStep model."""

    def test_create_approval_step(self, approval_request):
        """Test creating an approval step."""
        step = ApprovalStep.objects.create(
            approval_request=approval_request,
            step_order=1,
            assigned_role=ApprovalStep.AssignedRole.APPROVER,
        )
        assert step.status == ApprovalStep.Status.PENDING
        assert step.step_order == 1
        assert step.assigned_role == ApprovalStep.AssignedRole.APPROVER

    def test_approval_step_str(self, approval_request):
        """Test approval step string representation."""
        step = ApprovalStep.objects.create(
            approval_request=approval_request,
            step_order=1,
            assigned_role=ApprovalStep.AssignedRole.APPROVER,
        )
        assert 'Step 1' in str(step)
        assert 'APPROVER' in str(step)
        assert 'PENDING' in str(step)

    def test_approval_step_default_status(self, approval_request):
        """Test that default status is PENDING."""
        step = ApprovalStep.objects.create(
            approval_request=approval_request,
            step_order=1,
        )
        assert step.status == ApprovalStep.Status.PENDING

    def test_approval_step_default_assigned_role(self, approval_request):
        """Test that default assigned role is APPROVER."""
        step = ApprovalStep.objects.create(
            approval_request=approval_request,
            step_order=1,
        )
        assert step.assigned_role == ApprovalStep.AssignedRole.APPROVER

    def test_approval_step_decided_by_null_by_default(self, approval_request):
        """Test that decided_by is null by default."""
        step = ApprovalStep.objects.create(
            approval_request=approval_request,
            step_order=1,
        )
        assert step.decided_by is None

    def test_approval_step_decided_at_null_by_default(self, approval_request):
        """Test that decided_at is null by default."""
        step = ApprovalStep.objects.create(
            approval_request=approval_request,
            step_order=1,
        )
        assert step.decided_at is None

    def test_approval_step_with_decided_by(self, approval_request, approver_user):
        """Test approval step with decided_by set."""
        step = ApprovalStep.objects.create(
            approval_request=approval_request,
            step_order=1,
            decided_by=approver_user,
        )
        assert step.decided_by == approver_user

    def test_approval_step_all_statuses(self, approval_request):
        """Test all possible statuses for approval step."""
        for status_choice in ApprovalStep.Status.choices:
            step = ApprovalStep.objects.create(
                approval_request=approval_request,
                step_order=1,
                status=status_choice[0],
            )
            assert step.status == status_choice[0]
            step.delete()

    def test_approval_step_all_assigned_roles(self, approval_request):
        """Test all possible assigned roles for approval step."""
        for role_choice in ApprovalStep.AssignedRole.choices:
            step = ApprovalStep.objects.create(
                approval_request=approval_request,
                step_order=1,
                assigned_role=role_choice[0],
            )
            assert step.assigned_role == role_choice[0]
            step.delete()

    def test_multiple_steps_ordering(self, approval_request):
        """Test that multiple steps are ordered correctly."""
        step1 = ApprovalStep.objects.create(
            approval_request=approval_request,
            step_order=2,
        )
        step2 = ApprovalStep.objects.create(
            approval_request=approval_request,
            step_order=1,
        )
        step3 = ApprovalStep.objects.create(
            approval_request=approval_request,
            step_order=3,
        )

        steps = list(approval_request.steps.all())
        assert steps[0].step_order == 1
        assert steps[1].step_order == 2
        assert steps[2].step_order == 3
