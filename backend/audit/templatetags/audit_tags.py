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


@register.filter
def sla_countdown(issue):
    """Return human-readable SLA countdown for an issue."""
    if not issue.target_resolution_date:
        return 'No SLA set'
    if issue.status in ('Resolved', 'Closed'):
        return 'Resolved'

    from django.utils import timezone
    now = timezone.now().date()
    target = issue.target_resolution_date
    delta = (target - now).days

    if delta < 0:
        return f'Overdue by {abs(delta)}d'
    elif delta == 0:
        return 'Due today'
    elif delta == 1:
        return '1d remaining'
    else:
        return f'{delta}d remaining'


@register.filter
def sla_badge_class(issue):
    """Return Bootstrap badge class based on SLA status."""
    if not issue.target_resolution_date:
        return 'bg-secondary'
    if issue.status in ('Resolved', 'Closed'):
        return 'bg-success'

    from django.utils import timezone
    now = timezone.now().date()
    target = issue.target_resolution_date
    delta = (target - now).days

    if delta < 0:
        return 'bg-danger'
    elif delta <= 1:
        return 'bg-warning text-dark'
    else:
        return 'bg-success'
