"""Management command to seed sample data."""
from django.core.management.base import BaseCommand

from accounts.models import User
from approvals.models import ApprovalRequest, ApprovalStep
from clients.models import Client
from deliverables.models import Deliverable


class Command(BaseCommand):
    """Seed the database with sample data."""

    help = 'Creates sample users, clients, deliverables, and approvals'

    def handle(self, *args, **options):
        self.stdout.write('Seeding database...')

        # Create users
        admin, _ = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'role': User.ADMIN,
                'is_staff': True,
                'is_superuser': True,
            }
        )
        admin.set_password('admin123')
        admin.save()

        planner, _ = User.objects.get_or_create(
            username='planner',
            defaults={
                'email': 'planner@example.com',
                'role': User.PLANNER,
            }
        )
        planner.set_password('planner123')
        planner.save()

        approver, _ = User.objects.get_or_create(
            username='approver',
            defaults={
                'email': 'approver@example.com',
                'role': User.APPROVER,
            }
        )
        approver.set_password('approver123')
        approver.save()

        viewer, _ = User.objects.get_or_create(
            username='viewer',
            defaults={
                'email': 'viewer@example.com',
                'role': User.VIEWER,
            }
        )
        viewer.set_password('viewer123')
        viewer.save()

        self.stdout.write(self.style.SUCCESS('Created users: admin, planner, approver, viewer'))

        # Create clients
        acme, _ = Client.objects.get_or_create(name='Acme Corporation')
        globex, _ = Client.objects.get_or_create(name='Globex Industries')
        initech, _ = Client.objects.get_or_create(name='Initech LLC')

        self.stdout.write(self.style.SUCCESS('Created clients: Acme, Globex, Initech'))

        # Create deliverables
        d1, _ = Deliverable.objects.get_or_create(
            title='Q1 Financial Summary',
            defaults={
                'description': 'Quarterly financial summary report for Q1 2026',
                'client': acme,
                'created_by': planner,
                'status': Deliverable.DRAFT,
            }
        )

        d2, _ = Deliverable.objects.get_or_create(
            title='Annual Compliance Report',
            defaults={
                'description': 'Annual compliance and regulatory report',
                'client': globex,
                'created_by': planner,
                'status': Deliverable.SUBMITTED,
            }
        )

        d3, _ = Deliverable.objects.get_or_create(
            title='Risk Assessment 2026',
            defaults={
                'description': 'Comprehensive risk assessment for fiscal year 2026',
                'client': initech,
                'created_by': planner,
                'status': Deliverable.APPROVED,
            }
        )

        self.stdout.write(self.style.SUCCESS('Created deliverables'))

        # Create approval request for submitted deliverable
        if d2.status == Deliverable.SUBMITTED:
            ar, created = ApprovalRequest.objects.get_or_create(
                deliverable=d2,
                defaults={
                    'requested_by': planner,
                    'status': ApprovalRequest.PENDING,
                }
            )
            if created:
                ApprovalStep.objects.create(
                    approval_request=ar,
                    step_order=1,
                    assigned_role=ApprovalStep.ROLE_APPROVER,
                )

        self.stdout.write(self.style.SUCCESS('Created approval requests'))
        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))
        self.stdout.write('')
        self.stdout.write('Sample credentials:')
        self.stdout.write('  admin / admin123 (Admin)')
        self.stdout.write('  planner / planner123 (Planner)')
        self.stdout.write('  approver / approver123 (Approver)')
        self.stdout.write('  viewer / viewer123 (Viewer)')
