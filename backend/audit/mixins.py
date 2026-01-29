"""
Role-based access control mixins for Django views.

These mixins enforce role-based access at the view level using Django Groups.
Superusers always have access regardless of group membership.

Usage:
    class MyView(EducatorRequiredMixin, View):
        def get(self, request):
            # Only System Admin or MERT Educator can access this
            ...
"""

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class RoleRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Mixin requiring user to be in specific role groups.

    Set required_roles in the subclass to a list of group names.
    Superusers always pass the test.

    Attributes:
        required_roles: List of Django Group names that can access this view
    """

    required_roles = []  # Override in subclass

    def test_func(self):
        """Check if user is superuser or member of required roles."""
        if self.request.user.is_superuser:
            return True
        user_groups = set(self.request.user.groups.values_list('name', flat=True))
        return bool(user_groups.intersection(set(self.required_roles)))


class AdminRequiredMixin(RoleRequiredMixin):
    """Require System Admin role."""

    required_roles = ['System Admin']


class EducatorRequiredMixin(RoleRequiredMixin):
    """Require System Admin or MERT Educator role."""

    required_roles = ['System Admin', 'MERT Educator']


class ManagerRequiredMixin(RoleRequiredMixin):
    """Require System Admin, MERT Educator, or Service Line Manager role."""

    required_roles = ['System Admin', 'MERT Educator', 'Service Line Manager']


class AuditorRequiredMixin(RoleRequiredMixin):
    """Require System Admin, MERT Educator, Service Line Manager, or Auditor role."""

    required_roles = ['System Admin', 'MERT Educator', 'Service Line Manager', 'Auditor']


class ViewerRequiredMixin(RoleRequiredMixin):
    """
    Require any authenticated user with a role.

    All 5 roles (System Admin, MERT Educator, Service Line Manager, Auditor, Viewer)
    can access views with this mixin.
    """

    required_roles = [
        'System Admin',
        'MERT Educator',
        'Service Line Manager',
        'Auditor',
        'Viewer'
    ]
