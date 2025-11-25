"""
Comprehensive optimization and asset testing script.

Tests the Lunatic Trader strategy across:
- Major indices
- Individual stocks
- Cryptocurrencies
- Different time periods
- Parameter variations
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from trading_strategy.optimizer import (
    StrategyOptimizer,
    MAJOR_INDICES,
    MAJOR_STOCKS,
    CRYPTO_TICKERS,
    COMMODITIES,
    SECTORS
)


def test_all_asset_classes():
    """Test strategy across all major asset classes."""
    print("\n" + "="*70)
    print("COMPREHENSIVE ASSET CLASS TESTING")
    print("="*70)

    optimizer = StrategyOptimizer(data_source='yahoo')

    # Test period (adjust as needed)
    start_date = '2015-01-01'
    end_date = '2024-11-24'

    # Test major indices
    print("\n\n📊 TESTING MAJOR INDICES")
    print("="*70)
    for ticker in MAJOR_INDICES:
        optimizer.test_asset(ticker, start_date, end_date)

    # Test cryptocurrencies
    print("\n\n₿ TESTING CRYPTOCURRENCIES")
    print("="*70)
    for ticker in CRYPTO_TICKERS:
        optimizer.test_asset(ticker, start_date, end_date)

    # Test major tech stocks
    print("\n\n📈 TESTING MAJOR STOCKS")
    print("="*70)
    for ticker in MAJOR_STOCKS:
        optimizer.test_asset(ticker, start_date, end_date)

    # Test commodities
    print("\n\n🏆 TESTING COMMODITIES")
    print("="*70)
    for ticker in COMMODITIES:
        optimizer.test_asset(ticker, start_date, end_date)

    # Print final comparison
    optimizer.print_comparison()
    optimizer.save_results('full_asset_comparison.csv')


def test_crypto_focus():
    """Deep dive into cryptocurrency performance."""
    print("\n" + "="*70)
    print("CRYPTOCURRENCY DEEP DIVE")
    print("="*70)

    optimizer = StrategyOptimizer(data_source='yahoo')

    # Test Bitcoin across different periods
    print("\n\n₿ BITCOIN - MULTIPLE TIME PERIODS")
    print("="*70)

    periods = [
        ('2017-01-01', '2020-12-31', 'Bull Market Era'),
        ('2020-01-01', '2022-12-31', 'Pandemic/Post Era'),
        ('2015-01-01', '2024-11-24', 'Full History'),
    ]

    for start, end, label in periods:
        print(f"\n--- {label}: {start} to {end} ---")
        optimizer.test_asset('BTC-USD', start, end)

    # Test multiple cryptos in recent period
    print("\n\n₿ MULTIPLE CRYPTOCURRENCIES (2020-2024)")
    print("="*70)
    optimizer.test_multiple_assets(CRYPTO_TICKERS, '2020-01-01', '2024-11-24')

    optimizer.print_comparison()
    optimizer.save_results('crypto_analysis.csv')


def optimize_parameters():
    """Find optimal parameters for key assets."""
    print("\n" + "="*70)
    print("PARAMETER OPTIMIZATION")
    print("="*70)

    optimizer = StrategyOptimizer(data_source='yahoo')

    # Parameter grid to test
    param_grid = {
        'position_size_pct': [0.5, 0.75, 1.0],
        'commission': [0.0, 0.001, 0.002],
        'stop_loss_pct': [None, 0.03, 0.05, 0.10],
    }

    # Test on Bitcoin
    print("\n\n₿ OPTIMIZING FOR BITCOIN")
    optimizer.test_parameter_ranges(
        'BTC-USD',
        '2020-01-01',
        '2024-11-24',
        param_grid
    )

    # Test on NASDAQ
    print("\n\n📊 OPTIMIZING FOR NASDAQ")
    optimizer.test_parameter_ranges(
        '^IXIC',
        '2015-01-01',
        '2024-11-24',
        param_grid
    )


def optimize_entry_exit_points():
    """Find optimal entry/exit phase ranges."""
    print("\n" + "="*70)
    print("ENTRY/EXIT POINT OPTIMIZATION")
    print("="*70)

    optimizer = StrategyOptimizer(data_source='yahoo')

    # Test different entry/exit combinations
    entry_ranges = [
        (0.0, 0.05),   # Very early (new moon)
        (0.0, 0.1),    # Early
        (0.0, 0.15),   # Extended early
        (0.45, 0.5),   # Just before full moon
    ]

    exit_ranges = [
        (0.45, 0.55),  # Around full moon
        (0.5, 0.6),    # Just after full moon
        (0.4, 0.5),    # Before full moon
        (0.48, 0.52),  # Tight around full moon
    ]

    # Test on Bitcoin
    print("\n\n₿ BITCOIN ENTRY/EXIT OPTIMIZATION")
    optimizer.test_custom_entry_exit(
        'BTC-USD',
        '2020-01-01',
        '2024-11-24',
        entry_ranges,
        exit_ranges
    )


def quick_test():
    """Quick test on select assets."""
    print("\n" + "="*70)
    print("QUICK ASSET TEST")
    print("="*70)

    optimizer = StrategyOptimizer(data_source='yahoo')

    test_assets = [
        '^IXIC',    # NASDAQ
        'BTC-USD',  # Bitcoin
        'ETH-USD',  # Ethereum
        'TSLA',     # Tesla
        'GC=F',     # Gold
    ]

    optimizer.test_multiple_assets(
        test_assets,
        '2020-01-01',
        '2024-11-24'
    )

    optimizer.print_comparison()
    optimizer.save_results('quick_test_results.csv')


def compare_crypto_vs_stocks():
    """Direct comparison between crypto and traditional assets."""
    print("\n" + "="*70)
    print("CRYPTO vs TRADITIONAL ASSETS")
    print("="*70)

    optimizer = StrategyOptimizer(data_source='yahoo')

    comparison_assets = [
        # Traditional
        '^GSPC',    # S&P 500
        '^IXIC',    # NASDAQ
        'AAPL',     # Apple
        'MSFT',     # Microsoft
        'GC=F',     # Gold
        # Crypto
        'BTC-USD',  # Bitcoin
        'ETH-USD',  # Ethereum
        'SOL-USD',  # Solana
    ]

    optimizer.test_multiple_assets(
        comparison_assets,
        '2020-01-01',
        '2024-11-24',
        config_overrides={'initial_capital': 100000.0}
    )

    print("\n\n" + "="*70)
    print("CRYPTO vs STOCKS ANALYSIS")
    print("="*70)

    results_df = optimizer.get_results_dataframe()

    crypto_results = results_df[results_df['ticker'].str.contains('-USD')]
    stock_results = results_df[~results_df['ticker'].str.contains('-USD')]

    print("\n📊 TRADITIONAL ASSETS AVERAGES:")
    print(f"  Avg Return: {stock_results['total_return_pct'].mean():.2f}%")
    print(f"  Avg Sharpe: {stock_results['sharpe_ratio'].mean():.2f}")
    print(f"  Avg Win Rate: {stock_results['win_rate'].mean():.2f}%")
    print(f"  Avg Max DD: {stock_results['max_drawdown_pct'].mean():.2f}%")

    print("\n₿ CRYPTOCURRENCY AVERAGES:")
    print(f"  Avg Return: {crypto_results['total_return_pct'].mean():.2f}%")
    print(f"  Avg Sharpe: {crypto_results['sharpe_ratio'].mean():.2f}")
    print(f"  Avg Win Rate: {crypto_results['win_rate'].mean():.2f}%")
    print(f"  Avg Max DD: {crypto_results['max_drawdown_pct'].mean():.2f}%")

    optimizer.save_results('crypto_vs_stocks.csv')


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Run strategy optimization')
    parser.add_argument('--mode', type=str, default='quick',
                       choices=['quick', 'full', 'crypto', 'optimize-params',
                               'optimize-entry-exit', 'compare'],
                       help='Test mode to run')

    args = parser.parse_args()

    if args.mode == 'quick':
        quick_test()
    elif args.mode == 'full':
        test_all_asset_classes()
    elif args.mode == 'crypto':
        test_crypto_focus()
    elif args.mode == 'optimize-params':
        optimize_parameters()
    elif args.mode == 'optimize-entry-exit':
        optimize_entry_exit_points()
    elif args.mode == 'compare':
        compare_crypto_vs_stocks()

    print("\n\n✅ Optimization complete!")
