"""User model with role field."""
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user model with role field."""

    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        PLANNER = 'PLANNER', 'Planner'
        APPROVER = 'APPROVER', 'Approver'
        VIEWER = 'VIEWER', 'Viewer'

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.VIEWER,
    )

    class Meta:
        db_table = 'users'

    def __str__(self):
        return f"{self.username} ({self.role})"
