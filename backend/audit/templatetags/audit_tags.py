"""
Custom template tags and filters for the REdI Trolley Audit System.

Template tags will be implemented as templates are built out.
"""

from django import template

register = template.Library()


@register.filter
def compliance_class(value):
    """Return a CSS class name based on compliance percentage.

    Usage: {{ audit.overall_compliance|compliance_class }}
    """
    if value is None:
        return 'compliance-unknown'
    try:
        score = float(value)
    except (TypeError, ValueError):
        return 'compliance-unknown'

    if score >= 90:
        return 'compliance-good'
    elif score >= 70:
        return 'compliance-warning'
    else:
        return 'compliance-critical'


@register.filter
def severity_class(value):
    """Return a CSS class name based on issue severity.

    Usage: {{ issue.severity|severity_class }}
    """
    mapping = {
        'Critical': 'severity-critical',
        'High': 'severity-high',
        'Medium': 'severity-medium',
        'Low': 'severity-low',
    }
    return mapping.get(value, 'severity-unknown')
