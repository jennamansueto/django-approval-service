"""Tests for deliverables views."""
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
def planner_user():
    """Create a planner user."""
    return User.objects.create_user(
        username='planner',
        email='planner@example.com',
        password='testpass123',
        role=User.Role.PLANNER,
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
    """Create a test deliverable."""
    return Deliverable.objects.create(
        title='Test Deliverable',
        client=client_obj,
        created_by=planner_user,
    )


@pytest.mark.django_db
class TestDeliverableViewSet:
    """Tests for Deliverable viewset."""

    def test_list_deliverables(self, api_client, planner_user, deliverable):
        """Test listing deliverables."""
        api_client.force_authenticate(user=planner_user)
        response = api_client.get('/api/deliverables/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_list_deliverables_unauthenticated(self, api_client, deliverable):
        """Test listing deliverables without authentication."""
        response = api_client.get('/api/deliverables/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_list_deliverables_viewer_denied(self, api_client, viewer_user, deliverable):
        """Test that viewer cannot list deliverables."""
        api_client.force_authenticate(user=viewer_user)
        response = api_client.get('/api/deliverables/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_list_deliverables_approver_denied(self, api_client, approver_user, deliverable):
        """Test that approver cannot list deliverables."""
        api_client.force_authenticate(user=approver_user)
        response = api_client.get('/api/deliverables/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_list_deliverables_admin_allowed(self, api_client, admin_user, deliverable):
        """Test that admin can list deliverables."""
        api_client.force_authenticate(user=admin_user)
        response = api_client.get('/api/deliverables/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1


@pytest.mark.django_db
class TestDeliverableCreate:
    """Tests for creating deliverables."""

    def test_create_deliverable(self, api_client, planner_user, client_obj):
        """Test creating a deliverable."""
        api_client.force_authenticate(user=planner_user)
        response = api_client.post(
            '/api/deliverables/',
            {
                'title': 'New Deliverable',
                'description': 'A new deliverable',
                'client': client_obj.id,
            },
            format='json',
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['title'] == 'New Deliverable'
        assert response.data['description'] == 'A new deliverable'

        deliverable = Deliverable.objects.get(id=response.data['id'])
        assert deliverable.status == Deliverable.Status.DRAFT
        assert deliverable.created_by == planner_user

    def test_create_deliverable_admin(self, api_client, admin_user, client_obj):
        """Test that admin can create a deliverable."""
        api_client.force_authenticate(user=admin_user)
        response = api_client.post(
            '/api/deliverables/',
            {
                'title': 'Admin Deliverable',
                'client': client_obj.id,
            },
            format='json',
        )
        assert response.status_code == status.HTTP_201_CREATED

        deliverable = Deliverable.objects.get(id=response.data['id'])
        assert deliverable.created_by == admin_user

    def test_create_deliverable_viewer_denied(self, api_client, viewer_user, client_obj):
        """Test that viewer cannot create a deliverable."""
        api_client.force_authenticate(user=viewer_user)
        response = api_client.post(
            '/api/deliverables/',
            {
                'title': 'Viewer Deliverable',
                'client': client_obj.id,
            },
            format='json',
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_deliverable_approver_denied(self, api_client, approver_user, client_obj):
        """Test that approver cannot create a deliverable."""
        api_client.force_authenticate(user=approver_user)
        response = api_client.post(
            '/api/deliverables/',
            {
                'title': 'Approver Deliverable',
                'client': client_obj.id,
            },
            format='json',
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_deliverable_unauthenticated(self, api_client, client_obj):
        """Test creating a deliverable without authentication."""
        response = api_client.post(
            '/api/deliverables/',
            {
                'title': 'New Deliverable',
                'client': client_obj.id,
            },
            format='json',
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_deliverable_missing_title(self, api_client, planner_user, client_obj):
        """Test creating a deliverable without title."""
        api_client.force_authenticate(user=planner_user)
        response = api_client.post(
            '/api/deliverables/',
            {
                'client': client_obj.id,
            },
            format='json',
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_deliverable_missing_client(self, api_client, planner_user):
        """Test creating a deliverable without client."""
        api_client.force_authenticate(user=planner_user)
        response = api_client.post(
            '/api/deliverables/',
            {
                'title': 'New Deliverable',
            },
            format='json',
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_deliverable_invalid_client(self, api_client, planner_user):
        """Test creating a deliverable with invalid client."""
        api_client.force_authenticate(user=planner_user)
        response = api_client.post(
            '/api/deliverables/',
            {
                'title': 'New Deliverable',
                'client': 99999,
            },
            format='json',
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestDeliverableRetrieve:
    """Tests for retrieving a single deliverable."""

    def test_retrieve_deliverable(self, api_client, planner_user, deliverable):
        """Test retrieving a single deliverable."""
        api_client.force_authenticate(user=planner_user)
        response = api_client.get(f'/api/deliverables/{deliverable.id}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == deliverable.id
        assert response.data['title'] == 'Test Deliverable'
        assert response.data['created_by_username'] == 'planner'
        assert response.data['client_name'] == 'Test Client'

    def test_retrieve_deliverable_unauthenticated(self, api_client, deliverable):
        """Test retrieving a deliverable without authentication."""
        response = api_client.get(f'/api/deliverables/{deliverable.id}/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_retrieve_nonexistent_deliverable(self, api_client, planner_user):
        """Test retrieving a non-existent deliverable."""
        api_client.force_authenticate(user=planner_user)
        response = api_client.get('/api/deliverables/99999/')
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestDeliverableUpdate:
    """Tests for updating deliverables."""

    def test_update_deliverable(self, api_client, planner_user, deliverable):
        """Test updating a deliverable."""
        api_client.force_authenticate(user=planner_user)
        response = api_client.put(
            f'/api/deliverables/{deliverable.id}/',
            {
                'title': 'Updated Deliverable',
                'description': 'Updated description',
                'client': deliverable.client.id,
            },
            format='json',
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'Updated Deliverable'
        assert response.data['description'] == 'Updated description'

    def test_partial_update_deliverable(self, api_client, planner_user, deliverable):
        """Test partial update of a deliverable."""
        api_client.force_authenticate(user=planner_user)
        response = api_client.patch(
            f'/api/deliverables/{deliverable.id}/',
            {'title': 'Patched Deliverable'},
            format='json',
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'Patched Deliverable'

    def test_update_deliverable_viewer_denied(self, api_client, viewer_user, deliverable):
        """Test that viewer cannot update a deliverable."""
        api_client.force_authenticate(user=viewer_user)
        response = api_client.put(
            f'/api/deliverables/{deliverable.id}/',
            {
                'title': 'Updated Deliverable',
                'client': deliverable.client.id,
            },
            format='json',
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_deliverable_unauthenticated(self, api_client, deliverable):
        """Test updating a deliverable without authentication."""
        response = api_client.put(
            f'/api/deliverables/{deliverable.id}/',
            {
                'title': 'Updated Deliverable',
                'client': deliverable.client.id,
            },
            format='json',
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestDeliverableDelete:
    """Tests for deleting deliverables."""

    def test_delete_deliverable(self, api_client, planner_user, deliverable):
        """Test deleting a deliverable."""
        deliverable_id = deliverable.id
        api_client.force_authenticate(user=planner_user)
        response = api_client.delete(f'/api/deliverables/{deliverable_id}/')
        assert response.status_code == status.HTTP_204_NO_CONTENT

        assert not Deliverable.objects.filter(id=deliverable_id).exists()

    def test_delete_deliverable_viewer_denied(self, api_client, viewer_user, deliverable):
        """Test that viewer cannot delete a deliverable."""
        api_client.force_authenticate(user=viewer_user)
        response = api_client.delete(f'/api/deliverables/{deliverable.id}/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_deliverable_unauthenticated(self, api_client, deliverable):
        """Test deleting a deliverable without authentication."""
        response = api_client.delete(f'/api/deliverables/{deliverable.id}/')
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestDeliverableSubmit:
    """Tests for submit action."""

    def test_submit_deliverable(self, api_client, planner_user, deliverable):
        """Test submitting a deliverable."""
        api_client.force_authenticate(user=planner_user)
        response = api_client.post(f'/api/deliverables/{deliverable.id}/submit/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['status'] == 'SUBMITTED'

        deliverable.refresh_from_db()
        assert deliverable.status == Deliverable.Status.SUBMITTED

    def test_submit_creates_approval_request(self, api_client, planner_user, deliverable):
        """Test that submit creates an approval request."""
        api_client.force_authenticate(user=planner_user)
        api_client.post(f'/api/deliverables/{deliverable.id}/submit/')

        approval_request = ApprovalRequest.objects.filter(deliverable=deliverable).first()
        assert approval_request is not None
        assert approval_request.requested_by == planner_user
        assert approval_request.status == ApprovalRequest.Status.PENDING

    def test_submit_creates_approval_step(self, api_client, planner_user, deliverable):
        """Test that submit creates an approval step."""
        api_client.force_authenticate(user=planner_user)
        api_client.post(f'/api/deliverables/{deliverable.id}/submit/')

        approval_request = ApprovalRequest.objects.filter(deliverable=deliverable).first()
        step = approval_request.steps.first()
        assert step is not None
        assert step.step_order == 1
        assert step.assigned_role == ApprovalStep.AssignedRole.APPROVER
        assert step.status == ApprovalStep.Status.PENDING

    def test_submit_creates_audit_event(self, api_client, planner_user, deliverable):
        """Test that submit creates an audit event."""
        initial_count = AuditEvent.objects.count()
        api_client.force_authenticate(user=planner_user)
        api_client.post(f'/api/deliverables/{deliverable.id}/submit/')

        assert AuditEvent.objects.count() == initial_count + 1
        event = AuditEvent.objects.latest('created_at')
        assert event.actor == planner_user
        assert event.verb == 'submitted'
        assert event.object_type == 'Deliverable'
        assert event.object_id == str(deliverable.id)
        assert event.payload['title'] == deliverable.title

    def test_submit_non_draft_deliverable(self, api_client, planner_user, deliverable):
        """Test submitting a non-draft deliverable."""
        deliverable.status = Deliverable.Status.SUBMITTED
        deliverable.save()

        api_client.force_authenticate(user=planner_user)
        response = api_client.post(f'/api/deliverables/{deliverable.id}/submit/')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'error' in response.data
        assert 'draft' in response.data['error'].lower()

    def test_submit_approved_deliverable(self, api_client, planner_user, deliverable):
        """Test submitting an approved deliverable."""
        deliverable.status = Deliverable.Status.APPROVED
        deliverable.save()

        api_client.force_authenticate(user=planner_user)
        response = api_client.post(f'/api/deliverables/{deliverable.id}/submit/')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_submit_rejected_deliverable(self, api_client, planner_user, deliverable):
        """Test submitting a rejected deliverable."""
        deliverable.status = Deliverable.Status.REJECTED
        deliverable.save()

        api_client.force_authenticate(user=planner_user)
        response = api_client.post(f'/api/deliverables/{deliverable.id}/submit/')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_submit_viewer_denied(self, api_client, viewer_user, deliverable):
        """Test that viewer cannot submit a deliverable."""
        api_client.force_authenticate(user=viewer_user)
        response = api_client.post(f'/api/deliverables/{deliverable.id}/submit/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_submit_approver_denied(self, api_client, approver_user, deliverable):
        """Test that approver cannot submit a deliverable."""
        api_client.force_authenticate(user=approver_user)
        response = api_client.post(f'/api/deliverables/{deliverable.id}/submit/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_submit_unauthenticated(self, api_client, deliverable):
        """Test submitting a deliverable without authentication."""
        response = api_client.post(f'/api/deliverables/{deliverable.id}/submit/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_submit_admin_allowed(self, api_client, admin_user, client_obj):
        """Test that admin can submit a deliverable."""
        deliverable = Deliverable.objects.create(
            title='Admin Deliverable',
            client=client_obj,
            created_by=admin_user,
        )
        api_client.force_authenticate(user=admin_user)
        response = api_client.post(f'/api/deliverables/{deliverable.id}/submit/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['status'] == 'SUBMITTED'

