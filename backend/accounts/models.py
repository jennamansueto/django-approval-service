"""User model with role field."""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Custom user model with role field."""

    ADMIN = 'ADMIN'
    PLANNER = 'PLANNER'
    APPROVER = 'APPROVER'
    VIEWER = 'VIEWER'

    ROLE_CHOICES = (
        (ADMIN, _('Admin')),
        (PLANNER, _('Planner')),
        (APPROVER, _('Approver')),
        (VIEWER, _('Viewer')),
    )

    role = models.CharField(
        _('user role'),
        max_length=20,
        choices=ROLE_CHOICES,
        default=VIEWER,
        help_text=_('The role determines user permissions in the system'),
    )
    is_email_verified = models.BooleanField(
        _('email verified'),
        null=True,
        blank=True,
        default=False,
        help_text=_('Whether the user has verified their email address'),
    )
    notification_preferences = models.BooleanField(
        _('receive notifications'),
        null=True,
        blank=True,
        default=True,
        help_text=_('Whether the user wants to receive email notifications'),
    )

    class Meta:
        db_table = 'users'

    def __str__(self):
        return f"{self.username} ({self.role})"
