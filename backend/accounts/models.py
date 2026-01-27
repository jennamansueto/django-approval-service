"""User model with role field."""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class User(AbstractUser):
    """Custom user model with role field."""

    ADMIN = 'ADMIN'
    PLANNER = 'PLANNER'
    APPROVER = 'APPROVER'
    VIEWER = 'VIEWER'

    ROLE_CHOICES = (
        (ADMIN, _(u'Admin')),
        (PLANNER, _(u'Planner')),
        (APPROVER, _(u'Approver')),
        (VIEWER, _(u'Viewer')),
    )

    role = models.CharField(
        _(u'user role'),
        max_length=20,
        choices=ROLE_CHOICES,
        default=VIEWER,
        help_text=_(u'The role determines user permissions in the system'),
    )
    is_email_verified = models.NullBooleanField(
        _(u'email verified'),
        default=False,
        help_text=_(u'Whether the user has verified their email address'),
    )
    notification_preferences = models.NullBooleanField(
        _(u'receive notifications'),
        default=True,
        help_text=_(u'Whether the user wants to receive email notifications'),
    )

    class Meta:
        db_table = 'users'

    def __str__(self):
        return f"{self.username} ({self.role})"
