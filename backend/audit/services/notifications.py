"""
Email notification service for the REdI Trolley Audit System.

Sends notifications for:
1. Audit completion (to service line managers)
2. Issue creation (critical issues to MERT educators)
3. Issue assignment (to assigned person)
4. SLA breach warning (to assigned person and manager)
5. Issue escalation (to management chain)
6. Weekly random selection (to MERT educators)

Supports Power Automate HTTP trigger API and Django SMTP fallback.
"""
import logging

from django.conf import settings
from django.core.mail import send_mail
from django.utils.html import escape, strip_tags

from .email_backend import PowerAutomateEmailService

logger = logging.getLogger(__name__)


class NotificationService:
    """Send email notifications for audit system events."""

    def __init__(self):
        self.subject_prefix = getattr(
            settings, 'EMAIL_SUBJECT_PREFIX', '[REdI] ',
        )
        endpoint = getattr(settings, 'EMAIL_API_ENDPOINT', '')
        if endpoint:
            self._backend = 'power_automate'
            self._pa_service = PowerAutomateEmailService()
        else:
            self._backend = 'django'
            self._pa_service = None

    def _send_email(self, to, subject, body, importance='Normal'):
        """
        Send email using configured backend.

        Args:
            to: Recipient(s) - semicolon-separated string for Power Automate,
                or list of strings for Django mail.
            subject: Email subject.
            body: HTML email body.
            importance: Email importance level.
        """
        if self._backend == 'power_automate' and self._pa_service:
            return self._pa_service.send(
                to=to if isinstance(to, str) else ';'.join(to),
                subject=subject,
                body=body,
                importance=importance,
            )
        else:
            # Use Django's send_mail with SMTP/console backend
            recipient_list = (
                to.split(';') if isinstance(to, str) else to
            )
            recipient_list = [r.strip() for r in recipient_list if r.strip()]
            if not recipient_list:
                logger.warning('No recipients for email: %s', subject)
                return False
            try:
                send_mail(
                    subject=subject,
                    message=strip_tags(body),
                    from_email=getattr(
                        settings, 'DEFAULT_FROM_EMAIL',
                        'redi-noreply@health.qld.gov.au',
                    ),
                    recipient_list=recipient_list,
                    html_message=body,
                    fail_silently=False,
                )
                logger.info('Email sent via Django: %s -> %s', subject, recipient_list)
                return True
            except Exception:
                logger.error(
                    'Failed to send email via Django: %s', subject,
                    exc_info=True,
                )
                return False

    def notify_audit_completed(self, audit):
        """Notify relevant parties that an audit has been completed."""
        subject = f'{self.subject_prefix}Audit Completed: {audit.location.display_name}'
        body = (
            f"<h2>Audit Completed</h2>"
            f"<p><strong>Location:</strong> {escape(audit.location.display_name)}</p>"
            f"<p><strong>Auditor:</strong> {escape(audit.auditor_name)}</p>"
            f"<p><strong>Overall Compliance:</strong> {audit.overall_compliance}%</p>"
            f"<p><strong>Date:</strong> {audit.completed_at}</p>"
        )

        if audit.overall_compliance and audit.overall_compliance < 80:
            body += (
                f"<p style='color: #DC3545; font-weight: bold;'>"
                f"WARNING: Compliance below 80% threshold. Follow-up required.</p>"
            )

        recipients = self._get_service_line_contacts(audit.location.service_line)
        if recipients:
            self._send_email(
                to=';'.join(recipients),
                subject=subject,
                body=body,
            )

    def notify_critical_issue(self, issue):
        """Notify MERT educators of a critical issue."""
        if issue.severity != 'Critical':
            return

        subject = f'{self.subject_prefix}CRITICAL Issue: {issue.title}'
        body = (
            f"<h2>Critical Issue Reported</h2>"
            f"<p><strong>Location:</strong> {escape(issue.location.display_name)}</p>"
            f"<p><strong>Issue:</strong> {escape(issue.issue_number)} - {escape(issue.title)}</p>"
            f"<p><strong>Category:</strong> {escape(issue.issue_category)}</p>"
            f"<p><strong>Description:</strong> {escape(issue.description)}</p>"
            f"<p><strong>Reported by:</strong> {escape(issue.reported_by)}</p>"
            f"<p><strong>SLA Target:</strong> {issue.target_resolution_date}</p>"
        )

        recipients = self._get_educator_emails()
        if recipients:
            self._send_email(
                to=';'.join(recipients),
                subject=subject,
                body=body,
                importance='High',
            )

    def notify_issue_assigned(self, issue):
        """Notify the assigned person about their new issue."""
        subject = f'{self.subject_prefix}Issue Assigned: {issue.issue_number} - {issue.title}'
        body = (
            f"<h2>Issue Assigned to You</h2>"
            f"<p>You have been assigned issue <strong>{escape(issue.issue_number)}</strong></p>"
            f"<p><strong>Location:</strong> {escape(issue.location.display_name)}</p>"
            f"<p><strong>Severity:</strong> {issue.severity}</p>"
            f"<p><strong>Description:</strong> {escape(issue.description)}</p>"
            f"<p><strong>Target Resolution:</strong> {issue.target_resolution_date}</p>"
        )

        from django.contrib.auth import get_user_model
        User = get_user_model()
        try:
            user = User.objects.get(username=issue.assigned_to)
            if user.email:
                self._send_email(
                    to=user.email,
                    subject=subject,
                    body=body,
                )
        except User.DoesNotExist:
            logger.warning(
                'Cannot notify assigned user: %s not found',
                issue.assigned_to,
            )

    def notify_sla_warning(self, issue):
        """Send SLA breach warning."""
        subject = f'{self.subject_prefix}SLA WARNING: {issue.issue_number} - {issue.title}'
        body = (
            f"<h2>SLA Breach Warning</h2>"
            f"<p>SLA breach warning for issue <strong>{escape(issue.issue_number)}</strong></p>"
            f"<p><strong>Location:</strong> {escape(issue.location.display_name)}</p>"
            f"<p><strong>Severity:</strong> {issue.severity}</p>"
            f"<p><strong>Status:</strong> {issue.status}</p>"
            f"<p><strong>Target Date:</strong> {issue.target_resolution_date}</p>"
            f"<p><strong>Escalation Level:</strong> {issue.escalation_level}</p>"
        )

        recipients = self._get_service_line_contacts(issue.location.service_line)
        recipients.extend(self._get_educator_emails())
        recipients = list(set(recipients))

        if recipients:
            self._send_email(
                to=';'.join(recipients),
                subject=subject,
                body=body,
                importance='High',
            )

    def notify_weekly_selection(self, selection):
        """Notify educators about new weekly selection."""
        subject = (
            f'{self.subject_prefix}Weekly Random Selection: '
            f'{selection.week_start_date} - {selection.week_end_date}'
        )

        items = selection.items.select_related(
            'location', 'location__service_line',
        ).order_by('selection_rank')

        trolley_rows = ''.join([
            f"<tr><td>{item.selection_rank}</td>"
            f"<td>{escape(item.location.display_name)}</td>"
            f"<td>{escape(item.location.service_line.abbreviation)}</td>"
            f"<td>{item.priority_score}</td></tr>"
            for item in items
        ])

        body = (
            f"<h2>Weekly Random Audit Selection</h2>"
            f"<p><strong>Week:</strong> {selection.week_start_date} to {selection.week_end_date}</p>"
            f"<p><strong>Generated by:</strong> {escape(selection.generated_by)}</p>"
            f"<p><strong>Trolleys selected:</strong> {items.count()}</p>"
            f"<table border='1' cellpadding='8' cellspacing='0' style='border-collapse: collapse;'>"
            f"<thead><tr><th>Rank</th><th>Location</th><th>Service Line</th><th>Priority</th></tr></thead>"
            f"<tbody>{trolley_rows}</tbody></table>"
        )

        recipients = self._get_educator_emails()
        if recipients:
            self._send_email(
                to=';'.join(recipients),
                subject=subject,
                body=body,
            )

    def _get_service_line_contacts(self, service_line):
        """Get email addresses for a service line."""
        emails = []
        if service_line.contact_email:
            emails.append(service_line.contact_email)
        return emails

    def _get_educator_emails(self):
        """Get email addresses of all MERT educators."""
        from django.contrib.auth.models import Group
        try:
            group = Group.objects.get(name='MERT Educator')
            return list(group.user_set.filter(
                email__isnull=False,
            ).exclude(email='').values_list('email', flat=True))
        except Group.DoesNotExist:
            return []
