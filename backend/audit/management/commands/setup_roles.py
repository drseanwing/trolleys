"""
Management command to create Django Groups for role-based access control.

Usage:
    python manage.py setup_roles

Creates 5 groups with appropriate permissions:
    - System Admin (full access)
    - MERT Educator (manage trolleys, audits, issues, reports)
    - Service Line Manager (manage audits and issues for own service line)
    - Auditor (create and submit audits)
    - Viewer (read-only access)
"""

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from audit.models import (
    Audit,
    AuditChecks,
    AuditCondition,
    AuditDocuments,
    AuditEquipment,
    AuditPeriod,
    CorrectiveAction,
    Equipment,
    EquipmentCategory,
    Issue,
    IssueComment,
    Location,
    LocationChangeLog,
    LocationEquipment,
    RandomAuditSelection,
    RandomAuditSelectionItem,
    ServiceLine,
)


class Command(BaseCommand):
    help = 'Create Django Groups with appropriate permissions for role-based access control.'

    def handle(self, *args, **options):
        self.stdout.write('Setting up role-based access control groups...\n')

        # Create groups with permissions
        self._create_system_admin()
        self._create_mert_educator()
        self._create_service_line_manager()
        self._create_auditor()
        self._create_viewer()

        self.stdout.write(self.style.SUCCESS('\nRole setup complete.'))

    def _get_permissions(self, model, actions):
        """
        Get Permission objects for a given model and list of actions.

        Args:
            model: Django model class
            actions: List of permission actions (e.g., ['view', 'add', 'change', 'delete'])

        Returns:
            List of Permission objects
        """
        content_type = ContentType.objects.get_for_model(model)
        permissions = []
        for action in actions:
            codename = f'{action}_{model._meta.model_name}'
            try:
                perm = Permission.objects.get(content_type=content_type, codename=codename)
                permissions.append(perm)
            except Permission.DoesNotExist:
                self.stderr.write(
                    self.style.WARNING(f"  Permission '{codename}' not found for {model.__name__}")
                )
        return permissions

    def _create_system_admin(self):
        """Create System Admin group with full access to everything."""
        group, created = Group.objects.get_or_create(name='System Admin')

        if created:
            self.stdout.write('  Created group: System Admin')
        else:
            self.stdout.write('  Group already exists: System Admin')
            group.permissions.clear()

        # Full permissions on all audit models
        models = [
            Audit, AuditDocuments, AuditCondition, AuditChecks, AuditEquipment,
            Issue, CorrectiveAction, IssueComment,
            Location, LocationEquipment, LocationChangeLog,
            ServiceLine, EquipmentCategory, Equipment,
            AuditPeriod, RandomAuditSelection, RandomAuditSelectionItem
        ]

        all_perms = []
        for model in models:
            all_perms.extend(self._get_permissions(model, ['view', 'add', 'change', 'delete']))

        group.permissions.set(all_perms)
        self.stdout.write(f'    Assigned {len(all_perms)} permissions')

    def _create_mert_educator(self):
        """Create MERT Educator group with management access."""
        group, created = Group.objects.get_or_create(name='MERT Educator')

        if created:
            self.stdout.write('  Created group: MERT Educator')
        else:
            self.stdout.write('  Group already exists: MERT Educator')
            group.permissions.clear()

        # Full permissions on audit workflow and random selection
        full_access_models = [
            Audit, AuditDocuments, AuditCondition, AuditChecks, AuditEquipment,
            Issue, CorrectiveAction, IssueComment,
            RandomAuditSelection, RandomAuditSelectionItem,
            Location, LocationEquipment, LocationChangeLog
        ]

        # View-only permissions on reference data
        view_only_models = [
            ServiceLine, EquipmentCategory, Equipment, AuditPeriod
        ]

        all_perms = []
        for model in full_access_models:
            all_perms.extend(self._get_permissions(model, ['view', 'add', 'change', 'delete']))

        for model in view_only_models:
            all_perms.extend(self._get_permissions(model, ['view']))

        group.permissions.set(all_perms)
        self.stdout.write(f'    Assigned {len(all_perms)} permissions')

    def _create_service_line_manager(self):
        """Create Service Line Manager group with limited management access."""
        group, created = Group.objects.get_or_create(name='Service Line Manager')

        if created:
            self.stdout.write('  Created group: Service Line Manager')
        else:
            self.stdout.write('  Group already exists: Service Line Manager')
            group.permissions.clear()

        # Can manage audits and issues for their service line
        manage_models = [
            Audit, AuditDocuments, AuditCondition, AuditChecks, AuditEquipment,
            Issue, CorrectiveAction, IssueComment
        ]

        # View-only on reference data
        view_only_models = [
            Location, Equipment, ServiceLine, EquipmentCategory, AuditPeriod,
            LocationEquipment, LocationChangeLog
        ]

        all_perms = []
        for model in manage_models:
            all_perms.extend(self._get_permissions(model, ['view', 'add', 'change']))

        for model in view_only_models:
            all_perms.extend(self._get_permissions(model, ['view']))

        group.permissions.set(all_perms)
        self.stdout.write(f'    Assigned {len(all_perms)} permissions')

    def _create_auditor(self):
        """Create Auditor group with audit creation and issue reporting access."""
        group, created = Group.objects.get_or_create(name='Auditor')

        if created:
            self.stdout.write('  Created group: Auditor')
        else:
            self.stdout.write('  Group already exists: Auditor')
            group.permissions.clear()

        # Can create and edit audits
        audit_models = [
            Audit, AuditDocuments, AuditCondition, AuditChecks, AuditEquipment
        ]

        # Can create issues
        issue_models = [Issue]

        # View-only on reference data
        view_only_models = [
            Location, Equipment, EquipmentCategory, AuditPeriod, ServiceLine,
            CorrectiveAction, IssueComment
        ]

        all_perms = []
        for model in audit_models:
            all_perms.extend(self._get_permissions(model, ['view', 'add', 'change']))

        for model in issue_models:
            all_perms.extend(self._get_permissions(model, ['view', 'add']))

        for model in view_only_models:
            all_perms.extend(self._get_permissions(model, ['view']))

        group.permissions.set(all_perms)
        self.stdout.write(f'    Assigned {len(all_perms)} permissions')

    def _create_viewer(self):
        """Create Viewer group with read-only access."""
        group, created = Group.objects.get_or_create(name='Viewer')

        if created:
            self.stdout.write('  Created group: Viewer')
        else:
            self.stdout.write('  Group already exists: Viewer')
            group.permissions.clear()

        # View-only on all models
        models = [
            Audit, AuditDocuments, AuditCondition, AuditChecks, AuditEquipment,
            Issue, CorrectiveAction, IssueComment,
            Location, LocationEquipment, LocationChangeLog,
            ServiceLine, EquipmentCategory, Equipment,
            AuditPeriod, RandomAuditSelection, RandomAuditSelectionItem
        ]

        all_perms = []
        for model in models:
            all_perms.extend(self._get_permissions(model, ['view']))

        group.permissions.set(all_perms)
        self.stdout.write(f'    Assigned {len(all_perms)} permissions')
