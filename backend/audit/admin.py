"""
Django admin configuration for the REdI Trolley Audit System.

Registers all 17 models with appropriate list displays, filters,
search fields, and inline editing where relationships warrant it.
"""

from django.contrib import admin

from .models import (
    AuditChecks,
    AuditCondition,
    AuditDocuments,
    AuditEquipment,
    AuditPeriod,
    Audit,
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


# ---------------------------------------------------------------------------
# Inline classes
# ---------------------------------------------------------------------------

class LocationEquipmentInline(admin.TabularInline):
    model = LocationEquipment
    extra = 0
    fields = ('equipment', 'is_required', 'custom_quantity', 'notes')


class AuditDocumentsInline(admin.StackedInline):
    model = AuditDocuments
    extra = 0
    max_num = 1


class AuditConditionInline(admin.StackedInline):
    model = AuditCondition
    extra = 0
    max_num = 1


class AuditChecksInline(admin.StackedInline):
    model = AuditChecks
    extra = 0
    max_num = 1


class AuditEquipmentInline(admin.TabularInline):
    model = AuditEquipment
    extra = 0
    fields = (
        'equipment', 'is_present', 'quantity_found',
        'quantity_expected', 'expiry_ok', 'item_notes',
    )


class CorrectiveActionInline(admin.TabularInline):
    model = CorrectiveAction
    extra = 0
    fields = (
        'action_number', 'action_type', 'description',
        'action_taken_by', 'action_date', 'outcome_successful',
    )


class IssueCommentInline(admin.TabularInline):
    model = IssueComment
    extra = 0
    fields = ('comment_text', 'comment_by', 'is_internal')
    readonly_fields = ('comment_date',)


class RandomAuditSelectionItemInline(admin.TabularInline):
    model = RandomAuditSelectionItem
    extra = 0
    fields = (
        'location', 'selection_rank', 'priority_score',
        'days_since_audit', 'audit_status', 'audit', 'skip_reason',
    )


# ---------------------------------------------------------------------------
# Model admin classes
# ---------------------------------------------------------------------------

@admin.register(ServiceLine)
class ServiceLineAdmin(admin.ModelAdmin):
    list_display = ('abbreviation', 'name', 'contact_email', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'abbreviation')


@admin.register(EquipmentCategory)
class EquipmentCategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'sort_order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('category_name',)
    ordering = ('sort_order',)


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = (
        'item_name', 'category', 'standard_quantity',
        'critical_item', 'is_paediatric_item', 'required_for_defib_type',
        'requires_expiry_check', 'is_active',
    )
    list_filter = (
        'category', 'critical_item', 'is_paediatric_item',
        'is_altered_airway_item', 'required_for_defib_type',
        'requires_expiry_check', 'is_active',
    )
    search_fields = ('item_name', 'short_name', 's4hana_code', 'supplier')
    ordering = ('category__sort_order', 'sort_order')


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'display_name', 'service_line', 'building', 'level',
        'trolley_type', 'defibrillator_type', 'operating_hours',
        'has_paediatric_box', 'status', 'last_audit_date',
        'last_audit_compliance',
    )
    list_filter = (
        'service_line', 'trolley_type', 'defibrillator_type',
        'operating_hours', 'has_paediatric_box', 'has_altered_airway',
        'status', 'building',
    )
    search_fields = ('department_name', 'display_name', 'building')
    inlines = [LocationEquipmentInline]


@admin.register(LocationEquipment)
class LocationEquipmentAdmin(admin.ModelAdmin):
    list_display = ('location', 'equipment', 'is_required', 'custom_quantity')
    list_filter = ('is_required',)
    search_fields = (
        'location__display_name', 'equipment__item_name',
    )


@admin.register(LocationChangeLog)
class LocationChangeLogAdmin(admin.ModelAdmin):
    list_display = (
        'location', 'change_type', 'field_changed',
        'changed_by', 'changed_date',
    )
    list_filter = ('change_type', 'changed_date')
    search_fields = ('location__display_name', 'changed_by', 'field_changed')
    readonly_fields = ('changed_date',)


@admin.register(AuditPeriod)
class AuditPeriodAdmin(admin.ModelAdmin):
    list_display = (
        'period_name', 'period_type', 'year',
        'start_date', 'end_date', 'audit_deadline', 'is_active',
    )
    list_filter = ('period_type', 'year', 'is_active')
    search_fields = ('period_name',)


@admin.register(Audit)
class AuditAdmin(admin.ModelAdmin):
    list_display = (
        'location', 'period', 'audit_type', 'auditor_name',
        'submission_status', 'overall_compliance',
        'requires_follow_up', 'started_at', 'completed_at',
    )
    list_filter = (
        'audit_type', 'submission_status', 'requires_follow_up',
        'period', 'location__service_line',
    )
    search_fields = (
        'location__display_name', 'auditor_name', 'notes',
    )
    inlines = [
        AuditDocumentsInline,
        AuditConditionInline,
        AuditChecksInline,
        AuditEquipmentInline,
    ]
    readonly_fields = ('started_at',)


@admin.register(AuditDocuments)
class AuditDocumentsAdmin(admin.ModelAdmin):
    list_display = (
        'audit', 'check_record_status', 'check_guidelines_status',
        'bls_poster_present', 'equipment_list_status',
    )
    list_filter = (
        'check_record_status', 'check_guidelines_status',
        'bls_poster_present', 'equipment_list_status',
    )


@admin.register(AuditCondition)
class AuditConditionAdmin(admin.ModelAdmin):
    list_display = (
        'audit', 'is_clean', 'is_working_order', 'issue_type',
        'rubber_bands_used', 'o2_tubing_correct', 'inhalo_cylinder_ok',
    )
    list_filter = ('is_clean', 'is_working_order', 'issue_type')


@admin.register(AuditChecks)
class AuditChecksAdmin(admin.ModelAdmin):
    list_display = (
        'audit', 'outside_check_count', 'expected_outside',
        'outside_compliance', 'inside_check_count', 'expected_inside',
        'inside_compliance', 'count_not_available',
    )
    list_filter = ('count_not_available',)


@admin.register(AuditEquipment)
class AuditEquipmentAdmin(admin.ModelAdmin):
    list_display = (
        'audit', 'equipment', 'is_present',
        'quantity_found', 'quantity_expected', 'expiry_ok',
    )
    list_filter = ('is_present', 'expiry_ok')
    search_fields = (
        'equipment__item_name', 'audit__location__display_name',
    )


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = (
        'issue_number', 'title', 'location', 'issue_category',
        'severity', 'status', 'reported_by', 'reported_date',
        'assigned_to', 'target_resolution_date',
    )
    list_filter = (
        'issue_category', 'severity', 'status',
        'location__service_line',
    )
    search_fields = (
        'issue_number', 'title', 'description',
        'location__display_name', 'reported_by', 'assigned_to',
    )
    readonly_fields = ('issue_number', 'reported_date')
    inlines = [CorrectiveActionInline, IssueCommentInline]


@admin.register(CorrectiveAction)
class CorrectiveActionAdmin(admin.ModelAdmin):
    list_display = (
        'issue', 'action_number', 'action_type',
        'action_taken_by', 'action_date', 'outcome_successful',
    )
    list_filter = ('action_type', 'outcome_successful')
    search_fields = (
        'issue__issue_number', 'description', 'action_taken_by',
    )


@admin.register(IssueComment)
class IssueCommentAdmin(admin.ModelAdmin):
    list_display = ('issue', 'comment_by', 'comment_date', 'is_internal')
    list_filter = ('is_internal', 'comment_date')
    search_fields = ('comment_text', 'comment_by')
    readonly_fields = ('comment_date',)


@admin.register(RandomAuditSelection)
class RandomAuditSelectionAdmin(admin.ModelAdmin):
    list_display = (
        'week_start_date', 'week_end_date',
        'generated_by', 'generated_date', 'is_active',
    )
    list_filter = ('is_active', 'week_start_date')
    search_fields = ('generated_by',)
    inlines = [RandomAuditSelectionItemInline]


@admin.register(RandomAuditSelectionItem)
class RandomAuditSelectionItemAdmin(admin.ModelAdmin):
    list_display = (
        'selection', 'location', 'selection_rank',
        'priority_score', 'days_since_audit', 'audit_status',
    )
    list_filter = ('audit_status',)
    search_fields = ('location__display_name',)
