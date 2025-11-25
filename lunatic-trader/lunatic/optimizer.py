"""
Strategy Optimization Framework

Tests the Lunatic Trader strategy across multiple:
- Assets (stocks, indices, crypto)
- Time periods
- Parameters (position sizing, stop loss, etc.)
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Any, Tuple
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

from .lunatic_strategy import LunaticStrategy, LunaticStrategyCustomizable
from .backtester import Backtester
from .data_fetcher import DataFetcher
from .config import StrategyConfig


class StrategyOptimizer:
    """
    Optimizer for testing strategy across multiple assets and parameters.
    """

    def __init__(self, data_source='yahoo'):
        """
        Initialize optimizer.

        Args:
            data_source: Data source to use ('yahoo', 'crypto', 'csv')
        """
        self.data_source = data_source
        self.fetcher = DataFetcher(source=data_source)
        self.results = []

    def test_asset(self, ticker: str, start_date: str, end_date: str,
                   config_overrides: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Test strategy on a single asset.

        Args:
            ticker: Ticker symbol
            start_date: Start date
            end_date: End date
            config_overrides: Custom config parameters

        Returns:
            Dictionary with results
        """
        print(f"\n{'='*70}")
        print(f"Testing {ticker}")
        print(f"{'='*70}")

        try:
            # Fetch data
            data = self.fetcher.fetch(ticker, start_date, end_date)

            if len(data) < 100:
                print(f"⚠ Insufficient data for {ticker} ({len(data)} days)")
                return None

            # Create config
            config = StrategyConfig(
                name=f"Lunatic Trader - {ticker}",
                ticker=ticker,
                start_date=start_date,
                end_date=end_date
            )

            # Apply overrides
            if config_overrides:
                for key, value in config_overrides.items():
                    setattr(config, key, value)

            # Run backtest
            strategy = LunaticStrategy(config)
            backtester = Backtester(strategy, data)
            results = backtester.run()

            # Get summary
            summary = results.summary()
            summary['ticker'] = ticker
            summary['data_points'] = len(data)

            # Add period stats
            period_stats = strategy.get_period_stats()
            summary['green_period_return'] = period_stats['green_period']['total_return']
            summary['red_period_return'] = period_stats['red_period']['total_return']
            summary['green_avg_daily_return'] = period_stats['green_period']['avg_daily_return']
            summary['red_avg_daily_return'] = period_stats['red_period']['avg_daily_return']

            # Calculate buy-and-hold comparison
            buy_hold_return = ((data['Close'].iloc[-1] - data['Close'].iloc[0]) /
                              data['Close'].iloc[0]) * 100
            summary['buy_hold_return_pct'] = buy_hold_return
            summary['strategy_vs_buy_hold'] = summary['total_return_pct'] - buy_hold_return

            self.results.append(summary)

            # Print quick summary
            print(f"\n📊 {ticker} Results:")
            print(f"  Total Return: {summary['total_return_pct']:.2f}%")
            print(f"  Buy & Hold: {buy_hold_return:.2f}%")
            print(f"  Strategy Edge: {summary['strategy_vs_buy_hold']:.2f}%")
            print(f"  Win Rate: {summary['win_rate']:.2f}%")
            print(f"  Sharpe Ratio: {summary['sharpe_ratio']:.2f}")
            print(f"  Max Drawdown: {summary['max_drawdown_pct']:.2f}%")

            return summary

        except Exception as e:
            print(f"❌ Error testing {ticker}: {str(e)}")
            return None

    def test_multiple_assets(self, tickers: List[str], start_date: str,
                           end_date: str, config_overrides: Dict[str, Any] = None):
        """
        Test strategy on multiple assets.

        Args:
            tickers: List of ticker symbols
            start_date: Start date
            end_date: End date
            config_overrides: Custom config parameters
        """
        print(f"\n{'='*70}")
        print(f"MULTI-ASSET BACKTEST")
        print(f"{'='*70}")
        print(f"Period: {start_date} to {end_date}")
        print(f"Testing {len(tickers)} assets")

        for ticker in tickers:
            self.test_asset(ticker, start_date, end_date, config_overrides)

        self.print_comparison()

    def test_parameter_ranges(self, ticker: str, start_date: str, end_date: str,
                             param_grid: Dict[str, List[Any]]):
        """
        Test different parameter combinations.

        Args:
            ticker: Ticker symbol
            start_date: Start date
            end_date: End date
            param_grid: Dictionary of parameter names to lists of values
        """
        print(f"\n{'='*70}")
        print(f"PARAMETER OPTIMIZATION: {ticker}")
        print(f"{'='*70}")

        # Generate all parameter combinations
        from itertools import product

        param_names = list(param_grid.keys())
        param_values = list(param_grid.values())

        print(f"Testing {np.prod([len(v) for v in param_values])} combinations...")

        best_sharpe = -np.inf
        best_return = -np.inf
        best_params_sharpe = None
        best_params_return = None

        for values in product(*param_values):
            config_overrides = dict(zip(param_names, values))

            # Run test
            result = self.test_asset(ticker, start_date, end_date, config_overrides)

            if result:
                if result['sharpe_ratio'] > best_sharpe:
                    best_sharpe = result['sharpe_ratio']
                    best_params_sharpe = config_overrides.copy()

                if result['total_return_pct'] > best_return:
                    best_return = result['total_return_pct']
                    best_params_return = config_overrides.copy()

        print(f"\n{'='*70}")
        print("OPTIMIZATION RESULTS")
        print(f"{'='*70}")

        print("\n🏆 Best Parameters (by Sharpe Ratio):")
        print(f"  Sharpe: {best_sharpe:.2f}")
        for key, value in best_params_sharpe.items():
            print(f"  {key}: {value}")

        print("\n💰 Best Parameters (by Total Return):")
        print(f"  Return: {best_return:.2f}%")
        for key, value in best_params_return.items():
            print(f"  {key}: {value}")

    def test_custom_entry_exit(self, ticker: str, start_date: str, end_date: str,
                               entry_ranges: List[Tuple[float, float]],
                               exit_ranges: List[Tuple[float, float]]):
        """
        Test different entry/exit phase ranges.

        Args:
            ticker: Ticker symbol
            start_date: Start date
            end_date: End date
            entry_ranges: List of (start, end) phase percentages for entry
            exit_ranges: List of (start, end) phase percentages for exit
        """
        print(f"\n{'='*70}")
        print(f"ENTRY/EXIT OPTIMIZATION: {ticker}")
        print(f"{'='*70}")

        # Fetch data once
        data = self.fetcher.fetch(ticker, start_date, end_date)

        best_sharpe = -np.inf
        best_config = None

        for entry_range in entry_ranges:
            for exit_range in exit_ranges:
                config = StrategyConfig(
                    name=f"Custom {ticker}",
                    ticker=ticker,
                    start_date=start_date,
                    end_date=end_date
                )

                strategy = LunaticStrategyCustomizable(
                    config,
                    entry_phase_range=entry_range,
                    exit_phase_range=exit_range
                )

                backtester = Backtester(strategy, data)
                results = backtester.run()

                summary = results.summary()

                if summary['sharpe_ratio'] > best_sharpe:
                    best_sharpe = summary['sharpe_ratio']
                    best_config = {
                        'entry_range': entry_range,
                        'exit_range': exit_range,
                        'sharpe': summary['sharpe_ratio'],
                        'return': summary['total_return_pct'],
                        'max_dd': summary['max_drawdown_pct']
                    }

                print(f"Entry: {entry_range}, Exit: {exit_range} → "
                      f"Sharpe: {summary['sharpe_ratio']:.2f}, "
                      f"Return: {summary['total_return_pct']:.2f}%")

        print(f"\n{'='*70}")
        print("BEST CONFIGURATION")
        print(f"{'='*70}")
        print(f"Entry Range: {best_config['entry_range']}")
        print(f"Exit Range: {best_config['exit_range']}")
        print(f"Sharpe Ratio: {best_config['sharpe']:.2f}")
        print(f"Total Return: {best_config['return']:.2f}%")
        print(f"Max Drawdown: {best_config['max_dd']:.2f}%")

    def print_comparison(self):
        """Print comparison table of all tested assets."""
        if not self.results:
            print("No results to compare")
            return

        print(f"\n{'='*70}")
        print("ASSET COMPARISON")
        print(f"{'='*70}\n")

        # Create DataFrame
        df = pd.DataFrame(self.results)

        # Sort by Sharpe ratio
        df = df.sort_values('sharpe_ratio', ascending=False)

        # Display key metrics
        columns = ['ticker', 'total_return_pct', 'buy_hold_return_pct',
                  'strategy_vs_buy_hold', 'sharpe_ratio', 'win_rate',
                  'max_drawdown_pct', 'num_trades']

        print(df[columns].to_string(index=False))

        # Show best performers
        print(f"\n{'='*70}")
        print("TOP PERFORMERS")
        print(f"{'='*70}")

        print("\n🏆 Best Sharpe Ratio:")
        best_sharpe = df.iloc[0]
        print(f"  {best_sharpe['ticker']}: {best_sharpe['sharpe_ratio']:.2f}")

        print("\n💰 Best Total Return:")
        best_return = df.loc[df['total_return_pct'].idxmax()]
        print(f"  {best_return['ticker']}: {best_return['total_return_pct']:.2f}%")

        print("\n📈 Best vs Buy & Hold:")
        best_edge = df.loc[df['strategy_vs_buy_hold'].idxmax()]
        print(f"  {best_edge['ticker']}: +{best_edge['strategy_vs_buy_hold']:.2f}%")

        print("\n✅ Best Win Rate:")
        best_win = df.loc[df['win_rate'].idxmax()]
        print(f"  {best_win['ticker']}: {best_win['win_rate']:.2f}%")

    def get_results_dataframe(self) -> pd.DataFrame:
        """Get results as DataFrame."""
        return pd.DataFrame(self.results)

    def save_results(self, filename: str = 'optimization_results.csv'):
        """Save results to CSV."""
        if not self.results:
            print("No results to save")
            return

        df = pd.DataFrame(self.results)
        df.to_csv(filename, index=False)
        print(f"\n✓ Results saved to {filename}")


# Preset asset lists for testing
MAJOR_INDICES = [
    '^GSPC',   # S&P 500
    '^IXIC',   # NASDAQ
    '^DJI',    # Dow Jones
    '^RUT',    # Russell 2000
    '^FTSE',   # FTSE 100
    '^GDAXI',  # DAX
    '^N225',   # Nikkei 225
]

MAJOR_STOCKS = [
    'AAPL',    # Apple
    'MSFT',    # Microsoft
    'GOOGL',   # Google
    'AMZN',    # Amazon
    'TSLA',    # Tesla
    'NVDA',    # NVIDIA
    'META',    # Meta
]

CRYPTO_TICKERS = [
    'BTC-USD',  # Bitcoin
    'ETH-USD',  # Ethereum
    'BNB-USD',  # Binance Coin
    'SOL-USD',  # Solana
    'ADA-USD',  # Cardano
    'DOGE-USD', # Dogecoin
]

COMMODITIES = [
    'GC=F',    # Gold
    'SI=F',    # Silver
    'CL=F',    # Crude Oil
]

SECTORS = [
    'XLF',     # Financials
    'XLK',     # Technology
    'XLE',     # Energy
    'XLV',     # Healthcare
    'XLI',     # Industrials
]
