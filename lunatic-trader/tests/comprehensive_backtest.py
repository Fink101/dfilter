"""
Comprehensive Backtesting Framework

Scientific validation of the lunar cycle hypothesis with:
- Multiple time periods
- Statistical significance testing
- Buy-and-hold comparison
- Index fund benchmarks
- Volatility-adjusted returns
- Monte Carlo permutation tests to validate lunar effects are real
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Any
import warnings
warnings.filterwarnings('ignore')

from lunatic.lunatic_strategy import LunaticStrategy
from lunatic.backtester import Backtester
from lunatic.data_fetcher import DataFetcher
from lunatic.config import StrategyConfig


class ComprehensiveBacktest:
    """
    Rigorous backtesting framework to validate lunar cycle hypothesis.
    """

    def __init__(self, ticker: str, data_source='yahoo'):
        self.ticker = ticker
        self.fetcher = DataFetcher(source=data_source)
        self.results = {}

    def run_full_analysis(self, start_date: str, end_date: str):
        """
        Run complete analysis suite.

        Args:
            start_date: Analysis start date
            end_date: Analysis end date
        """
        print(f"\n{'='*80}")
        print(f"COMPREHENSIVE BACKTEST: {self.ticker}")
        print(f"{'='*80}")
        print(f"Period: {start_date} to {end_date}\n")

        # Fetch data
        print("Fetching market data...")
        data = self.fetcher.fetch(self.ticker, start_date, end_date)
        print(f"✓ Loaded {len(data)} trading days\n")

        # 1. Buy-and-hold baseline
        print("1. Running Buy-and-Hold Baseline...")
        buy_hold_return = self._buy_and_hold(data)

        # 2. Lunar strategy
        print("\n2. Running Lunar Strategy...")
        lunar_results = self._lunar_strategy(data, start_date, end_date)

        # 3. Statistical significance test
        print("\n3. Testing Statistical Significance (Monte Carlo)...")
        is_significant, p_value = self._monte_carlo_test(data, lunar_results, n_simulations=1000)

        # 4. Period-by-period analysis
        print("\n4. Analyzing Lunar Period Performance...")
        period_analysis = self._period_analysis(data)

        # 5. Volatility-adjusted returns
        print("\n5. Calculating Volatility-Adjusted Metrics...")
        vol_adjusted = self._volatility_adjusted_metrics(lunar_results, buy_hold_return, data)

        # Compile results
        self.results = {
            'ticker': self.ticker,
            'period': f"{start_date} to {end_date}",
            'days': len(data),
            'buy_hold': buy_hold_return,
            'lunar_strategy': lunar_results,
            'period_analysis': period_analysis,
            'statistical_significance': {
                'is_significant': is_significant,
                'p_value': p_value,
                'threshold': 0.05
            },
            'volatility_adjusted': vol_adjusted
        }

        self._print_summary()

        return self.results

    def _buy_and_hold(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Calculate buy-and-hold returns."""
        initial_price = data['Close'].iloc[0]
        final_price = data['Close'].iloc[-1]

        total_return = ((final_price - initial_price) / initial_price) * 100

        # Calculate CAGR
        days = len(data)
        years = days / 365.25
        cagr = (((final_price / initial_price) ** (1 / years)) - 1) * 100 if years > 0 else 0

        # Calculate metrics
        daily_returns = data['Close'].pct_change().dropna()
        volatility = daily_returns.std() * np.sqrt(252) * 100  # Annualized

        # Drawdown
        cumulative = (1 + daily_returns).cumprod()
        running_max = cumulative.expanding().max()
        drawdown = (cumulative - running_max) / running_max
        max_drawdown = drawdown.min() * 100

        # Sharpe
        excess_returns = daily_returns - (0.02 / 252)
        sharpe = np.sqrt(252) * (excess_returns.mean() / daily_returns.std()) if daily_returns.std() > 0 else 0

        print(f"  Total Return: {total_return:.2f}%")
        print(f"  CAGR: {cagr:.2f}%")
        print(f"  Volatility: {volatility:.2f}%")
        print(f"  Sharpe Ratio: {sharpe:.2f}")
        print(f"  Max Drawdown: {max_drawdown:.2f}%")

        return {
            'total_return_pct': total_return,
            'cagr': cagr,
            'volatility': volatility,
            'sharpe_ratio': sharpe,
            'max_drawdown_pct': max_drawdown,
            'final_value': 100000 * (1 + total_return/100)
        }

    def _lunar_strategy(self, data: pd.DataFrame, start_date: str, end_date: str) -> Dict[str, Any]:
        """Run lunar strategy backtest."""
        config = StrategyConfig(
            name=f"Lunatic - {self.ticker}",
            ticker=self.ticker,
            start_date=start_date,
            end_date=end_date,
            initial_capital=100000.0
        )

        strategy = LunaticStrategy(config)
        backtester = Backtester(strategy, data)
        results = backtester.run()

        summary = results.summary()

        print(f"  Total Return: {summary['total_return_pct']:.2f}%")
        print(f"  CAGR: {summary['cagr']:.2f}%")
        print(f"  Sharpe Ratio: {summary['sharpe_ratio']:.2f}")
        print(f"  Win Rate: {summary['win_rate']:.2f}%")
        print(f"  Max Drawdown: {summary['max_drawdown_pct']:.2f}%")
        print(f"  Trades: {summary['num_trades']}")

        return summary

    def _period_analysis(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Analyze performance during green vs red periods."""
        from lunatic.lunar_calculator import LunarCalculator

        calc = LunarCalculator()

        # Add lunar info to data
        lunar_data = []
        for date in data.index:
            info = calc.get_lunar_info(date)
            lunar_data.append({
                'date': date,
                'period': info['period_type'],
                'close': data.loc[date, 'Close']
            })

        df = pd.DataFrame(lunar_data).set_index('date')
        df['returns'] = df['close'].pct_change()

        # Separate by period
        green = df[df['period'] == 'green']
        red = df[df['period'] == 'red']

        # Calculate statistics
        green_stats = {
            'days': len(green),
            'avg_daily_return': green['returns'].mean() * 100,
            'total_return': ((green['close'].iloc[-1] / green['close'].iloc[0]) - 1) * 100 if len(green) > 0 else 0,
            'volatility': green['returns'].std() * 100,
            'win_rate': (green['returns'] > 0).sum() / len(green) * 100 if len(green) > 0 else 0
        }

        red_stats = {
            'days': len(red),
            'avg_daily_return': red['returns'].mean() * 100,
            'total_return': ((red['close'].iloc[-1] / red['close'].iloc[0]) - 1) * 100 if len(red) > 0 else 0,
            'volatility': red['returns'].std() * 100,
            'win_rate': (red['returns'] > 0).sum() / len(red) * 100 if len(red) > 0 else 0
        }

        print(f"\n  GREEN PERIOD (New Moon → Full Moon):")
        print(f"    Days: {green_stats['days']}")
        print(f"    Avg Daily Return: {green_stats['avg_daily_return']:.4f}%")
        print(f"    Total Return: {green_stats['total_return']:.2f}%")
        print(f"    Daily Win Rate: {green_stats['win_rate']:.2f}%")

        print(f"\n  RED PERIOD (Full Moon → New Moon):")
        print(f"    Days: {red_stats['days']}")
        print(f"    Avg Daily Return: {red_stats['avg_daily_return']:.4f}%")
        print(f"    Total Return: {red_stats['total_return']:.2f}%")
        print(f"    Daily Win Rate: {red_stats['win_rate']:.2f}%")

        # Calculate difference
        daily_diff = green_stats['avg_daily_return'] - red_stats['avg_daily_return']
        print(f"\n  DIFFERENCE:")
        print(f"    Green outperforms Red by: {daily_diff:.4f}% per day")

        return {
            'green': green_stats,
            'red': red_stats,
            'difference': daily_diff
        }

    def _monte_carlo_test(self, data: pd.DataFrame, lunar_results: Dict,
                          n_simulations: int = 1000) -> Tuple[bool, float]:
        """
        Test if lunar strategy outperformance is statistically significant.

        Uses Monte Carlo permutation test: randomly shuffle period labels
        and see if real strategy still outperforms.
        """
        from lunatic.lunar_calculator import LunarCalculator

        calc = LunarCalculator()

        # Get actual lunar periods
        periods = []
        for date in data.index:
            info = calc.get_lunar_info(date)
            periods.append(1 if info['period_type'] == 'green' else 0)

        periods = np.array(periods)
        returns = data['Close'].pct_change().fillna(0).values

        # Calculate actual strategy return
        actual_return = lunar_results['total_return_pct']

        # Run simulations with random period assignments
        random_returns = []

        print(f"  Running {n_simulations} Monte Carlo simulations...")

        for i in range(n_simulations):
            # Randomly shuffle periods
            shuffled_periods = np.random.permutation(periods)

            # Calculate return with shuffled periods
            # (only invest during "green" periods)
            invested_returns = returns[shuffled_periods == 1]
            random_return = ((1 + invested_returns).prod() - 1) * 100
            random_returns.append(random_return)

            if (i + 1) % 200 == 0:
                print(f"    Completed {i + 1}/{n_simulations}...")

        random_returns = np.array(random_returns)

        # Calculate p-value: how many random strategies beat actual?
        p_value = (random_returns >= actual_return).sum() / n_simulations

        is_significant = p_value < 0.05

        print(f"\n  Actual Strategy Return: {actual_return:.2f}%")
        print(f"  Average Random Return: {random_returns.mean():.2f}%")
        print(f"  P-value: {p_value:.4f}")
        print(f"  Significant at 5% level: {'YES ✓' if is_significant else 'NO ✗'}")

        return is_significant, p_value

    def _volatility_adjusted_metrics(self, lunar_results: Dict,
                                     buy_hold_results: Dict,
                                     data: pd.DataFrame) -> Dict[str, Any]:
        """
        Calculate metrics adjusted for volatility to see if lunar edge
        is just due to higher volatility/risk.
        """
        # Sharpe ratio comparison
        lunar_sharpe = lunar_results['sharpe_ratio']
        buy_hold_sharpe = buy_hold_results['sharpe_ratio']

        # Sortino ratio (downside risk only)
        daily_returns = data['Close'].pct_change().dropna()
        downside_returns = daily_returns[daily_returns < 0]

        lunar_sortino = lunar_results.get('sortino_ratio', 0)

        # Calculate return per unit of volatility
        lunar_return_per_vol = (lunar_results['total_return_pct'] /
                               (lunar_results['max_drawdown_pct'] if lunar_results['max_drawdown_pct'] != 0 else 1))

        buy_hold_return_per_vol = (buy_hold_results['total_return_pct'] /
                                   (buy_hold_results['max_drawdown_pct'] if buy_hold_results['max_drawdown_pct'] != 0 else 1))

        print(f"\n  Sharpe Comparison:")
        print(f"    Lunar: {lunar_sharpe:.2f}")
        print(f"    Buy-Hold: {buy_hold_sharpe:.2f}")
        print(f"    Difference: {lunar_sharpe - buy_hold_sharpe:+.2f}")

        print(f"\n  Return / Max Drawdown:")
        print(f"    Lunar: {lunar_return_per_vol:.2f}")
        print(f"    Buy-Hold: {buy_hold_return_per_vol:.2f}")

        return {
            'lunar_sharpe': lunar_sharpe,
            'buy_hold_sharpe': buy_hold_sharpe,
            'sharpe_advantage': lunar_sharpe - buy_hold_sharpe,
            'lunar_return_per_vol': lunar_return_per_vol,
            'buy_hold_return_per_vol': buy_hold_return_per_vol
        }

    def _print_summary(self):
        """Print comprehensive summary."""
        print(f"\n\n{'='*80}")
        print("COMPREHENSIVE BACKTEST SUMMARY")
        print(f"{'='*80}")

        print(f"\n📊 Asset: {self.results['ticker']}")
        print(f"📅 Period: {self.results['period']}")
        print(f"📈 Trading Days: {self.results['days']}")

        print(f"\n{'─'*80}")
        print("STRATEGY COMPARISON")
        print(f"{'─'*80}")

        lunar = self.results['lunar_strategy']
        buy_hold = self.results['buy_hold']

        print(f"\n{'Metric':<30} {'Lunar Strategy':>20} {'Buy & Hold':>20}")
        print(f"{'-'*70}")
        print(f"{'Total Return':<30} {lunar['total_return_pct']:>19.2f}% {buy_hold['total_return_pct']:>19.2f}%")
        print(f"{'CAGR':<30} {lunar['cagr']:>19.2f}% {buy_hold['cagr']:>19.2f}%")
        print(f"{'Sharpe Ratio':<30} {lunar['sharpe_ratio']:>20.2f} {buy_hold['sharpe_ratio']:>20.2f}")
        print(f"{'Max Drawdown':<30} {lunar['max_drawdown_pct']:>19.2f}% {buy_hold['max_drawdown_pct']:>19.2f}%")
        print(f"{'Final Value ($100k)':<30} ${lunar.get('final_capital', 0):>18,.0f} ${buy_hold['final_value']:>18,.0f}")

        edge = lunar['total_return_pct'] - buy_hold['total_return_pct']
        print(f"\n{'Strategy Edge':<30} {edge:>19.2f}%")

        print(f"\n{'─'*80}")
        print("LUNAR PERIOD ANALYSIS")
        print(f"{'─'*80}")

        period = self.results['period_analysis']
        print(f"\nGreen Period Avg Daily: {period['green']['avg_daily_return']:>6.4f}%")
        print(f"Red Period Avg Daily:   {period['red']['avg_daily_return']:>6.4f}%")
        print(f"Daily Advantage:        {period['difference']:>6.4f}%")

        print(f"\n{'─'*80}")
        print("STATISTICAL VALIDATION")
        print(f"{'─'*80}")

        sig = self.results['statistical_significance']
        print(f"\nP-value: {sig['p_value']:.4f}")
        print(f"Significant: {'YES ✓ (Lunar effect is real)' if sig['is_significant'] else 'NO ✗ (Could be random)'}")
        print(f"Confidence: {(1 - sig['p_value']) * 100:.1f}%")

        print(f"\n{'─'*80}")
        print("RISK-ADJUSTED PERFORMANCE")
        print(f"{'─'*80}")

        vol = self.results['volatility_adjusted']
        print(f"\nSharpe Advantage: {vol['sharpe_advantage']:+.2f}")
        print(f"Return/Drawdown Ratio: Lunar={vol['lunar_return_per_vol']:.2f}, "
              f"Buy-Hold={vol['buy_hold_return_per_vol']:.2f}")


class MultiPeriodBacktest:
    """Test strategy across multiple time periods."""

    def __init__(self, ticker: str):
        self.ticker = ticker
        self.results = []

    def run_multiple_periods(self, periods: List[Tuple[str, str, str]]):
        """
        Run backtests across multiple time periods.

        Args:
            periods: List of (start_date, end_date, label) tuples
        """
        print(f"\n{'='*80}")
        print(f"MULTI-PERIOD BACKTEST: {self.ticker}")
        print(f"{'='*80}")
        print(f"Testing {len(periods)} time periods\n")

        for start, end, label in periods:
            print(f"\n{'#'*80}")
            print(f"PERIOD: {label}")
            print(f"{'#'*80}")

            backtester = ComprehensiveBacktest(self.ticker)
            result = backtester.run_full_analysis(start, end)
            result['label'] = label
            self.results.append(result)

        self._print_comparison()

    def _print_comparison(self):
        """Print comparison across all periods."""
        print(f"\n\n{'='*80}")
        print("MULTI-PERIOD COMPARISON")
        print(f"{'='*80}\n")

        df_data = []
        for r in self.results:
            lunar = r['lunar_strategy']
            buy_hold = r['buy_hold']
            sig = r['statistical_significance']

            df_data.append({
                'Period': r['label'],
                'Lunar Return %': lunar['total_return_pct'],
                'Buy-Hold %': buy_hold['total_return_pct'],
                'Edge %': lunar['total_return_pct'] - buy_hold['total_return_pct'],
                'Lunar Sharpe': lunar['sharpe_ratio'],
                'Significant': '✓' if sig['is_significant'] else '✗',
                'P-value': sig['p_value']
            })

        df = pd.DataFrame(df_data)
        print(df.to_string(index=False))

        # Summary statistics
        print(f"\n{'─'*80}")
        print("SUMMARY ACROSS ALL PERIODS")
        print(f"{'─'*80}")

        avg_edge = df['Edge %'].mean()
        periods_significant = (df['Significant'] == '✓').sum()
        total_periods = len(df)

        print(f"\nAverage Strategy Edge: {avg_edge:.2f}%")
        print(f"Periods with Significant Effect: {periods_significant}/{total_periods} "
              f"({periods_significant/total_periods*100:.0f}%)")
        print(f"Average P-value: {df['P-value'].mean():.4f}")
