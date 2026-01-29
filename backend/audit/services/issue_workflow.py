"""
Issue state machine and workflow service for the REdI Trolley Audit System.

Implements a 7-state issue lifecycle with SLA-based auto-escalation:
Open -> Assigned -> InProgress -> PendingVerification -> Resolved -> Closed
With Escalated branch and Reopen paths.
"""
from datetime import timedelta
from django.utils import timezone


class InvalidTransitionError(Exception):
    """Raised when an invalid state transition is attempted."""
    pass


class IssueWorkflow:
    """Manage issue state transitions and SLA enforcement."""

    # Valid state transitions: current_state -> set of allowed next states
    TRANSITIONS = {
        'Open': {'Assigned', 'Escalated'},
        'Assigned': {'InProgress', 'Escalated'},
        'InProgress': {'PendingVerification', 'Escalated'},
        'PendingVerification': {'Resolved', 'InProgress'},
        'Resolved': {'Closed', 'Open'},
        'Closed': {'Open'},
        'Escalated': {'Assigned'},
    }

    # SLA targets in hours by severity
    SLA_HOURS = {
        'Critical': 24,
        'High': 72,      # 3 business days
        'Medium': 120,    # 5 business days
        'Low': 240,       # 10 business days
    }

    MAX_ESCALATION_LEVEL = 3

    def can_transition(self, issue, new_status):
        """Check if a state transition is valid."""
        current = issue.status
        allowed = self.TRANSITIONS.get(current, set())
        return new_status in allowed

    def get_available_transitions(self, issue):
        """Return list of valid next states for an issue."""
        return list(self.TRANSITIONS.get(issue.status, set()))

    def transition(self, issue, new_status, user_name='', notes=''):
        """
        Transition an issue to a new status.
        Raises InvalidTransitionError if transition is not allowed.
        """
        if not self.can_transition(issue, new_status):
            raise InvalidTransitionError(
                f"Cannot transition from '{issue.status}' to '{new_status}'. "
                f"Allowed transitions: {self.get_available_transitions(issue)}"
            )

        old_status = issue.status
        now = timezone.now()

        # Apply transition-specific logic
        if new_status == 'Assigned':
            if not issue.assigned_to:
                issue.assigned_to = user_name
            issue.assigned_date = now
            if old_status == 'Escalated':
                pass  # De-escalation, keep escalation_level for tracking

        elif new_status == 'InProgress':
            pass  # No special fields to update

        elif new_status == 'PendingVerification':
            pass  # Work submitted for verification

        elif new_status == 'Resolved':
            issue.resolved_date = now
            if not issue.verified_by:
                issue.verified_by = user_name

        elif new_status == 'Closed':
            issue.closed_date = now

        elif new_status == 'Open':
            # Reopen
            issue.reopen_count += 1
            issue.resolved_date = None
            issue.closed_date = None
            issue.verified_by = ''

        elif new_status == 'Escalated':
            issue.escalation_level += 1

        issue.status = new_status
        issue.save()

        # Add a comment about the transition
        from audit.models import IssueComment
        IssueComment.objects.create(
            issue=issue,
            comment_text=f"Status changed from '{old_status}' to '{new_status}'. {notes}".strip(),
            comment_by=user_name or 'System',
            is_internal=True,
        )

        return issue

    def assign(self, issue, assigned_to, user_name=''):
        """Assign an issue to someone."""
        issue.assigned_to = assigned_to
        return self.transition(issue, 'Assigned', user_name=user_name,
                              notes=f"Assigned to {assigned_to}")

    def start_work(self, issue, user_name=''):
        """Mark issue as in progress."""
        return self.transition(issue, 'InProgress', user_name=user_name)

    def submit_for_verification(self, issue, user_name='', resolution_summary=''):
        """Submit issue fix for verification."""
        if resolution_summary:
            issue.resolution_summary = resolution_summary
        return self.transition(issue, 'PendingVerification', user_name=user_name)

    def verify_and_resolve(self, issue, verified_by):
        """Verify and resolve an issue."""
        issue.verified_by = verified_by
        return self.transition(issue, 'Resolved', user_name=verified_by)

    def reject_verification(self, issue, user_name='', reason=''):
        """Reject verification, send back to in progress."""
        return self.transition(issue, 'InProgress', user_name=user_name,
                              notes=f"Verification rejected: {reason}")

    def close(self, issue, user_name=''):
        """Close a resolved issue."""
        return self.transition(issue, 'Closed', user_name=user_name)

    def reopen(self, issue, user_name='', reason=''):
        """Reopen a resolved or closed issue."""
        return self.transition(issue, 'Open', user_name=user_name,
                              notes=f"Reopened: {reason}")

    def escalate(self, issue, user_name='', reason=''):
        """Escalate an issue."""
        return self.transition(issue, 'Escalated', user_name=user_name,
                              notes=f"Escalated: {reason}")

    def get_sla_target(self, issue):
        """Calculate the SLA target date for an issue based on severity."""
        hours = self.SLA_HOURS.get(issue.severity, 240)
        if issue.reported_date:
            return issue.reported_date + timedelta(hours=hours)
        return None

    def is_sla_breached(self, issue):
        """Check if an issue has breached its SLA."""
        if issue.status in ('Resolved', 'Closed'):
            return False
        target = self.get_sla_target(issue)
        if target is None:
            return False
        return timezone.now() > target

    def check_and_auto_escalate(self, issue):
        """
        Check SLA and auto-escalate if breached.
        Returns True if escalated, False otherwise.
        """
        if not self.is_sla_breached(issue):
            return False

        if issue.status in ('Resolved', 'Closed', 'Escalated'):
            return False

        if self.can_transition(issue, 'Escalated'):
            self.escalate(issue, user_name='System',
                         reason=f"SLA breached ({issue.severity} severity)")
            return True
        return False

    def needs_management_review(self, issue):
        """Check if issue needs management review (escalation >= 3)."""
        return issue.escalation_level >= self.MAX_ESCALATION_LEVEL

    def set_target_resolution_date(self, issue):
        """Set the target resolution date based on SLA."""
        target = self.get_sla_target(issue)
        if target:
            issue.target_resolution_date = target.date()
            issue.save(update_fields=['target_resolution_date'])
