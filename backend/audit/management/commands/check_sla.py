"""
Management command to check issue SLA compliance and auto-escalate breaches.

Intended to be run periodically (e.g., daily via cron or scheduled task).
Usage: python manage.py check_sla
"""
from django.core.management.base import BaseCommand
from audit.models import Issue
from audit.services.issue_workflow import IssueWorkflow
from audit.services.notifications import NotificationService


class Command(BaseCommand):
    help = 'Check SLA compliance for all open issues and auto-escalate breaches'

    def handle(self, *args, **options):
        workflow = IssueWorkflow()
        notifications = NotificationService()

        # Get all open issues (not resolved or closed)
        open_issues = Issue.objects.exclude(
            status__in=['Resolved', 'Closed']
        ).select_related('location', 'location__service_line')

        escalated_count = 0
        warned_count = 0

        for issue in open_issues:
            if workflow.is_sla_breached(issue):
                # Try to auto-escalate
                if workflow.check_and_auto_escalate(issue):
                    escalated_count += 1
                    notifications.notify_sla_warning(issue)
                    self.stdout.write(
                        self.style.WARNING(
                            f'Escalated: {issue.issue_number} - {issue.title} '
                            f'(severity: {issue.severity}, escalation: {issue.escalation_level})'
                        )
                    )
                else:
                    warned_count += 1
                    self.stdout.write(
                        self.style.NOTICE(
                            f'SLA breached (already escalated): {issue.issue_number}'
                        )
                    )

        self.stdout.write(self.style.SUCCESS(
            f'SLA check complete. Checked: {open_issues.count()}, '
            f'Escalated: {escalated_count}, Warned: {warned_count}'
        ))
