"""
Lunatic Trader Strategy Implementation

Based on lunar cycle trading methodology from blog.lunatictrader.com
- Buy at the end of red (bearish) periods
- Sell at the end of green (bullish) periods
- Green periods: New Moon to Full Moon (waxing moon)
- Red periods: Full Moon to New Moon (waning moon)
"""

import pandas as pd
from typing import Dict, Any
from .strategy_base import StrategyBase
from .lunar_calculator import LunarCalculator


class LunaticStrategy(StrategyBase):
    """
    Lunatic Trader strategy based on lunar cycles.

    Strategy logic:
    1. Calculate lunar phase for each trading day
    2. Identify green (bullish) and red (bearish) periods
    3. Buy at transitions from red to green (new moon)
    4. Sell at transitions from green to red (full moon)
    """

    def __init__(self, config):
        """
        Initialize the Lunatic Trader strategy.

        Args:
            config: StrategyConfig object
        """
        super().__init__(config)

        # Initialize lunar calculator
        self.lunar_calc = LunarCalculator(
            green_phase_start=config.lunar_green_start,
            green_phase_end=config.lunar_green_end
        )

        # Store lunar data for explanations
        self.lunar_data = {}

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Generate trading signals based on lunar cycles.

        Args:
            data: DataFrame with OHLCV price data

        Returns:
            DataFrame with added columns:
                - 'lunar_phase': Phase name
                - 'period_type': 'green' or 'red'
                - 'phase_percent': Lunar phase percentage
                - 'signal': Trading signal (1=buy, -1=sell, 0=hold)
        """
        df = data.copy()

        # Calculate lunar information for each date
        lunar_info_list = []

        for date in df.index:
            lunar_info = self.lunar_calc.get_lunar_info(date)
            lunar_info_list.append(lunar_info)

            # Store for later reference
            self.lunar_data[date] = lunar_info

        # Convert to DataFrame and merge
        lunar_df = pd.DataFrame(lunar_info_list)
        lunar_df.set_index('date', inplace=True)

        df['lunar_phase'] = lunar_df['phase_name']
        df['period_type'] = lunar_df['period_type']
        df['phase_percent'] = lunar_df['phase_percent']

        # Generate signals based on period transitions
        df['signal'] = 0

        # Detect transitions
        df['prev_period'] = df['period_type'].shift(1)

        # Buy signal: Transition from red to green (new moon)
        df.loc[(df['period_type'] == 'green') & (df['prev_period'] == 'red'), 'signal'] = 1

        # Sell signal: Transition from green to red (full moon)
        df.loc[(df['period_type'] == 'red') & (df['prev_period'] == 'green'), 'signal'] = -1

        # Clean up temporary column
        df.drop('prev_period', axis=1, inplace=True)

        self.signals = df

        return df

    def get_signal_explanation(self, date: pd.Timestamp, signal: int) -> str:
        """
        Get explanation for a trading signal.

        Args:
            date: Date of the signal
            signal: Signal value (1, -1, or 0)

        Returns:
            String explanation
        """
        if date not in self.lunar_data:
            return "No lunar data available for this date"

        lunar_info = self.lunar_data[date]

        if signal == 1:
            return (f"BUY Signal: Transition to GREEN period (bullish)\n"
                   f"  Lunar Phase: {lunar_info['phase_name'].replace('_', ' ').title()}\n"
                   f"  Phase: {lunar_info['phase_percent']*100:.1f}% of cycle\n"
                   f"  Period: New Moon → Full Moon (waxing moon)\n"
                   f"  Strategy: Enter long position")

        elif signal == -1:
            return (f"SELL Signal: Transition to RED period (bearish)\n"
                   f"  Lunar Phase: {lunar_info['phase_name'].replace('_', ' ').title()}\n"
                   f"  Phase: {lunar_info['phase_percent']*100:.1f}% of cycle\n"
                   f"  Period: Full Moon → New Moon (waning moon)\n"
                   f"  Strategy: Exit long position")

        else:
            period = lunar_info['period_type'].upper()
            return (f"HOLD: Currently in {period} period\n"
                   f"  Lunar Phase: {lunar_info['phase_name'].replace('_', ' ').title()}\n"
                   f"  Phase: {lunar_info['phase_percent']*100:.1f}% of cycle\n"
                   f"  Next transition: {lunar_info['next_transition_date'].strftime('%Y-%m-%d')}")

    def get_period_stats(self) -> Dict[str, Any]:
        """
        Calculate performance statistics by lunar period.

        Returns:
            Dictionary with green and red period statistics
        """
        if self.signals is None:
            return {}

        df = self.signals.copy()

        # Calculate returns for each period
        df['returns'] = df['Close'].pct_change()

        green_periods = df[df['period_type'] == 'green']
        red_periods = df[df['period_type'] == 'red']

        green_total_return = (green_periods['Close'].iloc[-1] - green_periods['Close'].iloc[0]) if len(green_periods) > 0 else 0
        red_total_return = (red_periods['Close'].iloc[-1] - red_periods['Close'].iloc[0]) if len(red_periods) > 0 else 0

        return {
            'green_period': {
                'days': len(green_periods),
                'total_return': green_total_return,
                'avg_daily_return': green_periods['returns'].mean() if len(green_periods) > 0 else 0,
                'volatility': green_periods['returns'].std() if len(green_periods) > 0 else 0,
            },
            'red_period': {
                'days': len(red_periods),
                'total_return': red_total_return,
                'avg_daily_return': red_periods['returns'].mean() if len(red_periods) > 0 else 0,
                'volatility': red_periods['returns'].std() if len(red_periods) > 0 else 0,
            }
        }

    def print_period_stats(self):
        """Print statistics comparing green and red periods."""
        stats = self.get_period_stats()

        if not stats:
            print("No statistics available. Run generate_signals first.")
            return

        print("\n" + "=" * 60)
        print("LUNAR PERIOD PERFORMANCE COMPARISON")
        print("=" * 60)

        print("\nGREEN PERIOD (New Moon → Full Moon):")
        print(f"  Days:              {stats['green_period']['days']}")
        print(f"  Total Return:      ${stats['green_period']['total_return']:,.2f}")
        print(f"  Avg Daily Return:  {stats['green_period']['avg_daily_return']*100:.4f}%")
        print(f"  Volatility (std):  {stats['green_period']['volatility']*100:.4f}%")

        print("\nRED PERIOD (Full Moon → New Moon):")
        print(f"  Days:              {stats['red_period']['days']}")
        print(f"  Total Return:      ${stats['red_period']['total_return']:,.2f}")
        print(f"  Avg Daily Return:  {stats['red_period']['avg_daily_return']*100:.4f}%")
        print(f"  Volatility (std):  {stats['red_period']['volatility']*100:.4f}%")

        print("\n" + "=" * 60 + "\n")


class LunaticStrategyAlternate(LunaticStrategy):
    """
    Alternate version of Lunatic Strategy - inverted logic.

    This version:
    - Sells during green periods (contrarian approach)
    - Buys during red periods

    Useful for testing the opposite hypothesis or different market conditions.
    """

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """Generate inverted signals compared to standard strategy."""
        # Use parent class to generate standard signals
        df = super().generate_signals(data)

        # Invert the signals
        df['signal'] = -df['signal']

        return df

    def get_signal_explanation(self, date: pd.Timestamp, signal: int) -> str:
        """Get explanation for inverted signals."""
        # Invert signal for parent explanation
        inverted_signal = -signal

        base_explanation = super().get_signal_explanation(date, inverted_signal)

        return f"[ALTERNATE/INVERTED STRATEGY]\n{base_explanation}"


class LunaticStrategyCustomizable(LunaticStrategy):
    """
    Customizable version allowing fine-tuning of entry/exit points.

    Allows specification of:
    - Exact phase percentages for entry/exit
    - Multiple entry/exit windows
    - Custom filters
    """

    def __init__(self, config, entry_phase_range=(0.0, 0.1), exit_phase_range=(0.45, 0.55)):
        """
        Initialize customizable strategy.

        Args:
            config: StrategyConfig object
            entry_phase_range: Tuple of (min, max) phase percentage for entries
            exit_phase_range: Tuple of (min, max) phase percentage for exits
        """
        super().__init__(config)
        self.entry_phase_range = entry_phase_range
        self.exit_phase_range = exit_phase_range

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """Generate signals based on custom phase ranges."""
        df = data.copy()

        # Calculate lunar information
        lunar_info_list = []
        for date in df.index:
            lunar_info = self.lunar_calc.get_lunar_info(date)
            lunar_info_list.append(lunar_info)
            self.lunar_data[date] = lunar_info

        lunar_df = pd.DataFrame(lunar_info_list)
        lunar_df.set_index('date', inplace=True)

        df['lunar_phase'] = lunar_df['phase_name']
        df['period_type'] = lunar_df['period_type']
        df['phase_percent'] = lunar_df['phase_percent']

        # Generate signals based on custom phase ranges
        df['signal'] = 0

        # Entry signal: Phase within entry range
        entry_mask = (df['phase_percent'] >= self.entry_phase_range[0]) & \
                     (df['phase_percent'] <= self.entry_phase_range[1])

        # Exit signal: Phase within exit range
        exit_mask = (df['phase_percent'] >= self.exit_phase_range[0]) & \
                    (df['phase_percent'] <= self.exit_phase_range[1])

        # Only trigger on first day in range
        df.loc[entry_mask & ~entry_mask.shift(1).fillna(False), 'signal'] = 1
        df.loc[exit_mask & ~exit_mask.shift(1).fillna(False), 'signal'] = -1

        self.signals = df

        return df
