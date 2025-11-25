"""
Lunar Cycle Calculator

Calculates lunar phases and determines bullish (green) vs bearish (red) periods
based on moon cycles.
"""

from datetime import datetime, timedelta
import math


class LunarCalculator:
    """
    Calculates lunar phases and trading periods based on moon cycles.

    The lunar cycle is approximately 29.53 days. This calculator determines
    the current phase and whether it's a "green" (bullish) or "red" (bearish)
    period according to the Lunatic Trader methodology.
    """

    # Known new moon reference point (January 6, 2000, 18:14 UTC)
    KNOWN_NEW_MOON = datetime(2000, 1, 6, 18, 14)
    LUNAR_CYCLE_DAYS = 29.53058867  # Average lunar cycle length

    # Phase definitions (in percentage of cycle)
    PHASES = {
        'new_moon': (0, 0.033),
        'waxing_crescent': (0.033, 0.216),
        'first_quarter': (0.216, 0.283),
        'waxing_gibbous': (0.283, 0.466),
        'full_moon': (0.466, 0.533),
        'waning_gibbous': (0.533, 0.716),
        'last_quarter': (0.716, 0.783),
        'waning_crescent': (0.783, 1.0)
    }

    def __init__(self, green_phase_start='new_moon', green_phase_end='full_moon'):
        """
        Initialize the lunar calculator.

        Args:
            green_phase_start: Start of bullish period (default: 'new_moon')
            green_phase_end: End of bullish period (default: 'full_moon')
        """
        self.green_phase_start = green_phase_start
        self.green_phase_end = green_phase_end

    def get_lunar_age(self, date):
        """
        Calculate the age of the moon in days for a given date.

        Args:
            date: datetime object or date string (YYYY-MM-DD)

        Returns:
            float: Days since last new moon (0-29.53)
        """
        if isinstance(date, str):
            date = datetime.strptime(date, '%Y-%m-%d')

        # Calculate days since known new moon
        delta = date - self.KNOWN_NEW_MOON
        days_since_ref = delta.total_seconds() / 86400

        # Calculate lunar age (days into current cycle)
        lunar_age = days_since_ref % self.LUNAR_CYCLE_DAYS

        return lunar_age

    def get_lunar_phase_percent(self, date):
        """
        Get the lunar phase as a percentage of the full cycle.

        Args:
            date: datetime object or date string

        Returns:
            float: Phase percentage (0.0 to 1.0)
        """
        lunar_age = self.get_lunar_age(date)
        return lunar_age / self.LUNAR_CYCLE_DAYS

    def get_phase_name(self, date):
        """
        Get the name of the current lunar phase.

        Args:
            date: datetime object or date string

        Returns:
            str: Phase name (e.g., 'full_moon', 'waxing_crescent')
        """
        phase_percent = self.get_lunar_phase_percent(date)

        for phase_name, (start, end) in self.PHASES.items():
            if start <= phase_percent < end:
                return phase_name

        return 'new_moon'  # Fallback for edge case

    def is_green_period(self, date):
        """
        Determine if the date falls in a "green" (bullish) period.

        According to Lunatic Trader methodology:
        - Green period: New Moon to Full Moon (waxing moon)
        - Red period: Full Moon to New Moon (waning moon)

        Args:
            date: datetime object or date string

        Returns:
            bool: True if in green period, False if in red period
        """
        phase_percent = self.get_lunar_phase_percent(date)

        # Green period is from new moon (0) to full moon (~0.5)
        # Red period is from full moon (~0.5) to new moon (1.0)
        return phase_percent < 0.5

    def get_next_phase_transition(self, date):
        """
        Calculate the next green/red period transition date.

        Args:
            date: datetime object or date string

        Returns:
            tuple: (transition_date, new_period_type)
                  where new_period_type is 'green' or 'red'
        """
        if isinstance(date, str):
            date = datetime.strptime(date, '%Y-%m-%d')

        phase_percent = self.get_lunar_phase_percent(date)
        lunar_age = self.get_lunar_age(date)

        if phase_percent < 0.5:
            # Currently in green period, next transition is to red (full moon)
            days_until_transition = (0.5 * self.LUNAR_CYCLE_DAYS) - lunar_age
            next_period = 'red'
        else:
            # Currently in red period, next transition is to green (new moon)
            days_until_transition = self.LUNAR_CYCLE_DAYS - lunar_age
            next_period = 'green'

        transition_date = date + timedelta(days=days_until_transition)

        return transition_date, next_period

    def get_period_transitions(self, start_date, end_date):
        """
        Get all period transitions between two dates.

        Args:
            start_date: Start date (datetime or string)
            end_date: End date (datetime or string)

        Returns:
            list: List of tuples (date, period_type) for each transition
        """
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date, '%Y-%m-%d')

        transitions = []
        current_date = start_date

        while current_date < end_date:
            transition_date, period_type = self.get_next_phase_transition(current_date)

            if transition_date > end_date:
                break

            transitions.append((transition_date, period_type))
            current_date = transition_date + timedelta(days=1)

        return transitions

    def get_lunar_info(self, date):
        """
        Get comprehensive lunar information for a date.

        Args:
            date: datetime object or date string

        Returns:
            dict: Dictionary with lunar information
        """
        lunar_age = self.get_lunar_age(date)
        phase_percent = self.get_lunar_phase_percent(date)
        phase_name = self.get_phase_name(date)
        is_green = self.is_green_period(date)
        next_transition, next_period = self.get_next_phase_transition(date)

        return {
            'date': date if isinstance(date, datetime) else datetime.strptime(date, '%Y-%m-%d'),
            'lunar_age_days': round(lunar_age, 2),
            'phase_percent': round(phase_percent, 4),
            'phase_name': phase_name,
            'period_type': 'green' if is_green else 'red',
            'next_transition_date': next_transition,
            'next_period_type': next_period
        }
