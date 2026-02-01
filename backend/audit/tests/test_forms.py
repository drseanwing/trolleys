"""Tests for audit app forms."""
from django.test import TestCase

from audit.forms import (
    AuditChecksForm, AuditConditionForm, AuditDocumentsForm,
    IssueCreateForm, LocationEditForm,
)
from .factories import create_equipment, create_location, create_service_line


class AuditDocumentsFormTest(TestCase):
    """Tests for AuditDocumentsForm."""

    def test_valid_form(self):
        form = AuditDocumentsForm(data={
            'check_record_status': 'Current',
            'check_guidelines_status': 'Current',
            'bls_poster_present': True,
            'equipment_list_status': 'Current',
        })
        self.assertTrue(form.is_valid())


class AuditConditionFormTest(TestCase):
    """Tests for AuditConditionForm."""

    def test_valid_form(self):
        form = AuditConditionForm(data={
            'is_clean': True,
            'is_working_order': True,
            'issue_type': 'None',
            'issue_description': '',
            'rubber_bands_used': True,
            'o2_tubing_correct': True,
            'inhalo_cylinder_ok': True,
        })
        self.assertTrue(form.is_valid())


class IssueCreateFormTest(TestCase):
    """Tests for IssueCreateForm."""

    def test_valid_form(self):
        location = create_location()
        form = IssueCreateForm(data={
            'location': location.pk,
            'issue_category': 'Equipment',
            'severity': 'Medium',
            'title': 'Missing item',
            'description': 'A required item is missing.',
        })
        self.assertTrue(form.is_valid())

    def test_missing_required_fields(self):
        form = IssueCreateForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('location', form.errors)
        self.assertIn('title', form.errors)
