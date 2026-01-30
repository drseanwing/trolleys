"""
Random audit selection algorithm for the REdI Trolley Audit System.

Implements priority-weighted weekly selection of trolleys:
- Never-audited trolleys get highest priority (1000 points)
- Priority decreases as audit recency increases
- Service line distribution ensures coverage
- Randomness within priority tiers prevents predictability
"""
import random
from collections import defaultdict
from datetime import date, timedelta
from django.utils import timezone
from django.db.models import F, Q


class RandomAuditSelector:
    """Select trolleys for weekly random audit based on priority scoring."""

    DEFAULT_SELECTION_COUNT = 10

    # Priority score tiers (days since last audit -> base points)
    PRIORITY_TIERS = [
        (None, 1000),   # Never audited
        (180, 500),     # > 6 months
        (90, 250),      # > 3 months
        (60, 100),      # > 2 months
        (30, 50),       # > 1 month
        (0, 10),        # Recently audited
    ]

    def calculate_priority_score(self, location):
        """
        Calculate the priority score for a location.

        Returns (score, days_since_audit) tuple.
        """
        if location.last_audit_date is None:
            return 1000, None

        days_since = (timezone.now().date() - location.last_audit_date.date()).days

        base_score = 10  # default for recently audited
        for threshold, score in self.PRIORITY_TIERS:
            if threshold is None:
                continue
            if days_since > threshold:
                base_score = score
                break

        # Add 1 point per day since last audit
        total_score = base_score + days_since
        return total_score, days_since

    def get_scored_locations(self):
        """
        Get all active locations with priority scores.

        Returns list of (location, score, days_since_audit) tuples,
        sorted by score descending.
        """
        from audit.models import Location

        active_locations = Location.objects.filter(
            status='Active'
        ).select_related('service_line')

        scored = []
        for location in active_locations:
            score, days_since = self.calculate_priority_score(location)
            scored.append((location, score, days_since))

        # Sort by score descending, then shuffle within same-score groups
        scored.sort(key=lambda x: x[1], reverse=True)

        return scored

    def apply_service_line_distribution(self, scored_locations, count):
        """
        Select locations ensuring service line distribution.

        Strategy:
        1. Group by service line
        2. Ensure at least 1 from each active service line (if possible)
        3. Fill remaining slots from highest-priority locations
        """
        # Group by service line
        by_service_line = defaultdict(list)
        for loc, score, days in scored_locations:
            by_service_line[loc.service_line.name].append((loc, score, days))

        selected = []
        remaining_pool = list(scored_locations)

        # Phase 1: Select highest-priority from each service line
        for sl_name, sl_locations in sorted(by_service_line.items()):
            if len(selected) >= count:
                break
            if sl_locations:
                # Pick the highest priority from this service line
                best = sl_locations[0]  # Already sorted by score
                selected.append(best)
                remaining_pool.remove(best)

        # Phase 2: Fill remaining slots from highest-priority unselected
        if len(selected) < count:
            # Add randomness: shuffle within score tiers in remaining pool
            remaining_pool = self._shuffle_within_tiers(remaining_pool)

            for item in remaining_pool:
                if len(selected) >= count:
                    break
                if item not in selected:
                    selected.append(item)

        return selected[:count]

    def _shuffle_within_tiers(self, scored_list):
        """Shuffle locations within the same score tier for randomness."""
        if not scored_list:
            return scored_list

        tiers = defaultdict(list)
        for item in scored_list:
            # Group by score (round to nearest 10 for tier grouping)
            tier_key = item[1] // 10
            tiers[tier_key].append(item)

        result = []
        for tier_key in sorted(tiers.keys(), reverse=True):
            tier_items = tiers[tier_key]
            random.shuffle(tier_items)
            result.extend(tier_items)

        return result

    def generate_selection(self, week_start_date=None, generated_by='System',
                          count=None):
        """
        Generate a new weekly random audit selection.

        Args:
            week_start_date: Start of the audit week (defaults to next Monday)
            generated_by: Name of user/system generating the selection
            count: Number of trolleys to select (default: 10)

        Returns:
            RandomAuditSelection instance with items
        """
        from audit.models import RandomAuditSelection, RandomAuditSelectionItem

        if count is None:
            count = self.DEFAULT_SELECTION_COUNT

        if week_start_date is None:
            # Default to next Monday
            today = date.today()
            days_until_monday = (7 - today.weekday()) % 7
            if days_until_monday == 0:
                days_until_monday = 7  # Next Monday, not today
            week_start_date = today + timedelta(days=days_until_monday)

        week_end_date = week_start_date + timedelta(days=6)

        # Get scored locations and select with distribution
        scored = self.get_scored_locations()
        selected = self.apply_service_line_distribution(scored, count)

        # Create the selection record
        selection = RandomAuditSelection.objects.create(
            week_start_date=week_start_date,
            week_end_date=week_end_date,
            generated_by=generated_by,
            selection_criteria=f"Priority-weighted selection of {count} from {len(scored)} active locations",
            is_active=True,
        )

        # Deactivate previous active selections
        RandomAuditSelection.objects.filter(
            is_active=True
        ).exclude(
            pk=selection.pk
        ).update(is_active=False)

        # Create selection items
        for rank, (location, score, days_since) in enumerate(selected, start=1):
            RandomAuditSelectionItem.objects.create(
                selection=selection,
                location=location,
                selection_rank=rank,
                priority_score=score,
                days_since_audit=days_since,
                audit_status='Pending',
            )

        return selection

    def get_active_selection(self):
        """Get the currently active weekly selection."""
        from audit.models import RandomAuditSelection
        return RandomAuditSelection.objects.filter(
            is_active=True
        ).prefetch_related(
            'items__location__service_line'
        ).first()
