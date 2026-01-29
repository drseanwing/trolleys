"""
Models for the REdI (Resuscitation Education Initiative) Trolley Audit System.

Royal Brisbane and Women's Hospital - 17 Django models covering:
- Reference data (ServiceLine, EquipmentCategory, Equipment)
- Location management (Location, LocationEquipment, LocationChangeLog)
- Audit workflow (AuditPeriod, Audit, AuditDocuments, AuditCondition, AuditChecks, AuditEquipment)
- Issue tracking (Issue, CorrectiveAction, IssueComment)
- Random selection (RandomAuditSelection, RandomAuditSelectionItem)
"""

import uuid

from django.conf import settings
from django.db import models
from django.utils import timezone


# ---------------------------------------------------------------------------
# Shared choice constants
# ---------------------------------------------------------------------------

DEFIB_CHOICES = [
    ('N/A', 'N/A'),
    ('LIFEPAK_1000_AED', 'LIFEPAK 1000 AED'),
    ('LIFEPAK_20_20e', 'LIFEPAK 20/20e'),
]


# ===========================================================================
# 1. ServiceLine
# ===========================================================================

class ServiceLine(models.Model):
    """Hospital service line / division that owns trolley locations."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    abbreviation = models.CharField(max_length=20)
    contact_email = models.EmailField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Service Line'
        verbose_name_plural = 'Service Lines'

    def __str__(self):
        return f"{self.abbreviation} - {self.name}"


# ===========================================================================
# 2. EquipmentCategory
# ===========================================================================

class EquipmentCategory(models.Model):
    """Category grouping for trolley equipment (e.g. drawer, top of trolley)."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category_name = models.CharField(max_length=200)
    sort_order = models.IntegerField(default=0)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['sort_order']
        verbose_name = 'Equipment Category'
        verbose_name_plural = 'Equipment Categories'

    def __str__(self):
        return self.category_name


# ===========================================================================
# 3. Equipment
# ===========================================================================

class Equipment(models.Model):
    """Individual equipment item that should be present on a resuscitation trolley."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey(
        EquipmentCategory,
        on_delete=models.CASCADE,
        related_name='equipment',
    )
    item_name = models.CharField(max_length=300)
    short_name = models.CharField(max_length=100, blank=True)
    s4hana_code = models.CharField(max_length=50, blank=True, verbose_name='S/4HANA Code')
    supplier = models.CharField(max_length=200, blank=True)
    standard_quantity = models.PositiveIntegerField(default=1)
    is_standard_item = models.BooleanField(default=True)
    is_paediatric_item = models.BooleanField(default=False)
    is_altered_airway_item = models.BooleanField(default=False)
    required_for_defib_type = models.CharField(
        max_length=30,
        choices=DEFIB_CHOICES,
        default='N/A',
    )
    requires_expiry_check = models.BooleanField(default=False)
    critical_item = models.BooleanField(default=False)
    sort_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['category__sort_order', 'sort_order']
        verbose_name = 'Equipment'
        verbose_name_plural = 'Equipment'

    def __str__(self):
        return self.item_name


# ===========================================================================
# 4. Location
# ===========================================================================

class Location(models.Model):
    """A physical trolley location within the hospital."""

    TROLLEY_TYPE_CHOICES = [
        ('Standard', 'Standard'),
        ('Paediatric', 'Paediatric'),
        ('Specialty', 'Specialty'),
    ]

    OPERATING_HOURS_CHOICES = [
        ('24_7', '24/7'),
        ('Weekday_Business', 'Weekday Business Hours'),
        ('Extended', 'Extended Hours'),
    ]

    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
        ('Decommissioned', 'Decommissioned'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    service_line = models.ForeignKey(
        ServiceLine,
        on_delete=models.PROTECT,
        related_name='locations',
    )
    department_name = models.CharField(max_length=300)
    display_name = models.CharField(max_length=300)
    building = models.CharField(max_length=200)
    level = models.CharField(max_length=100)
    trolley_type = models.CharField(
        max_length=30,
        choices=TROLLEY_TYPE_CHOICES,
        default='Standard',
    )
    defibrillator_type = models.CharField(
        max_length=30,
        choices=DEFIB_CHOICES,
        default='LIFEPAK_1000_AED',
    )
    operating_hours = models.CharField(
        max_length=30,
        choices=OPERATING_HOURS_CHOICES,
        default='24_7',
    )
    has_paediatric_box = models.BooleanField(default=False)
    has_altered_airway = models.BooleanField(default=False)
    has_specialty_meds = models.BooleanField(default=False)
    last_audit_date = models.DateTimeField(null=True, blank=True)
    last_audit_compliance = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Active',
    )
    status_change_date = models.DateTimeField(null=True, blank=True)
    status_change_reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['department_name']
        verbose_name = 'Location'
        verbose_name_plural = 'Locations'

    def __str__(self):
        return self.display_name

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('audit:trolley_detail', kwargs={'pk': self.pk})

    @property
    def days_since_last_audit(self):
        """Number of days since the last audit was completed at this location."""
        if self.last_audit_date is None:
            return None
        delta = timezone.now() - self.last_audit_date
        return delta.days

    @property
    def audit_priority_score(self):
        """Priority score for random audit selection. Higher = more urgent."""
        if self.last_audit_date is None:
            return 1000
        days = self.days_since_last_audit
        if days is None:
            return 1000
        return days


# ===========================================================================
# 5. LocationEquipment
# ===========================================================================

class LocationEquipment(models.Model):
    """Per-location equipment overrides (custom quantities or exclusions)."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        related_name='equipment_overrides',
    )
    equipment = models.ForeignKey(
        Equipment,
        on_delete=models.CASCADE,
        related_name='location_overrides',
    )
    is_required = models.BooleanField(default=True)
    custom_quantity = models.PositiveIntegerField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['location', 'equipment']
        verbose_name = 'Location Equipment Override'
        verbose_name_plural = 'Location Equipment Overrides'

    def __str__(self):
        return f"{self.location} - {self.equipment}"


# ===========================================================================
# 6. LocationChangeLog
# ===========================================================================

class LocationChangeLog(models.Model):
    """Audit trail for changes made to location records."""

    CHANGE_TYPE_CHOICES = [
        ('Created', 'Created'),
        ('Updated', 'Updated'),
        ('StatusChange', 'Status Change'),
        ('Decommissioned', 'Decommissioned'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        related_name='change_logs',
    )
    change_type = models.CharField(max_length=30, choices=CHANGE_TYPE_CHOICES)
    field_changed = models.CharField(max_length=100)
    old_value = models.TextField(blank=True)
    new_value = models.TextField(blank=True)
    change_reason = models.TextField(blank=True)
    changed_by = models.CharField(max_length=200)
    changed_date = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-changed_date']
        verbose_name = 'Location Change Log'
        verbose_name_plural = 'Location Change Logs'

    def __str__(self):
        return f"{self.location} - {self.change_type} ({self.changed_date})"


# ===========================================================================
# 7. AuditPeriod
# ===========================================================================

class AuditPeriod(models.Model):
    """Time period within which audits are expected to be completed."""

    PERIOD_TYPE_CHOICES = [
        ('Monthly', 'Monthly'),
        ('Quarterly', 'Quarterly'),
        ('Annual', 'Annual'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    period_name = models.CharField(max_length=200)
    period_type = models.CharField(
        max_length=20,
        choices=PERIOD_TYPE_CHOICES,
        default='Monthly',
    )
    year = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    audit_deadline = models.DateField()
    is_active = models.BooleanField(default=True)
    expected_outside_checks_24_7 = models.PositiveIntegerField(default=0)
    expected_inside_checks = models.PositiveIntegerField(default=4)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-year', '-start_date']
        verbose_name = 'Audit Period'
        verbose_name_plural = 'Audit Periods'

    def __str__(self):
        return self.period_name


# ===========================================================================
# 8. Audit
# ===========================================================================

class Audit(models.Model):
    """A single audit performed on a trolley location."""

    AUDIT_TYPE_CHOICES = [
        ('Monthly', 'Monthly'),
        ('Random', 'Random'),
        ('FollowUp', 'Follow-Up'),
        ('Spot', 'Spot Check'),
    ]

    SUBMISSION_STATUS_CHOICES = [
        ('Draft', 'Draft'),
        ('InProgress', 'In Progress'),
        ('Submitted', 'Submitted'),
        ('Reviewed', 'Reviewed'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    location = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        related_name='audits',
    )
    period = models.ForeignKey(
        AuditPeriod,
        on_delete=models.PROTECT,
        related_name='audits',
    )
    audit_type = models.CharField(
        max_length=20,
        choices=AUDIT_TYPE_CHOICES,
        default='Monthly',
    )
    triggered_by_issue = models.ForeignKey(
        'Issue',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='triggered_audits',
    )
    auditor_name = models.CharField(max_length=200)
    auditor_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='audits',
    )
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    submission_status = models.CharField(
        max_length=20,
        choices=SUBMISSION_STATUS_CHOICES,
        default='Draft',
    )
    overall_compliance = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True,
    )
    document_score = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True,
    )
    equipment_score = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True,
    )
    condition_score = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True,
    )
    check_score = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True,
    )
    requires_follow_up = models.BooleanField(default=False)
    follow_up_due_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-started_at']
        verbose_name = 'Audit'
        verbose_name_plural = 'Audits'

    def __str__(self):
        date_str = self.started_at.strftime('%Y-%m-%d') if self.started_at else 'Draft'
        return f"Audit {self.location} - {date_str}"


# ===========================================================================
# 9. AuditDocuments
# ===========================================================================

class AuditDocuments(models.Model):
    """Documentation checks performed during an audit."""

    DOC_STATUS_CHOICES = [
        ('Current', 'Current'),
        ('Expired', 'Expired'),
        ('Missing', 'Missing'),
        ('N/A', 'Not Applicable'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    audit = models.OneToOneField(
        Audit,
        on_delete=models.CASCADE,
        related_name='documents',
    )
    check_record_status = models.CharField(
        max_length=20,
        choices=DOC_STATUS_CHOICES,
        default='Missing',
    )
    check_guidelines_status = models.CharField(
        max_length=20,
        choices=DOC_STATUS_CHOICES,
        default='Missing',
    )
    bls_poster_present = models.BooleanField(default=False)
    equipment_list_status = models.CharField(
        max_length=20,
        choices=DOC_STATUS_CHOICES,
        default='Missing',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Audit Documents'
        verbose_name_plural = 'Audit Documents'

    def __str__(self):
        return f"Documents for {self.audit}"


# ===========================================================================
# 10. AuditCondition
# ===========================================================================

class AuditCondition(models.Model):
    """Physical condition assessment of the trolley during an audit."""

    ISSUE_TYPE_CHOICES = [
        ('None', 'None'),
        ('Cleanliness', 'Cleanliness'),
        ('Damage', 'Damage'),
        ('Missing', 'Missing Component'),
        ('Other', 'Other'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    audit = models.OneToOneField(
        Audit,
        on_delete=models.CASCADE,
        related_name='condition',
    )
    is_clean = models.BooleanField(default=False)
    is_working_order = models.BooleanField(default=False)
    issue_type = models.CharField(
        max_length=30,
        choices=ISSUE_TYPE_CHOICES,
        default='None',
    )
    issue_description = models.TextField(blank=True)
    rubber_bands_used = models.BooleanField(default=False)
    o2_tubing_correct = models.BooleanField(
        default=False,
        verbose_name='O2 Tubing Correct',
    )
    inhalo_cylinder_ok = models.BooleanField(
        default=False,
        verbose_name='INHALO Cylinder OK',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Audit Condition'
        verbose_name_plural = 'Audit Conditions'

    def __str__(self):
        return f"Condition for {self.audit}"


# ===========================================================================
# 11. AuditChecks
# ===========================================================================

class AuditChecks(models.Model):
    """Daily/weekly check count compliance recorded during an audit."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    audit = models.OneToOneField(
        Audit,
        on_delete=models.CASCADE,
        related_name='checks',
    )
    outside_check_count = models.PositiveIntegerField(default=0)
    inside_check_count = models.PositiveIntegerField(default=0)
    expected_outside = models.PositiveIntegerField(default=0)
    expected_inside = models.PositiveIntegerField(default=0)
    count_not_available = models.BooleanField(default=False)
    outside_compliance = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True,
    )
    inside_compliance = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Audit Checks'
        verbose_name_plural = 'Audit Checks'

    def __str__(self):
        return f"Checks for {self.audit}"


# ===========================================================================
# 12. AuditEquipment
# ===========================================================================

class AuditEquipment(models.Model):
    """Result of checking a single equipment item during an audit."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    audit = models.ForeignKey(
        Audit,
        on_delete=models.CASCADE,
        related_name='equipment_checks',
    )
    equipment = models.ForeignKey(
        Equipment,
        on_delete=models.PROTECT,
        related_name='audit_checks',
    )
    is_present = models.BooleanField(default=False)
    quantity_found = models.PositiveIntegerField(default=0)
    quantity_expected = models.PositiveIntegerField(default=0)
    expiry_ok = models.BooleanField(default=True)
    item_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['audit', 'equipment']
        verbose_name = 'Audit Equipment Check'
        verbose_name_plural = 'Audit Equipment Checks'

    def __str__(self):
        return f"{self.equipment} in {self.audit}"


# ===========================================================================
# 13. Issue
# ===========================================================================

class Issue(models.Model):
    """A problem found during an audit or reported independently."""

    CATEGORY_CHOICES = [
        ('Equipment', 'Equipment'),
        ('Documentation', 'Documentation'),
        ('Condition', 'Condition'),
        ('Compliance', 'Compliance'),
        ('Process', 'Process'),
        ('Other', 'Other'),
    ]

    SEVERITY_CHOICES = [
        ('Critical', 'Critical'),
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low'),
    ]

    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('Assigned', 'Assigned'),
        ('InProgress', 'In Progress'),
        ('PendingVerification', 'Pending Verification'),
        ('Resolved', 'Resolved'),
        ('Closed', 'Closed'),
        ('Escalated', 'Escalated'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    location = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        related_name='issues',
    )
    audit = models.ForeignKey(
        Audit,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='issues',
    )
    issue_number = models.CharField(max_length=20, unique=True, blank=True)
    issue_category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    severity = models.CharField(
        max_length=20,
        choices=SEVERITY_CHOICES,
        default='Medium',
    )
    title = models.CharField(max_length=300)
    description = models.TextField()
    equipment = models.ForeignKey(
        Equipment,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='issues',
    )
    reported_by = models.CharField(max_length=200)
    reported_date = models.DateTimeField(auto_now_add=True)
    assigned_to = models.CharField(max_length=200, blank=True)
    assigned_date = models.DateTimeField(null=True, blank=True)
    target_resolution_date = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default='Open',
    )
    resolution_summary = models.TextField(blank=True)
    resolved_date = models.DateTimeField(null=True, blank=True)
    verified_by = models.CharField(max_length=200, blank=True)
    closed_date = models.DateTimeField(null=True, blank=True)
    reopen_count = models.PositiveIntegerField(default=0)
    escalation_level = models.PositiveIntegerField(default=0)
    linked_follow_up_audit = models.ForeignKey(
        Audit,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='follow_up_for_issues',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-reported_date']
        verbose_name = 'Issue'
        verbose_name_plural = 'Issues'

    def __str__(self):
        return f"{self.issue_number} - {self.title}"

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('audit:issue_detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        if not self.issue_number:
            now = timezone.now()
            prefix = f"ISS-{now.strftime('%Y%m')}-"
            last_issue = (
                Issue.objects
                .filter(issue_number__startswith=prefix)
                .order_by('-issue_number')
                .first()
            )
            if last_issue:
                try:
                    last_seq = int(last_issue.issue_number.split('-')[-1])
                except (ValueError, IndexError):
                    last_seq = 0
                seq = last_seq + 1
            else:
                seq = 1
            self.issue_number = f"{prefix}{seq:03d}"
        super().save(*args, **kwargs)


# ===========================================================================
# 14. CorrectiveAction
# ===========================================================================

class CorrectiveAction(models.Model):
    """An action taken to resolve an issue."""

    ACTION_TYPE_CHOICES = [
        ('Replacement', 'Replacement'),
        ('Repair', 'Repair'),
        ('Restock', 'Restock'),
        ('ProcessChange', 'Process Change'),
        ('Training', 'Training'),
        ('Other', 'Other'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    issue = models.ForeignKey(
        Issue,
        on_delete=models.CASCADE,
        related_name='corrective_actions',
    )
    action_number = models.PositiveIntegerField()
    action_type = models.CharField(max_length=30, choices=ACTION_TYPE_CHOICES)
    description = models.TextField()
    action_taken_by = models.CharField(max_length=200)
    action_date = models.DateTimeField()
    outcome_description = models.TextField(blank=True)
    outcome_successful = models.BooleanField(default=False)
    evidence_attached = models.BooleanField(default=False)
    evidence_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['action_number']
        verbose_name = 'Corrective Action'
        verbose_name_plural = 'Corrective Actions'

    def __str__(self):
        return f"Action {self.action_number} for {self.issue}"


# ===========================================================================
# 15. IssueComment
# ===========================================================================

class IssueComment(models.Model):
    """A comment or note attached to an issue."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    issue = models.ForeignKey(
        Issue,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    comment_text = models.TextField()
    comment_by = models.CharField(max_length=200)
    comment_date = models.DateTimeField(auto_now_add=True)
    is_internal = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['comment_date']
        verbose_name = 'Issue Comment'
        verbose_name_plural = 'Issue Comments'

    def __str__(self):
        return f"Comment by {self.comment_by} on {self.issue}"


# ===========================================================================
# 16. RandomAuditSelection
# ===========================================================================

class RandomAuditSelection(models.Model):
    """A weekly random audit selection batch."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    week_start_date = models.DateField()
    week_end_date = models.DateField()
    generated_date = models.DateTimeField(auto_now_add=True)
    generated_by = models.CharField(max_length=200)
    selection_criteria = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-week_start_date']
        verbose_name = 'Random Audit Selection'
        verbose_name_plural = 'Random Audit Selections'

    def __str__(self):
        return f"Selection {self.week_start_date} to {self.week_end_date}"


# ===========================================================================
# 17. RandomAuditSelectionItem
# ===========================================================================

class RandomAuditSelectionItem(models.Model):
    """An individual location selected for a random audit."""

    AUDIT_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Skipped', 'Skipped'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    selection = models.ForeignKey(
        RandomAuditSelection,
        on_delete=models.CASCADE,
        related_name='items',
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        related_name='random_selections',
    )
    selection_rank = models.PositiveIntegerField()
    priority_score = models.IntegerField(default=0)
    days_since_audit = models.IntegerField(null=True, blank=True)
    audit_status = models.CharField(
        max_length=20,
        choices=AUDIT_STATUS_CHOICES,
        default='Pending',
    )
    audit = models.ForeignKey(
        Audit,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='selection_items',
    )
    skip_reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['selection_rank']
        unique_together = ['selection', 'location']
        verbose_name = 'Random Audit Selection Item'
        verbose_name_plural = 'Random Audit Selection Items'

    def __str__(self):
        return f"Rank {self.selection_rank}: {self.location}"
