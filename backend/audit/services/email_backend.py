"""
Email service using Power Automate HTTP trigger API.

Replaces Django SMTP email with direct HTTP POST to a Power Automate
workflow endpoint for sending emails via the organization's shared mailbox.
"""
import logging

import requests
from django.conf import settings

logger = logging.getLogger(__name__)


class PowerAutomateEmailService:
    """Send emails via Power Automate HTTP trigger workflow."""

    def __init__(self):
        self.endpoint = getattr(
            settings,
            'EMAIL_API_ENDPOINT',
            '',
        )
        self.default_from = getattr(
            settings,
            'DEFAULT_FROM_EMAIL',
            'redi-noreply@health.qld.gov.au',
        )
        self.timeout = getattr(settings, 'EMAIL_API_TIMEOUT', 30)

    def send(self, to, subject, body, cc=None, bcc=None,
             importance='Normal', reply_to=None):
        """
        Send an email via Power Automate API.

        Args:
            to: Recipient email address(es), semicolon-separated for multiple.
            subject: Email subject line.
            body: Email body (HTML supported).
            cc: CC recipient(s), semicolon-separated (optional).
            bcc: BCC recipient(s), semicolon-separated (optional).
            importance: Email importance - Low, Normal, High (default: Normal).
            reply_to: Reply-to address (optional).

        Returns:
            True if sent successfully, False otherwise.
        """
        if not self.endpoint:
            logger.warning(
                'EMAIL_API_ENDPOINT not configured. Email not sent: %s',
                subject,
            )
            return False

        payload = {
            'to': to,
            'subject': subject,
            'body': body,
        }

        if cc:
            payload['cc'] = cc
        if bcc:
            payload['bcc'] = bcc
        if importance and importance != 'Normal':
            payload['importance'] = importance
        if reply_to:
            payload['replyTo'] = reply_to

        try:
            response = requests.post(
                self.endpoint,
                json=payload,
                timeout=self.timeout,
            )
            response.raise_for_status()
            logger.info('Email sent successfully: %s -> %s', subject, to)
            return True
        except requests.exceptions.Timeout:
            logger.error(
                'Email API timeout sending to %s: %s', to, subject,
            )
            return False
        except requests.exceptions.RequestException as e:
            logger.error(
                'Failed to send email via Power Automate API: %s '
                '(to=%s, subject=%s)',
                e, to, subject,
            )
            return False
