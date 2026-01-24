"""Comprehensive permission boundary tests for all endpoints."""
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
def all_role_users():
    """Create users with all roles."""
    return {
        'admin': User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='testpass123',
            role=User.ADMIN,
        ),
        'planner': User.objects.create_user(
            username='planner',
            email='planner@example.com',
            password='testpass123',
            role=User.PLANNER,
        ),
        'approver': User.objects.create_user(
            username='approver',
            email='approver@example.com',
            password='testpass123',
            role=User.APPROVER,
        ),
        'viewer': User.objects.create_user(
            username='viewer',
            email='viewer@example.com',
            password='testpass123',
            role=User.VIEWER,
        ),
    }


@pytest.fixture
def client_obj():
    """Create a test client."""
    return Client.objects.create(name='Test Client')


@pytest.fixture
def deliverable(client_obj, all_role_users):
    """Create a test deliverable."""
    return Deliverable.objects.create(
        title='Test Deliverable',
        client=client_obj,
        created_by=all_role_users['planner'],
    )


@pytest.fixture
def submitted_deliverable(client_obj, all_role_users):
    """Create a submitted deliverable."""
    return Deliverable.objects.create(
        title='Submitted Deliverable',
        client=client_obj,
        created_by=all_role_users['planner'],
        status=Deliverable.SUBMITTED,
    )


@pytest.fixture
def approval_request(submitted_deliverable, all_role_users):
    """Create an approval request with a step."""
    request = ApprovalRequest.objects.create(
        deliverable=submitted_deliverable,
        requested_by=all_role_users['planner'],
    )
    ApprovalStep.objects.create(
        approval_request=request,
        step_order=1,
        assigned_role=ApprovalStep.ROLE_APPROVER,
    )
    return request


@pytest.mark.django_db
class TestAuthenticationRequired:
    """Test that all endpoints require authentication."""

    def test_unauthenticated_access_denied_clients(self, api_client):
        """Test clients endpoint requires authentication."""
        response = api_client.get('/api/clients/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_unauthenticated_access_denied_deliverables(self, api_client):
        """Test deliverables endpoint requires authentication."""
        response = api_client.get('/api/deliverables/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_unauthenticated_access_denied_approvals(self, api_client):
        """Test approvals endpoint requires authentication."""
        response = api_client.get('/api/approvals/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_unauthenticated_access_denied_audit(self, api_client):
        """Test audit endpoint requires authentication."""
        response = api_client.get('/api/audit/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_unauthenticated_cannot_create_client(self, api_client):
        """Test unauthenticated user cannot create client."""
        response = api_client.post('/api/clients/', {'name': 'New Client'})
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_unauthenticated_cannot_create_deliverable(self, api_client, client_obj):
        """Test unauthenticated user cannot create deliverable."""
        response = api_client.post('/api/deliverables/', {
            'title': 'Test',
            'client': client_obj.id,
        })
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestClientsPermissions:
    """Test permission boundaries for clients endpoints."""

    def test_viewer_cannot_access_clients(self, api_client, all_role_users, client_obj):
        """Test VIEWER role cannot access client endpoints."""
        api_client.force_authenticate(user=all_role_users['viewer'])
        response = api_client.get('/api/clients/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_planner_cannot_access_clients(self, api_client, all_role_users, client_obj):
        """Test PLANNER role cannot access client endpoints."""
        api_client.force_authenticate(user=all_role_users['planner'])
        response = api_client.get('/api/clients/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_approver_cannot_access_clients(self, api_client, all_role_users, client_obj):
        """Test APPROVER role cannot access client endpoints."""
        api_client.force_authenticate(user=all_role_users['approver'])
        response = api_client.get('/api/clients/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_viewer_cannot_create_clients(self, api_client, all_role_users):
        """Test VIEWER role cannot create clients."""
        api_client.force_authenticate(user=all_role_users['viewer'])
        response = api_client.post('/api/clients/', {'name': 'New Client'})
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_planner_cannot_create_clients(self, api_client, all_role_users):
        """Test PLANNER role cannot create clients."""
        api_client.force_authenticate(user=all_role_users['planner'])
        response = api_client.post('/api/clients/', {'name': 'New Client'})
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_approver_cannot_create_clients(self, api_client, all_role_users):
        """Test APPROVER role cannot create clients."""
        api_client.force_authenticate(user=all_role_users['approver'])
        response = api_client.post('/api/clients/', {'name': 'New Client'})
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_viewer_cannot_update_clients(self, api_client, all_role_users, client_obj):
        """Test VIEWER role cannot update clients."""
        api_client.force_authenticate(user=all_role_users['viewer'])
        response = api_client.put(
            f'/api/clients/{client_obj.id}/',
            {'name': 'Updated Client'},
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_planner_cannot_update_clients(self, api_client, all_role_users, client_obj):
        """Test PLANNER role cannot update clients."""
        api_client.force_authenticate(user=all_role_users['planner'])
        response = api_client.put(
            f'/api/clients/{client_obj.id}/',
            {'name': 'Updated Client'},
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_approver_cannot_update_clients(self, api_client, all_role_users, client_obj):
        """Test APPROVER role cannot update clients."""
        api_client.force_authenticate(user=all_role_users['approver'])
        response = api_client.put(
            f'/api/clients/{client_obj.id}/',
            {'name': 'Updated Client'},
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_viewer_cannot_delete_clients(self, api_client, all_role_users, client_obj):
        """Test VIEWER role cannot delete clients."""
        api_client.force_authenticate(user=all_role_users['viewer'])
        response = api_client.delete(f'/api/clients/{client_obj.id}/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_planner_cannot_delete_clients(self, api_client, all_role_users, client_obj):
        """Test PLANNER role cannot delete clients."""
        api_client.force_authenticate(user=all_role_users['planner'])
        response = api_client.delete(f'/api/clients/{client_obj.id}/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_approver_cannot_delete_clients(self, api_client, all_role_users, client_obj):
        """Test APPROVER role cannot delete clients."""
        api_client.force_authenticate(user=all_role_users['approver'])
        response = api_client.delete(f'/api/clients/{client_obj.id}/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_admin_can_access_clients(self, api_client, all_role_users, client_obj):
        """Test ADMIN role can access client endpoints."""
        api_client.force_authenticate(user=all_role_users['admin'])
        response = api_client.get('/api/clients/')
        assert response.status_code == status.HTTP_200_OK

    def test_admin_can_create_clients(self, api_client, all_role_users):
        """Test ADMIN role can create clients."""
        api_client.force_authenticate(user=all_role_users['admin'])
        response = api_client.post('/api/clients/', {'name': 'New Client'})
        assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
class TestDeliverablesPermissions:
    """Test permission boundaries for deliverables endpoints."""

    def test_viewer_cannot_access_deliverables(self, api_client, all_role_users, deliverable):
        """Test VIEWER role cannot access deliverables endpoints."""
        api_client.force_authenticate(user=all_role_users['viewer'])
        response = api_client.get('/api/deliverables/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_approver_cannot_access_deliverables(self, api_client, all_role_users, deliverable):
        """Test APPROVER role cannot access deliverables endpoints."""
        api_client.force_authenticate(user=all_role_users['approver'])
        response = api_client.get('/api/deliverables/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_viewer_cannot_create_deliverables(self, api_client, all_role_users, client_obj):
        """Test VIEWER role cannot create deliverables."""
        api_client.force_authenticate(user=all_role_users['viewer'])
        response = api_client.post('/api/deliverables/', {
            'title': 'Test',
            'client': client_obj.id,
        })
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_approver_cannot_create_deliverables(self, api_client, all_role_users, client_obj):
        """Test APPROVER role cannot create deliverables."""
        api_client.force_authenticate(user=all_role_users['approver'])
        response = api_client.post('/api/deliverables/', {
            'title': 'Test',
            'client': client_obj.id,
        })
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_viewer_cannot_update_deliverables(self, api_client, all_role_users, deliverable):
        """Test VIEWER role cannot update deliverables."""
        api_client.force_authenticate(user=all_role_users['viewer'])
        response = api_client.put(
            f'/api/deliverables/{deliverable.id}/',
            {'title': 'Updated', 'client': deliverable.client.id},
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_approver_cannot_update_deliverables(self, api_client, all_role_users, deliverable):
        """Test APPROVER role cannot update deliverables."""
        api_client.force_authenticate(user=all_role_users['approver'])
        response = api_client.put(
            f'/api/deliverables/{deliverable.id}/',
            {'title': 'Updated', 'client': deliverable.client.id},
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_viewer_cannot_delete_deliverables(self, api_client, all_role_users, deliverable):
        """Test VIEWER role cannot delete deliverables."""
        api_client.force_authenticate(user=all_role_users['viewer'])
        response = api_client.delete(f'/api/deliverables/{deliverable.id}/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_approver_cannot_delete_deliverables(self, api_client, all_role_users, deliverable):
        """Test APPROVER role cannot delete deliverables."""
        api_client.force_authenticate(user=all_role_users['approver'])
        response = api_client.delete(f'/api/deliverables/{deliverable.id}/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_viewer_cannot_submit_deliverables(self, api_client, all_role_users, deliverable):
        """Test VIEWER role cannot submit deliverables."""
        api_client.force_authenticate(user=all_role_users['viewer'])
        response = api_client.post(f'/api/deliverables/{deliverable.id}/submit/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_approver_cannot_submit_deliverables(self, api_client, all_role_users, deliverable):
        """Test APPROVER role cannot submit deliverables."""
        api_client.force_authenticate(user=all_role_users['approver'])
        response = api_client.post(f'/api/deliverables/{deliverable.id}/submit/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_planner_can_access_deliverables(self, api_client, all_role_users, deliverable):
        """Test PLANNER role can access deliverables endpoints."""
        api_client.force_authenticate(user=all_role_users['planner'])
        response = api_client.get('/api/deliverables/')
        assert response.status_code == status.HTTP_200_OK

    def test_admin_can_access_deliverables(self, api_client, all_role_users, deliverable):
        """Test ADMIN role can access deliverables endpoints."""
        api_client.force_authenticate(user=all_role_users['admin'])
        response = api_client.get('/api/deliverables/')
        assert response.status_code == status.HTTP_200_OK

    def test_planner_can_create_deliverables(self, api_client, all_role_users, client_obj):
        """Test PLANNER role can create deliverables."""
        api_client.force_authenticate(user=all_role_users['planner'])
        response = api_client.post('/api/deliverables/', {
            'title': 'New Deliverable',
            'client': client_obj.id,
        })
        assert response.status_code == status.HTTP_201_CREATED

    def test_planner_can_submit_deliverables(self, api_client, all_role_users, deliverable):
        """Test PLANNER role can submit deliverables."""
        api_client.force_authenticate(user=all_role_users['planner'])
        response = api_client.post(f'/api/deliverables/{deliverable.id}/submit/')
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestApprovalsPermissions:
    """Test permission boundaries for approvals endpoints."""

    def test_viewer_can_list_approvals(self, api_client, all_role_users, approval_request):
        """Test VIEWER role can list approval requests (read-only)."""
        api_client.force_authenticate(user=all_role_users['viewer'])
        response = api_client.get('/api/approvals/')
        assert response.status_code == status.HTTP_200_OK

    def test_planner_can_list_approvals(self, api_client, all_role_users, approval_request):
        """Test PLANNER role can list approval requests."""
        api_client.force_authenticate(user=all_role_users['planner'])
        response = api_client.get('/api/approvals/')
        assert response.status_code == status.HTTP_200_OK

    def test_viewer_cannot_approve_requests(self, api_client, all_role_users, approval_request):
        """Test VIEWER role cannot approve requests."""
        api_client.force_authenticate(user=all_role_users['viewer'])
        response = api_client.post(f'/api/approvals/{approval_request.id}/approve/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_planner_cannot_approve_requests(self, api_client, all_role_users, approval_request):
        """Test PLANNER role cannot approve requests."""
        api_client.force_authenticate(user=all_role_users['planner'])
        response = api_client.post(f'/api/approvals/{approval_request.id}/approve/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_viewer_cannot_reject_requests(self, api_client, all_role_users, approval_request):
        """Test VIEWER role cannot reject requests."""
        api_client.force_authenticate(user=all_role_users['viewer'])
        response = api_client.post(f'/api/approvals/{approval_request.id}/reject/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_planner_cannot_reject_requests(self, api_client, all_role_users, approval_request):
        """Test PLANNER role cannot reject requests."""
        api_client.force_authenticate(user=all_role_users['planner'])
        response = api_client.post(f'/api/approvals/{approval_request.id}/reject/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_approver_can_approve_requests(self, api_client, all_role_users, approval_request):
        """Test APPROVER role can approve requests."""
        api_client.force_authenticate(user=all_role_users['approver'])
        response = api_client.post(f'/api/approvals/{approval_request.id}/approve/')
        assert response.status_code == status.HTTP_200_OK

    def test_approver_can_reject_requests(self, api_client, all_role_users, submitted_deliverable):
        """Test APPROVER role can reject requests."""
        request = ApprovalRequest.objects.create(
            deliverable=submitted_deliverable,
            requested_by=all_role_users['planner'],
        )
        ApprovalStep.objects.create(
            approval_request=request,
            step_order=1,
            assigned_role=ApprovalStep.ROLE_APPROVER,
        )
        api_client.force_authenticate(user=all_role_users['approver'])
        response = api_client.post(f'/api/approvals/{request.id}/reject/')
        assert response.status_code == status.HTTP_200_OK

    def test_admin_can_approve_requests(self, api_client, all_role_users, submitted_deliverable):
        """Test ADMIN role can approve requests."""
        request = ApprovalRequest.objects.create(
            deliverable=submitted_deliverable,
            requested_by=all_role_users['planner'],
        )
        ApprovalStep.objects.create(
            approval_request=request,
            step_order=1,
            assigned_role=ApprovalStep.ROLE_APPROVER,
        )
        api_client.force_authenticate(user=all_role_users['admin'])
        response = api_client.post(f'/api/approvals/{request.id}/approve/')
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestAuditPermissions:
    """Test permission boundaries for audit endpoints."""

    def test_viewer_can_access_audit(self, api_client, all_role_users):
        """Test VIEWER role can access audit endpoint."""
        api_client.force_authenticate(user=all_role_users['viewer'])
        response = api_client.get('/api/audit/')
        assert response.status_code == status.HTTP_200_OK

    def test_planner_can_access_audit(self, api_client, all_role_users):
        """Test PLANNER role can access audit endpoint."""
        api_client.force_authenticate(user=all_role_users['planner'])
        response = api_client.get('/api/audit/')
        assert response.status_code == status.HTTP_200_OK

    def test_approver_can_access_audit(self, api_client, all_role_users):
        """Test APPROVER role can access audit endpoint."""
        api_client.force_authenticate(user=all_role_users['approver'])
        response = api_client.get('/api/audit/')
        assert response.status_code == status.HTTP_200_OK

    def test_admin_can_access_audit(self, api_client, all_role_users):
        """Test ADMIN role can access audit endpoint."""
        api_client.force_authenticate(user=all_role_users['admin'])
        response = api_client.get('/api/audit/')
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestWorkflowPermissions:
    """Test approval workflow enforces role boundaries."""

    def test_planner_submits_approver_approves(self, api_client, all_role_users, client_obj):
        """Test complete workflow: planner submits, approver approves."""
        deliverable = Deliverable.objects.create(
            title='Workflow Test Deliverable',
            client=client_obj,
            created_by=all_role_users['planner'],
            status=Deliverable.DRAFT,
        )

        api_client.force_authenticate(user=all_role_users['planner'])
        submit_response = api_client.post(f'/api/deliverables/{deliverable.id}/submit/')
        assert submit_response.status_code == status.HTTP_200_OK

        approval_request = ApprovalRequest.objects.get(deliverable=deliverable)

        approve_response = api_client.post(f'/api/approvals/{approval_request.id}/approve/')
        assert approve_response.status_code == status.HTTP_403_FORBIDDEN

        api_client.force_authenticate(user=all_role_users['approver'])
        approve_response = api_client.post(f'/api/approvals/{approval_request.id}/approve/')
        assert approve_response.status_code == status.HTTP_200_OK

        deliverable.refresh_from_db()
        assert deliverable.status == Deliverable.APPROVED

    def test_planner_submits_approver_rejects(self, api_client, all_role_users, client_obj):
        """Test workflow: planner submits, approver rejects."""
        deliverable = Deliverable.objects.create(
            title='Rejection Test Deliverable',
            client=client_obj,
            created_by=all_role_users['planner'],
            status=Deliverable.DRAFT,
        )

        api_client.force_authenticate(user=all_role_users['planner'])
        submit_response = api_client.post(f'/api/deliverables/{deliverable.id}/submit/')
        assert submit_response.status_code == status.HTTP_200_OK

        approval_request = ApprovalRequest.objects.get(deliverable=deliverable)

        reject_response = api_client.post(f'/api/approvals/{approval_request.id}/reject/')
        assert reject_response.status_code == status.HTTP_403_FORBIDDEN

        api_client.force_authenticate(user=all_role_users['approver'])
        reject_response = api_client.post(f'/api/approvals/{approval_request.id}/reject/')
        assert reject_response.status_code == status.HTTP_200_OK

        deliverable.refresh_from_db()
        assert deliverable.status == Deliverable.REJECTED

    def test_viewer_cannot_participate_in_workflow(self, api_client, all_role_users, client_obj):
        """Test VIEWER cannot participate in any workflow step."""
        deliverable = Deliverable.objects.create(
            title='Viewer Test Deliverable',
            client=client_obj,
            created_by=all_role_users['planner'],
            status=Deliverable.DRAFT,
        )

        api_client.force_authenticate(user=all_role_users['viewer'])

        submit_response = api_client.post(f'/api/deliverables/{deliverable.id}/submit/')
        assert submit_response.status_code == status.HTTP_403_FORBIDDEN

        api_client.force_authenticate(user=all_role_users['planner'])
        api_client.post(f'/api/deliverables/{deliverable.id}/submit/')
        approval_request = ApprovalRequest.objects.get(deliverable=deliverable)

        api_client.force_authenticate(user=all_role_users['viewer'])
        approve_response = api_client.post(f'/api/approvals/{approval_request.id}/approve/')
        assert approve_response.status_code == status.HTTP_403_FORBIDDEN

        reject_response = api_client.post(f'/api/approvals/{approval_request.id}/reject/')
        assert reject_response.status_code == status.HTTP_403_FORBIDDEN

    def test_approver_cannot_create_or_submit_deliverables(self, api_client, all_role_users, client_obj):
        """Test APPROVER cannot create or submit deliverables."""
        api_client.force_authenticate(user=all_role_users['approver'])

        create_response = api_client.post('/api/deliverables/', {
            'title': 'Approver Deliverable',
            'client': client_obj.id,
        })
        assert create_response.status_code == status.HTTP_403_FORBIDDEN

        deliverable = Deliverable.objects.create(
            title='Test Deliverable',
            client=client_obj,
            created_by=all_role_users['planner'],
            status=Deliverable.DRAFT,
        )
        submit_response = api_client.post(f'/api/deliverables/{deliverable.id}/submit/')
        assert submit_response.status_code == status.HTTP_403_FORBIDDEN
