"""Custom permission classes."""
from rest_framework import permissions

from .models import User


class IsAdminUser(permissions.BasePermission):
    """Allow access only to admin users."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == User.ADMIN


class IsAdminOrPlanner(permissions.BasePermission):
    """Allow access to admin or planner users."""

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.role in [User.ADMIN, User.PLANNER]


class IsAdminOrApprover(permissions.BasePermission):
    """Allow access to admin or approver users."""

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.role in [User.ADMIN, User.APPROVER]


class IsViewerOrAbove(permissions.BasePermission):
    """Allow access to any authenticated user (all roles)."""

    def has_permission(self, request, view):
        return request.user.is_authenticated
