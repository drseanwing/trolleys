"""
Management command to create an admin superuser for first-run setup.
"""
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Create an admin superuser and assign to System Admin group'

    def add_arguments(self, parser):
        parser.add_argument('--username', default='admin', help='Admin username')
        parser.add_argument('--email', default='admin@rbwh.qld.gov.au', help='Admin email')
        parser.add_argument('--password', required=True, help='Admin password')

    def handle(self, *args, **options):
        User = get_user_model()
        username = options['username']
        email = options['email']
        password = options['password']

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f'User "{username}" already exists.'))
            return

        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
        )

        # Assign to System Admin group
        group, _ = Group.objects.get_or_create(name='System Admin')
        user.groups.add(group)

        self.stdout.write(self.style.SUCCESS(
            f'Admin user "{username}" created and assigned to System Admin group.',
        ))
