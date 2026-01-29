"""
Management command to generate the weekly random audit selection.

Intended to be run weekly (e.g., every Monday via cron).
Usage: python manage.py generate_weekly_selection [--count N]
"""
from django.core.management.base import BaseCommand
from audit.services.random_selection import RandomAuditSelector
from audit.services.notifications import NotificationService


class Command(BaseCommand):
    help = 'Generate weekly random audit selection'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count', type=int, default=10,
            help='Number of trolleys to select (default: 10)'
        )

    def handle(self, *args, **options):
        count = options['count']

        selector = RandomAuditSelector()
        selection = selector.generate_selection(
            generated_by='System (scheduled)',
            count=count,
        )

        items = selection.items.select_related(
            'location', 'location__service_line'
        ).order_by('selection_rank')

        self.stdout.write(self.style.SUCCESS(
            f'Generated selection for week {selection.week_start_date} to {selection.week_end_date}'
        ))
        self.stdout.write(f'Selected {items.count()} trolleys:')

        for item in items:
            self.stdout.write(
                f'  {item.selection_rank}. {item.location.display_name} '
                f'({item.location.service_line.abbreviation}) - '
                f'Priority: {item.priority_score}, '
                f'Days since audit: {item.days_since_audit or "Never"}'
            )

        # Send notification
        notifications = NotificationService()
        notifications.notify_weekly_selection(selection)

        self.stdout.write(self.style.SUCCESS('Notification sent to MERT educators.'))
