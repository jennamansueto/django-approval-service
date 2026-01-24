"""User model with role field."""
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user model with role field."""

    ADMIN = 'ADMIN'
    PLANNER = 'PLANNER'
    APPROVER = 'APPROVER'
    VIEWER = 'VIEWER'

    ROLE_CHOICES = (
        (ADMIN, 'Admin'),
        (PLANNER, 'Planner'),
        (APPROVER, 'Approver'),
        (VIEWER, 'Viewer'),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=VIEWER,
    )

    class Meta:
        db_table = 'users'

    def __str__(self):
        return f"{self.username} ({self.role})"
