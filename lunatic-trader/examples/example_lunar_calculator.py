"""
Example: Using the Lunar Calculator

This script demonstrates the lunar cycle calculator functionality.
"""

from datetime import datetime, timedelta
from trading_strategy import LunarCalculator


def main():
    """Demonstrate lunar calculator features."""

    print("=" * 70)
    print("LUNAR CALCULATOR DEMONSTRATION")
    print("=" * 70)

    # Initialize calculator
    calc = LunarCalculator()

    # Get current date info
    today = datetime.now()

    print("\n--- TODAY'S LUNAR INFORMATION ---")
    lunar_info = calc.get_lunar_info(today)

    print(f"\nDate: {lunar_info['date'].strftime('%Y-%m-%d')}")
    print(f"Lunar Age: {lunar_info['lunar_age_days']} days")
    print(f"Phase: {lunar_info['phase_name'].replace('_', ' ').title()}")
    print(f"Phase %: {lunar_info['phase_percent']*100:.2f}%")
    print(f"Period Type: {lunar_info['period_type'].upper()}")
    print(f"Next Transition: {lunar_info['next_transition_date'].strftime('%Y-%m-%d')} "
          f"(to {lunar_info['next_period_type'].upper()} period)")

    # Show next few transitions
    print("\n--- UPCOMING LUNAR TRANSITIONS ---")
    end_date = today + timedelta(days=180)  # Next 6 months
    transitions = calc.get_period_transitions(today, end_date)

    for i, (date, period_type) in enumerate(transitions[:10], 1):
        phase_info = calc.get_lunar_info(date)
        phase_name = phase_info['phase_name'].replace('_', ' ').title()

        print(f"\n{i}. {date.strftime('%Y-%m-%d')} - Transition to {period_type.upper()} period")
        print(f"   Lunar Phase: {phase_name}")

        if period_type == 'green':
            print("   → BUY SIGNAL (Enter long position)")
        else:
            print("   → SELL SIGNAL (Exit long position)")

    # Historical example - check specific dates
    print("\n--- HISTORICAL LUNAR ANALYSIS ---")

    historical_dates = [
        "2020-01-01",
        "2020-03-15",
        "2020-06-21",
        "2020-09-15",
        "2020-12-31",
    ]

    for date_str in historical_dates:
        date = datetime.strptime(date_str, '%Y-%m-%d')
        info = calc.get_lunar_info(date)

        print(f"\n{date_str}:")
        print(f"  Phase: {info['phase_name'].replace('_', ' ').title()} "
              f"({info['phase_percent']*100:.1f}%)")
        print(f"  Period: {info['period_type'].upper()}")
        print(f"  Trading Action: {'HOLD (in position)' if info['period_type'] == 'green' else 'HOLD (in cash)'}")

    # Demonstrate custom configuration
    print("\n--- CUSTOM LUNAR CONFIGURATION ---")
    print("\nStandard configuration: Green period from New Moon to Full Moon")

    # You can customize the green/red period definitions if needed
    custom_calc = LunarCalculator(
        green_phase_start='first_quarter',
        green_phase_end='last_quarter'
    )

    print("Custom configuration: Green period from First Quarter to Last Quarter")
    print("(This is just an example - you can experiment with different configurations)")

    custom_info = custom_calc.get_lunar_info(today)
    print(f"\nToday's period with custom config: {custom_info['period_type'].upper()}")

    print("\n" + "=" * 70)
    print("LUNAR CALCULATOR DEMONSTRATION COMPLETE")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
