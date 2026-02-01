"""
Test factories for the REdI Trolley Audit System.

Provides helper functions to create test data for models.
Uses Django's ORM directly (no factory_boy dependency).
"""
from datetime import date, timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.utils import timezone

from audit.models import (
    Audit, AuditChecks, AuditCondition, AuditDocuments, AuditEquipment,
    AuditPeriod, Equipment, EquipmentCategory, Issue, Location, ServiceLine,
)

User = get_user_model()


def create_user(username='testuser', password='testpass123', groups=None, **kwargs):
    """Create a test user with optional group membership."""
    defaults = {
        'first_name': 'Test',
        'last_name': 'User',
        'email': f'{username}@test.com',
    }
    defaults.update(kwargs)
    user = User.objects.create_user(username=username, password=password, **defaults)
    if groups:
        for group_name in groups:
            group, _ = Group.objects.get_or_create(name=group_name)
            user.groups.add(group)
    return user


def create_service_line(name='Emergency Medicine', abbreviation='EM', **kwargs):
    """Create a test service line."""
    defaults = {
        'name': name,
        'abbreviation': abbreviation,
        'contact_email': 'em@test.com',
        'is_active': True,
    }
    defaults.update(kwargs)
    return ServiceLine.objects.create(**defaults)


def create_equipment_category(category_name='Airway Equipment', sort_order=1, **kwargs):
    """Create a test equipment category."""
    defaults = {
        'category_name': category_name,
        'sort_order': sort_order,
        'is_active': True,
    }
    defaults.update(kwargs)
    return EquipmentCategory.objects.create(**defaults)


def create_equipment(category=None, item_name='Laryngoscope', **kwargs):
    """Create a test equipment item."""
    if category is None:
        category = create_equipment_category()
    defaults = {
        'category': category,
        'item_name': item_name,
        'standard_quantity': 1,
        'is_active': True,
        'critical_item': False,
        'requires_expiry_check': False,
    }
    defaults.update(kwargs)
    return Equipment.objects.create(**defaults)


def create_location(service_line=None, department_name='Emergency Dept', **kwargs):
    """Create a test location."""
    if service_line is None:
        service_line = create_service_line()
    defaults = {
        'service_line': service_line,
        'department_name': department_name,
        'display_name': department_name,
        'building': 'Block 7',
        'level': 'Level 2',
        'trolley_type': 'Standard',
        'defibrillator_type': 'LIFEPAK_1000_AED',
        'operating_hours': '24_7',
        'status': 'Active',
    }
    defaults.update(kwargs)
    return Location.objects.create(**defaults)


def create_audit_period(**kwargs):
    """Create a test audit period."""
    today = date.today()
    defaults = {
        'period_name': f'Test Period {today.strftime("%B %Y")}',
        'period_type': 'Monthly',
        'year': today.year,
        'start_date': today.replace(day=1),
        'end_date': (today.replace(day=1) + timedelta(days=31)).replace(day=1) - timedelta(days=1),
        'audit_deadline': (today.replace(day=1) + timedelta(days=31)).replace(day=1) - timedelta(days=1),
        'is_active': True,
        'expected_outside_checks_24_7': 28,
        'expected_inside_checks': 4,
    }
    defaults.update(kwargs)
    return AuditPeriod.objects.create(**defaults)


def create_audit(location=None, period=None, user=None, **kwargs):
    """Create a test audit."""
    if location is None:
        location = create_location()
    if period is None:
        period = create_audit_period()
    defaults = {
        'location': location,
        'period': period,
        'auditor_name': 'Test Auditor',
        'auditor_user': user,
        'submission_status': 'InProgress',
    }
    defaults.update(kwargs)
    return Audit.objects.create(**defaults)


def create_audit_documents(audit, **kwargs):
    """Create test audit documents."""
    defaults = {
        'audit': audit,
        'check_record_status': 'Current',
        'check_guidelines_status': 'Current',
        'bls_poster_present': True,
        'equipment_list_status': 'Current',
    }
    defaults.update(kwargs)
    return AuditDocuments.objects.create(**defaults)


def create_audit_condition(audit, **kwargs):
    """Create test audit condition."""
    defaults = {
        'audit': audit,
        'is_clean': True,
        'is_working_order': True,
        'issue_type': 'None',
        'rubber_bands_used': True,
        'o2_tubing_correct': True,
        'inhalo_cylinder_ok': True,
    }
    defaults.update(kwargs)
    return AuditCondition.objects.create(**defaults)


def create_audit_checks(audit, **kwargs):
    """Create test audit checks."""
    defaults = {
        'audit': audit,
        'outside_check_count': 28,
        'inside_check_count': 4,
        'expected_outside': 28,
        'expected_inside': 4,
        'count_not_available': False,
    }
    defaults.update(kwargs)
    return AuditChecks.objects.create(**defaults)


def create_audit_equipment(audit, equipment=None, **kwargs):
    """Create test audit equipment check."""
    if equipment is None:
        equipment = create_equipment()
    defaults = {
        'audit': audit,
        'equipment': equipment,
        'is_present': True,
        'quantity_found': 1,
        'quantity_expected': 1,
        'expiry_ok': True,
    }
    defaults.update(kwargs)
    return AuditEquipment.objects.create(**defaults)


def create_issue(location=None, **kwargs):
    """Create a test issue."""
    if location is None:
        location = create_location()
    defaults = {
        'location': location,
        'issue_category': 'Equipment',
        'severity': 'Medium',
        'title': 'Test Issue',
        'description': 'Test issue description',
        'reported_by': 'Test User',
    }
    defaults.update(kwargs)
    return Issue.objects.create(**defaults)


def setup_all_roles():
    """Create all 5 role groups."""
    role_names = [
        'System Admin',
        'MERT Educator',
        'Service Line Manager',
        'Auditor',
        'Viewer',
    ]
    groups = []
    for name in role_names:
        group, _ = Group.objects.get_or_create(name=name)
        groups.append(group)
    return groups
