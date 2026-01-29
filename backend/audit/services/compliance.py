"""
Compliance scoring algorithm for the REdI Trolley Audit System.

Implements the 4-factor weighted compliance scoring formula:
- Documentation: 25%
- Equipment: 40% (60/40 critical vs non-critical)
- Condition: 15%
- Routine Checks: 20%
"""
from decimal import Decimal, ROUND_HALF_UP


class ComplianceScorer:
    """Calculate compliance scores for trolley audits."""

    # Component weights
    DOCUMENTATION_WEIGHT = Decimal('0.25')
    EQUIPMENT_WEIGHT = Decimal('0.40')
    CONDITION_WEIGHT = Decimal('0.15')
    CHECK_WEIGHT = Decimal('0.20')

    # Equipment sub-weights
    CRITICAL_WEIGHT = Decimal('0.60')
    NON_CRITICAL_WEIGHT = Decimal('0.40')

    def calculate_documentation_score(self, audit_documents):
        """Calculate documentation compliance score (0-100)."""
        # audit_documents is an AuditDocuments model instance
        points = 0
        total = 4

        if audit_documents.check_record_status == 'Current':
            points += 1
        if audit_documents.check_guidelines_status == 'Current':
            points += 1
        if audit_documents.bls_poster_present:
            points += 1
        if audit_documents.equipment_list_status == 'Current':
            points += 1

        return Decimal(points) / Decimal(total) * 100

    def calculate_equipment_score(self, equipment_checks):
        """Calculate equipment compliance score with critical weighting (0-100)."""
        # equipment_checks is a queryset of AuditEquipment, need to join with Equipment
        critical_pass = 0
        critical_total = 0
        non_critical_pass = 0
        non_critical_total = 0

        for check in equipment_checks.select_related('equipment'):
            is_critical = check.equipment.critical_item

            # Determine if item passes
            passes = (
                check.is_present and
                check.quantity_found >= check.quantity_expected
            )
            if check.equipment.requires_expiry_check:
                passes = passes and check.expiry_ok

            if is_critical:
                critical_total += 1
                if passes:
                    critical_pass += 1
            else:
                non_critical_total += 1
                if passes:
                    non_critical_pass += 1

        critical_score = (
            Decimal(critical_pass) / Decimal(critical_total) * 100
            if critical_total > 0 else Decimal('100')
        )
        non_critical_score = (
            Decimal(non_critical_pass) / Decimal(non_critical_total) * 100
            if non_critical_total > 0 else Decimal('100')
        )

        return (critical_score * self.CRITICAL_WEIGHT) + (non_critical_score * self.NON_CRITICAL_WEIGHT)

    def calculate_condition_score(self, audit_condition):
        """Calculate physical condition compliance score (0-100)."""
        points = 0
        total = 5

        if audit_condition.is_clean:
            points += 1
        if audit_condition.is_working_order:
            points += 1
        if audit_condition.rubber_bands_used:
            points += 1
        if audit_condition.o2_tubing_correct:
            points += 1
        if audit_condition.inhalo_cylinder_ok:
            points += 1

        return Decimal(points) / Decimal(total) * 100

    def calculate_check_score(self, audit_checks):
        """Calculate routine check compliance score (0-100)."""
        if audit_checks.count_not_available:
            return Decimal('0')

        if audit_checks.expected_outside > 0:
            outside_compliance = min(
                Decimal(audit_checks.outside_check_count) / Decimal(audit_checks.expected_outside),
                Decimal('1')
            ) * 100
        else:
            outside_compliance = Decimal('100')

        if audit_checks.expected_inside > 0:
            inside_compliance = min(
                Decimal(audit_checks.inside_check_count) / Decimal(audit_checks.expected_inside),
                Decimal('1')
            ) * 100
        else:
            inside_compliance = Decimal('100')

        return (outside_compliance * Decimal('0.5')) + (inside_compliance * Decimal('0.5'))

    def calculate_overall_score(self, audit):
        """
        Calculate overall compliance score for an audit.
        Updates the audit instance with all component scores and overall score.
        Returns the overall score.

        Args:
            audit: An Audit model instance with related documents, condition, checks,
                   and equipment_checks loaded
        """
        # Calculate each component
        doc_score = Decimal('0')
        equip_score = Decimal('0')
        cond_score = Decimal('0')
        check_score = Decimal('0')

        try:
            doc_score = self.calculate_documentation_score(audit.documents)
        except Exception:
            pass  # AuditDocuments may not exist yet

        equip_score = self.calculate_equipment_score(audit.equipment_checks.all())

        try:
            cond_score = self.calculate_condition_score(audit.condition)
        except Exception:
            pass  # AuditCondition may not exist yet

        try:
            check_score = self.calculate_check_score(audit.checks)
        except Exception:
            pass  # AuditChecks may not exist yet

        # Calculate overall weighted score
        overall = (
            doc_score * self.DOCUMENTATION_WEIGHT +
            equip_score * self.EQUIPMENT_WEIGHT +
            cond_score * self.CONDITION_WEIGHT +
            check_score * self.CHECK_WEIGHT
        )

        # Round to 2 decimal places
        overall = overall.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        doc_score = doc_score.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        equip_score = equip_score.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        cond_score = cond_score.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        check_score = check_score.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        # Update audit instance
        audit.document_score = doc_score
        audit.equipment_score = equip_score
        audit.condition_score = cond_score
        audit.check_score = check_score
        audit.overall_compliance = overall
        audit.save(update_fields=[
            'document_score', 'equipment_score', 'condition_score',
            'check_score', 'overall_compliance'
        ])

        return overall
