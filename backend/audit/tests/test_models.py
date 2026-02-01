"""Tests for audit app models."""
from django.test import TestCase

from audit.models import (
    Audit, EquipmentCategory, Issue, Location, ServiceLine,
)
from .factories import (
    create_audit, create_audit_period, create_equipment,
    create_equipment_category, create_issue, create_location,
    create_service_line, create_user,
)


class ServiceLineModelTest(TestCase):
    """Tests for ServiceLine model."""

    def test_str_representation(self):
        sl = create_service_line(name='Emergency Medicine', abbreviation='EM')
        self.assertEqual(str(sl), 'EM - Emergency Medicine')

    def test_default_is_active(self):
        sl = create_service_line()
        self.assertTrue(sl.is_active)

    def test_uuid_primary_key(self):
        sl = create_service_line()
        self.assertIsNotNone(sl.pk)


class EquipmentCategoryModelTest(TestCase):
    """Tests for EquipmentCategory model."""

    def test_str_representation(self):
        cat = create_equipment_category(category_name='Airway Equipment')
        self.assertEqual(str(cat), 'Airway Equipment')

    def test_ordering_by_sort_order(self):
        cat_b = create_equipment_category(category_name='B', sort_order=2)
        cat_a = create_equipment_category(category_name='A', sort_order=1)
        cats = list(EquipmentCategory.objects.all())
        self.assertEqual(cats[0], cat_a)


class EquipmentModelTest(TestCase):
    """Tests for Equipment model."""

    def test_str_representation(self):
        equip = create_equipment(item_name='Laryngoscope')
        self.assertEqual(str(equip), 'Laryngoscope')

    def test_default_quantity(self):
        equip = create_equipment()
        self.assertEqual(equip.standard_quantity, 1)


class LocationModelTest(TestCase):
    """Tests for Location model."""

    def test_str_representation(self):
        loc = create_location(display_name='ED Resus Bay 1')
        self.assertEqual(str(loc), 'ED Resus Bay 1')

    def test_get_absolute_url(self):
        loc = create_location()
        url = loc.get_absolute_url()
        self.assertIn(str(loc.pk), url)

    def test_days_since_last_audit_none(self):
        loc = create_location()
        self.assertIsNone(loc.days_since_last_audit)

    def test_audit_priority_score_never_audited(self):
        loc = create_location()
        self.assertEqual(loc.audit_priority_score, 1000)


class IssueModelTest(TestCase):
    """Tests for Issue model."""

    def test_auto_numbering(self):
        issue = create_issue()
        self.assertTrue(issue.issue_number.startswith('ISS-'))

    def test_sequential_numbering(self):
        loc = create_location()
        issue1 = create_issue(location=loc)
        issue2 = create_issue(location=loc, title='Second Issue')
        # Extract sequence numbers
        seq1 = int(issue1.issue_number.split('-')[-1])
        seq2 = int(issue2.issue_number.split('-')[-1])
        self.assertEqual(seq2, seq1 + 1)

    def test_get_absolute_url(self):
        issue = create_issue()
        url = issue.get_absolute_url()
        self.assertIn(str(issue.pk), url)
