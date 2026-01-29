"""
Forms for the REdI Trolley Audit System.

Provides Django ModelForms for data entry across the audit workflow:
- Location editing
- Audit section forms (documents, condition, checks)
- Issue creation, commenting, assignment, and resolution
"""

from django import forms

from .models import (
    Location, AuditDocuments, AuditCondition, AuditChecks,
    Issue, IssueComment,
)


class LocationEditForm(forms.ModelForm):
    """Form for editing trolley location details."""

    class Meta:
        model = Location
        fields = [
            'department_name', 'display_name', 'building', 'level',
            'service_line', 'trolley_type', 'defibrillator_type',
            'operating_hours', 'has_paediatric_box', 'has_altered_airway',
            'has_specialty_meds', 'status',
        ]
        widgets = {
            'department_name': forms.TextInput(attrs={'class': 'form-control'}),
            'display_name': forms.TextInput(attrs={'class': 'form-control'}),
            'building': forms.TextInput(attrs={'class': 'form-control'}),
            'level': forms.TextInput(attrs={'class': 'form-control'}),
            'service_line': forms.Select(attrs={'class': 'form-select'}),
            'trolley_type': forms.Select(attrs={'class': 'form-select'}),
            'defibrillator_type': forms.Select(attrs={'class': 'form-select'}),
            'operating_hours': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }


class AuditDocumentsForm(forms.ModelForm):
    """Form for the documentation check section of an audit."""

    class Meta:
        model = AuditDocuments
        fields = [
            'check_record_status', 'check_guidelines_status',
            'bls_poster_present', 'equipment_list_status',
        ]
        widgets = {
            'check_record_status': forms.Select(attrs={'class': 'form-select'}),
            'check_guidelines_status': forms.Select(attrs={'class': 'form-select'}),
            'equipment_list_status': forms.Select(attrs={'class': 'form-select'}),
        }


class AuditConditionForm(forms.ModelForm):
    """Form for the physical condition section of an audit."""

    class Meta:
        model = AuditCondition
        fields = [
            'is_clean', 'is_working_order', 'issue_type',
            'issue_description', 'rubber_bands_used',
            'o2_tubing_correct', 'inhalo_cylinder_ok',
        ]
        widgets = {
            'issue_type': forms.Select(attrs={'class': 'form-select'}),
            'issue_description': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 3,
            }),
        }


class AuditChecksForm(forms.ModelForm):
    """Form for the routine checks section of an audit."""

    class Meta:
        model = AuditChecks
        fields = [
            'outside_check_count', 'inside_check_count',
            'expected_outside', 'expected_inside', 'count_not_available',
        ]
        widgets = {
            'outside_check_count': forms.NumberInput(attrs={'class': 'form-control'}),
            'inside_check_count': forms.NumberInput(attrs={'class': 'form-control'}),
            'expected_outside': forms.NumberInput(attrs={'class': 'form-control'}),
            'expected_inside': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class IssueCreateForm(forms.ModelForm):
    """Form for creating a new issue."""

    class Meta:
        model = Issue
        fields = [
            'location', 'issue_category', 'severity', 'title',
            'description', 'equipment',
        ]
        widgets = {
            'location': forms.Select(attrs={'class': 'form-select'}),
            'issue_category': forms.Select(attrs={'class': 'form-select'}),
            'severity': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 4,
            }),
            'equipment': forms.Select(attrs={'class': 'form-select'}),
        }


class IssueCommentForm(forms.ModelForm):
    """Form for adding a comment to an issue."""

    class Meta:
        model = IssueComment
        fields = ['comment_text', 'is_internal']
        widgets = {
            'comment_text': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 3,
            }),
        }


class IssueAssignForm(forms.Form):
    """Simple form for assigning an issue to a person."""

    assigned_to = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )


class IssueResolveForm(forms.Form):
    """Simple form for providing a resolution summary."""

    resolution_summary = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
    )
