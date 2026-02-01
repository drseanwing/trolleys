"""Tests for audit app services."""
from decimal import Decimal

from django.test import TestCase

from audit.services.compliance import ComplianceScorer
from audit.services.issue_workflow import InvalidTransitionError, IssueWorkflow
from .factories import (
    create_audit, create_audit_checks, create_audit_condition,
    create_audit_documents, create_audit_equipment, create_equipment,
    create_equipment_category, create_issue,
)


class ComplianceScorerTest(TestCase):
    """Tests for ComplianceScorer service."""

    def setUp(self):
        self.scorer = ComplianceScorer()

    def test_documentation_score_all_current(self):
        audit = create_audit()
        docs = create_audit_documents(audit)
        score = self.scorer.calculate_documentation_score(docs)
        self.assertEqual(score, Decimal('100'))

    def test_documentation_score_all_missing(self):
        audit = create_audit()
        docs = create_audit_documents(
            audit,
            check_record_status='Missing',
            check_guidelines_status='Missing',
            bls_poster_present=False,
            equipment_list_status='Missing',
        )
        score = self.scorer.calculate_documentation_score(docs)
        self.assertEqual(score, Decimal('0'))

    def test_condition_score_all_good(self):
        audit = create_audit()
        cond = create_audit_condition(audit)
        score = self.scorer.calculate_condition_score(cond)
        self.assertEqual(score, Decimal('100'))

    def test_condition_score_all_bad(self):
        audit = create_audit()
        cond = create_audit_condition(
            audit,
            is_clean=False,
            is_working_order=False,
            rubber_bands_used=False,
            o2_tubing_correct=False,
            inhalo_cylinder_ok=False,
        )
        score = self.scorer.calculate_condition_score(cond)
        self.assertEqual(score, Decimal('0'))

    def test_check_score_full_compliance(self):
        audit = create_audit()
        checks = create_audit_checks(audit)
        score = self.scorer.calculate_check_score(checks)
        self.assertEqual(score, Decimal('100'))

    def test_check_score_count_not_available(self):
        audit = create_audit()
        checks = create_audit_checks(audit, count_not_available=True)
        score = self.scorer.calculate_check_score(checks)
        self.assertEqual(score, Decimal('0'))

    def test_equipment_score_all_present(self):
        audit = create_audit()
        cat = create_equipment_category()
        equip = create_equipment(category=cat, critical_item=True)
        create_audit_equipment(audit, equipment=equip)
        score = self.scorer.calculate_equipment_score(audit.equipment_checks.all())
        self.assertEqual(score, Decimal('100'))

    def test_equipment_score_critical_missing(self):
        audit = create_audit()
        cat = create_equipment_category()
        equip = create_equipment(category=cat, critical_item=True)
        create_audit_equipment(audit, equipment=equip, is_present=False, quantity_found=0)
        score = self.scorer.calculate_equipment_score(audit.equipment_checks.all())
        # Critical weight is 60%, non-critical is 40% (defaults to 100 when empty)
        expected = Decimal('0') * Decimal('0.60') + Decimal('100') * Decimal('0.40')
        self.assertEqual(score, expected)

    def test_overall_score_calculation(self):
        audit = create_audit()
        create_audit_documents(audit)
        create_audit_condition(audit)
        create_audit_checks(audit)
        cat = create_equipment_category()
        equip = create_equipment(category=cat)
        create_audit_equipment(audit, equipment=equip)
        overall = self.scorer.calculate_overall_score(audit)
        self.assertIsNotNone(overall)
        self.assertGreater(overall, Decimal('0'))
        # Verify scores were persisted
        audit.refresh_from_db()
        self.assertIsNotNone(audit.overall_compliance)
        self.assertIsNotNone(audit.document_score)
        self.assertIsNotNone(audit.equipment_score)
        self.assertIsNotNone(audit.condition_score)
        self.assertIsNotNone(audit.check_score)


class IssueWorkflowTest(TestCase):
    """Tests for IssueWorkflow service."""

    def setUp(self):
        self.workflow = IssueWorkflow()

    def test_initial_status_is_open(self):
        issue = create_issue()
        self.assertEqual(issue.status, 'Open')

    def test_assign_from_open(self):
        issue = create_issue()
        self.workflow.assign(issue, 'John Doe', 'Admin')
        issue.refresh_from_db()
        self.assertEqual(issue.status, 'Assigned')
        self.assertEqual(issue.assigned_to, 'John Doe')

    def test_full_workflow(self):
        issue = create_issue()
        self.workflow.assign(issue, 'Jane', 'Admin')
        self.workflow.start_work(issue, 'Jane')
        self.assertEqual(issue.status, 'InProgress')
        self.workflow.submit_for_verification(issue, 'Jane', 'Fixed it')
        self.assertEqual(issue.status, 'PendingVerification')
        self.workflow.verify_and_resolve(issue, 'Admin')
        self.assertEqual(issue.status, 'Resolved')
        self.workflow.close(issue, 'Admin')
        self.assertEqual(issue.status, 'Closed')

    def test_invalid_transition_raises(self):
        issue = create_issue()
        with self.assertRaises(InvalidTransitionError):
            self.workflow.start_work(issue, 'Admin')  # Can't go Open -> InProgress

    def test_reopen_increments_count(self):
        issue = create_issue()
        self.workflow.assign(issue, 'Jane', 'Admin')
        self.workflow.start_work(issue, 'Jane')
        self.workflow.submit_for_verification(issue, 'Jane')
        self.workflow.verify_and_resolve(issue, 'Admin')
        self.workflow.reopen(issue, 'Admin', 'Not fixed')
        issue.refresh_from_db()
        self.assertEqual(issue.reopen_count, 1)

    def test_escalate_increments_level(self):
        issue = create_issue()
        self.workflow.escalate(issue, 'Admin', 'Urgent')
        issue.refresh_from_db()
        self.assertEqual(issue.escalation_level, 1)
        self.assertEqual(issue.status, 'Escalated')

    def test_sla_target_calculation(self):
        issue = create_issue(severity='Critical')
        target = self.workflow.get_sla_target(issue)
        self.assertIsNotNone(target)

    def test_set_target_resolution_date(self):
        issue = create_issue(severity='High')
        self.workflow.set_target_resolution_date(issue)
        issue.refresh_from_db()
        self.assertIsNotNone(issue.target_resolution_date)
