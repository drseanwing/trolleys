"""
Management command to load seed data from the repository's seed_data/ directory.

Usage:
    python manage.py seed_data
    python manage.py seed_data --flush   # Delete existing data first

Load order:
    1. ServiceLine   (from seed_data/ServiceLine.json)
    2. EquipmentCategory (from seed_data/EquipmentCategory.json)
    3. Equipment     (from seed_data/Equipment.json)
    4. Location      (from seed_data/Location.json)
    5. AuditPeriod   (from seed_data/AuditPeriod.json)
"""

import json
import os
from datetime import date

from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError

from audit.models import (
    AuditPeriod,
    Equipment,
    EquipmentCategory,
    Location,
    ServiceLine,
)


class Command(BaseCommand):
    help = 'Load seed data from the seed_data/ directory into the database.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--flush',
            action='store_true',
            help='Delete existing seed-data records before loading.',
        )

    def handle(self, *args, **options):
        # Resolve the seed_data directory (two levels up from manage.py -> repo root)
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )))
        seed_dir = os.path.join(base_dir, 'seed_data')

        if not os.path.isdir(seed_dir):
            raise CommandError(
                f"Seed data directory not found at: {seed_dir}\n"
                "Make sure you are running from the backend/ directory."
            )

        self.stdout.write(f"Seed data directory: {seed_dir}")

        if options['flush']:
            self.stdout.write(self.style.WARNING('Flushing existing seed data...'))
            AuditPeriod.objects.all().delete()
            Location.objects.all().delete()
            Equipment.objects.all().delete()
            EquipmentCategory.objects.all().delete()
            ServiceLine.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Existing data flushed.'))

        self._load_service_lines(seed_dir)
        self._load_equipment_categories(seed_dir)
        self._load_equipment(seed_dir)
        self._load_locations(seed_dir)
        self._load_audit_periods(seed_dir)

        self.stdout.write(self.style.SUCCESS('\nSeed data loading complete.'))

        # Setup role-based access control groups
        self.stdout.write('\n' + '='*70)
        call_command('setup_roles')
        self.stdout.write('='*70)

    # ------------------------------------------------------------------
    # 1. ServiceLine
    # ------------------------------------------------------------------
    def _load_service_lines(self, seed_dir):
        path = os.path.join(seed_dir, 'ServiceLine.json')
        data = self._read_json(path)
        created = 0
        skipped = 0

        for item in data:
            _, was_created = ServiceLine.objects.get_or_create(
                name=item['Title'],
                defaults={
                    'abbreviation': item.get('Abbreviation', ''),
                    'is_active': item.get('IsActive', True),
                },
            )
            if was_created:
                created += 1
            else:
                skipped += 1

        self.stdout.write(
            f"  ServiceLine: {created} created, {skipped} already existed "
            f"(total {len(data)})"
        )

    # ------------------------------------------------------------------
    # 2. EquipmentCategory
    # ------------------------------------------------------------------
    def _load_equipment_categories(self, seed_dir):
        path = os.path.join(seed_dir, 'EquipmentCategory.json')
        data = self._read_json(path)
        created = 0
        skipped = 0

        for item in data:
            _, was_created = EquipmentCategory.objects.get_or_create(
                category_name=item['Title'],
                defaults={
                    'sort_order': item.get('SortOrder', 0),
                    'description': item.get('Description', ''),
                    'is_active': item.get('IsActive', True),
                },
            )
            if was_created:
                created += 1
            else:
                skipped += 1

        self.stdout.write(
            f"  EquipmentCategory: {created} created, {skipped} already existed "
            f"(total {len(data)})"
        )

    # ------------------------------------------------------------------
    # 3. Equipment
    # ------------------------------------------------------------------
    def _load_equipment(self, seed_dir):
        path = os.path.join(seed_dir, 'Equipment.json')
        data = self._read_json(path)
        created = 0
        skipped = 0
        errors = 0

        for item in data:
            category_name = item.get('Category', '')
            try:
                category = EquipmentCategory.objects.get(
                    category_name=category_name,
                )
            except EquipmentCategory.DoesNotExist:
                self.stderr.write(
                    self.style.ERROR(
                        f"    Category '{category_name}' not found for "
                        f"equipment '{item.get('Title')}'. Skipping."
                    )
                )
                errors += 1
                continue

            defib_type = item.get('DefibrillatorType', 'N/A')
            if defib_type not in ('N/A', 'LIFEPAK_1000_AED', 'LIFEPAK_20_20e'):
                defib_type = 'N/A'

            _, was_created = Equipment.objects.get_or_create(
                item_name=item['Title'],
                category=category,
                required_for_defib_type=defib_type,
                defaults={
                    'short_name': item.get('ShortName', ''),
                    's4hana_code': item.get('S4HANACode', ''),
                    'supplier': item.get('Supplier', ''),
                    'standard_quantity': item.get('StandardQuantity', 1),
                    'is_paediatric_item': item.get('IsPaediatric', False),
                    'requires_expiry_check': item.get('RequiresExpiryCheck', False),
                    'critical_item': item.get('IsCritical', False),
                    'sort_order': item.get('SortOrder', 0),
                    'is_active': item.get('IsActive', True),
                },
            )
            if was_created:
                created += 1
            else:
                skipped += 1

        self.stdout.write(
            f"  Equipment: {created} created, {skipped} already existed, "
            f"{errors} errors (total {len(data)})"
        )

    # ------------------------------------------------------------------
    # 4. Location
    # ------------------------------------------------------------------
    def _load_locations(self, seed_dir):
        path = os.path.join(seed_dir, 'Location.json')
        data = self._read_json(path)
        created = 0
        skipped = 0
        errors = 0

        for item in data:
            service_line_name = item.get('ServiceLine', '')
            try:
                service_line = ServiceLine.objects.get(name=service_line_name)
            except ServiceLine.DoesNotExist:
                self.stderr.write(
                    self.style.ERROR(
                        f"    ServiceLine '{service_line_name}' not found for "
                        f"location '{item.get('Title')}'. Skipping."
                    )
                )
                errors += 1
                continue

            defib_type = item.get('DefibrillatorType', 'LIFEPAK_1000_AED')
            if defib_type not in ('N/A', 'LIFEPAK_1000_AED', 'LIFEPAK_20_20e'):
                defib_type = 'LIFEPAK_1000_AED'

            operating_hours = item.get('OperatingHours', '24_7')
            if operating_hours not in ('24_7', 'Weekday_Business', 'Extended'):
                operating_hours = '24_7'

            trolley_type = item.get('TrolleyType', 'Standard')
            if trolley_type not in ('Standard', 'Paediatric', 'Specialty'):
                trolley_type = 'Standard'

            status = item.get('Status', 'Active')
            if status not in ('Active', 'Inactive', 'Decommissioned'):
                status = 'Active'

            _, was_created = Location.objects.get_or_create(
                department_name=item['Title'],
                defaults={
                    'display_name': item.get('DisplayName', item['Title']),
                    'service_line': service_line,
                    'building': item.get('Building', ''),
                    'level': item.get('Level', ''),
                    'trolley_type': trolley_type,
                    'defibrillator_type': defib_type,
                    'operating_hours': operating_hours,
                    'has_paediatric_box': item.get('HasPaedBox', False),
                    'status': status,
                },
            )
            if was_created:
                created += 1
            else:
                skipped += 1

        self.stdout.write(
            f"  Location: {created} created, {skipped} already existed, "
            f"{errors} errors (total {len(data)})"
        )

    # ------------------------------------------------------------------
    # 5. AuditPeriod
    # ------------------------------------------------------------------
    def _load_audit_periods(self, seed_dir):
        path = os.path.join(seed_dir, 'AuditPeriod.json')
        data = self._read_json(path)
        created = 0
        skipped = 0

        for item in data:
            _, was_created = AuditPeriod.objects.get_or_create(
                period_name=item['Title'],
                defaults={
                    'period_type': 'Monthly',
                    'year': item.get('Year', 2026),
                    'start_date': date.fromisoformat(item['StartDate']),
                    'end_date': date.fromisoformat(item['EndDate']),
                    'audit_deadline': date.fromisoformat(item['AuditDeadline']),
                    'is_active': item.get('IsActive', True),
                    'expected_outside_checks_24_7': item.get(
                        'ExpectedOutsideChecks24_7', 0
                    ),
                    'expected_inside_checks': item.get('ExpectedInsideChecks', 4),
                    'notes': item.get('Notes', ''),
                },
            )
            if was_created:
                created += 1
            else:
                skipped += 1

        self.stdout.write(
            f"  AuditPeriod: {created} created, {skipped} already existed "
            f"(total {len(data)})"
        )

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    @staticmethod
    def _read_json(path):
        """Read and parse a JSON file, returning the parsed list."""
        if not os.path.isfile(path):
            raise CommandError(f"Seed file not found: {path}")
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
