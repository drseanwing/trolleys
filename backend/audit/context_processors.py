"""
Context processors for making user role information available in templates.

This context processor adds user role flags to all template contexts,
allowing easy role-based UI adjustments without view logic changes.

Usage in templates:
    {% if is_admin %}
        <a href="{% url 'admin:index' %}">Admin Panel</a>
    {% endif %}

    {% if is_educator %}
        <a href="{% url 'random_selection' %}">Random Selection</a>
    {% endif %}
"""


def user_roles(request):
    """
    Add user role information to template context.

    Returns a dictionary with:
        - user_roles: List of group names the user belongs to
        - is_admin: True if user is superuser or in 'System Admin' group
        - is_educator: True if user has educator-level or higher access
        - is_manager: True if user has manager-level or higher access
        - is_auditor: True if user has auditor-level or higher access
        - is_viewer: True if user has any role

    Args:
        request: Django HttpRequest object

    Returns:
        Dictionary of role information for template context
    """
    if not request.user.is_authenticated:
        return {
            'user_roles': [],
            'is_admin': False,
            'is_educator': False,
            'is_manager': False,
            'is_auditor': False,
            'is_viewer': False
        }

    groups = set(request.user.groups.values_list('name', flat=True))
    is_superuser = request.user.is_superuser

    return {
        'user_roles': list(groups),
        'is_admin': is_superuser or 'System Admin' in groups,
        'is_educator': is_superuser or bool(groups & {'System Admin', 'MERT Educator'}),
        'is_manager': is_superuser or bool(
            groups & {'System Admin', 'MERT Educator', 'Service Line Manager'}
        ),
        'is_auditor': is_superuser or bool(
            groups & {'System Admin', 'MERT Educator', 'Service Line Manager', 'Auditor'}
        ),
        'is_viewer': is_superuser or bool(groups),
    }
