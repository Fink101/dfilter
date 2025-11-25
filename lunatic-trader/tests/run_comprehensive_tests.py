"""
Run comprehensive backtests across multiple assets and time periods.

This script scientifically validates the lunar hypothesis by:
1. Testing across different time spans
2. Comparing with buy-and-hold
3. Testing statistical significance
4. Validating if crypto effects are real vs just volatility
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tests.comprehensive_backtest import ComprehensiveBacktest, MultiPeriodBacktest


def test_bitcoin_comprehensive():
    """Comprehensive Bitcoin testing across multiple periods."""
    print("\n" + "="*80)
    print("BITCOIN COMPREHENSIVE ANALYSIS")
    print("="*80)

    periods = [
        ('2015-01-01', '2017-12-31', '2015-2017: Early Bull Run'),
        ('2018-01-01', '2019-12-31', '2018-2019: Bear/Recovery'),
        ('2020-01-01', '2021-12-31', '2020-2021: Pandemic Bull'),
        ('2022-01-01', '2023-12-31', '2022-2023: Bear Market'),
        ('2015-01-01', '2024-11-24', '2015-2024: Full History'),
    ]

    tester = MultiPeriodBacktest('BTC-USD')
    tester.run_multiple_periods(periods)

    # Save results
    import pandas as pd
    results_data = []
    for r in tester.results:
        results_data.append({
            'period': r['label'],
            'lunar_return': r['lunar_strategy']['total_return_pct'],
            'buy_hold_return': r['buy_hold']['total_return_pct'],
            'edge': r['lunar_strategy']['total_return_pct'] - r['buy_hold']['total_return_pct'],
            'p_value': r['statistical_significance']['p_value'],
            'significant': r['statistical_significance']['is_significant'],
            'lunar_sharpe': r['lunar_strategy']['sharpe_ratio'],
            'buy_hold_sharpe': r['buy_hold']['sharpe_ratio']
        })

    df = pd.DataFrame(results_data)
    df.to_csv('../results/bitcoin_comprehensive_results.csv', index=False)
    print("\n✓ Results saved to results/bitcoin_comprehensive_results.csv")


def test_ethereum_comprehensive():
    """Comprehensive Ethereum testing."""
    print("\n" + "="*80)
    print("ETHEREUM COMPREHENSIVE ANALYSIS")
    print("="*80)

    periods = [
        ('2017-01-01', '2018-12-31', '2017-2018: ICO Boom/Bust'),
        ('2019-01-01', '2020-12-31', '2019-2020: Pre-DeFi'),
        ('2021-01-01', '2022-12-31', '2021-2022: DeFi/NFT Era'),
        ('2017-01-01', '2024-11-24', '2017-2024: Full History'),
    ]

    tester = MultiPeriodBacktest('ETH-USD')
    tester.run_multiple_periods(periods)


def test_nasdaq_comprehensive():
    """Comprehensive NASDAQ testing."""
    print("\n" + "="*80)
    print("NASDAQ COMPREHENSIVE ANALYSIS")
    print("="*80)

    periods = [
        ('2010-01-01', '2014-12-31', '2010-2014: Post-Crisis Recovery'),
        ('2015-01-01', '2019-12-31', '2015-2019: Bull Market'),
        ('2020-01-01', '2022-12-31', '2020-2022: Pandemic Era'),
        ('2010-01-01', '2024-11-24', '2010-2024: Full History'),
    ]

    tester = MultiPeriodBacktest('^IXIC')
    tester.run_multiple_periods(periods)


def test_sp500_comprehensive():
    """Comprehensive S&P 500 testing."""
    print("\n" + "="*80)
    print("S&P 500 COMPREHENSIVE ANALYSIS")
    print("="*80)

    periods = [
        ('2010-01-01', '2014-12-31', '2010-2014: Post-Crisis'),
        ('2015-01-01', '2019-12-31', '2015-2019: Steady Bull'),
        ('2020-01-01', '2024-11-24', '2020-2024: Recent'),
        ('2010-01-01', '2024-11-24', '2010-2024: Full History'),
    ]

    tester = MultiPeriodBacktest('^GSPC')
    tester.run_multiple_periods(periods)


def compare_asset_classes():
    """
    Direct comparison: Are crypto lunar effects just due to higher volatility?

    Tests the same time period for crypto vs traditional assets.
    """
    print("\n" + "="*80)
    print("ASSET CLASS COMPARISON (2020-2024)")
    print("Testing if crypto lunar effects are real or just volatility")
    print("="*80)

    assets = [
        ('BTC-USD', 'Bitcoin'),
        ('ETH-USD', 'Ethereum'),
        ('^IXIC', 'NASDAQ'),
        ('^GSPC', 'S&P 500'),
    ]

    results = []

    for ticker, name in assets:
        print(f"\n{'='*80}")
        print(f"Testing: {name} ({ticker})")
        print(f"{'='*80}")

        backtester = ComprehensiveBacktest(ticker)
        result = backtester.run_full_analysis('2020-01-01', '2024-11-24')
        result['name'] = name
        results.append(result)

    # Comparison analysis
    print(f"\n\n{'='*80}")
    print("CROSS-ASSET COMPARISON")
    print(f"{'='*80}\n")

    comparison_data = []
    for r in results:
        lunar = r['lunar_strategy']
        buy_hold = r['buy_hold']
        sig = r['statistical_significance']
        period = r['period_analysis']

        comparison_data.append({
            'Asset': r['name'],
            'Volatility (Buy-Hold)': buy_hold['volatility'],
            'Lunar Return': lunar['total_return_pct'],
            'Buy-Hold Return': buy_hold['total_return_pct'],
            'Edge': lunar['total_return_pct'] - buy_hold['total_return_pct'],
            'Lunar Sharpe': lunar['sharpe_ratio'],
            'Buy-Hold Sharpe': buy_hold['sharpe_ratio'],
            'Sharpe Advantage': lunar['sharpe_ratio'] - buy_hold['sharpe_ratio'],
            'Green vs Red Diff (daily)': period['difference'],
            'P-value': sig['p_value'],
            'Significant': '✓' if sig['is_significant'] else '✗'
        })

    import pandas as pd
    df = pd.DataFrame(comparison_data)
    print(df.to_string(index=False))

    # Analysis
    print(f"\n{'='*80}")
    print("KEY FINDINGS")
    print(f"{'='*80}\n")

    crypto = df[df['Asset'].isin(['Bitcoin', 'Ethereum'])]
    traditional = df[~df['Asset'].isin(['Bitcoin', 'Ethereum'])]

    print("CRYPTOCURRENCY AVERAGES:")
    print(f"  Volatility: {crypto['Volatility (Buy-Hold)'].mean():.2f}%")
    print(f"  Strategy Edge: {crypto['Edge'].mean():.2f}%")
    print(f"  Sharpe Advantage: {crypto['Sharpe Advantage'].mean():.2f}")
    print(f"  Green vs Red Daily: {crypto['Green vs Red Diff (daily)'].mean():.4f}%")
    print(f"  Significant: {(crypto['Significant'] == '✓').sum()}/{len(crypto)}")

    print("\nTRADITIONAL ASSET AVERAGES:")
    print(f"  Volatility: {traditional['Volatility (Buy-Hold)'].mean():.2f}%")
    print(f"  Strategy Edge: {traditional['Edge'].mean():.2f}%")
    print(f"  Sharpe Advantage: {traditional['Sharpe Advantage'].mean():.2f}")
    print(f"  Green vs Red Daily: {traditional['Green vs Red Diff (daily)'].mean():.4f}%")
    print(f"  Significant: {(traditional['Significant'] == '✓').sum()}/{len(traditional)}")

    # Statistical comparison
    print(f"\n{'='*80}")
    print("CONCLUSION")
    print(f"{'='*80}\n")

    # Normalize by volatility to see if effect persists
    crypto_norm = (crypto['Edge'] / crypto['Volatility (Buy-Hold)']).mean()
    trad_norm = (traditional['Edge'] / traditional['Volatility (Buy-Hold)']).mean()

    print("After normalizing for volatility:")
    print(f"  Crypto Edge / Volatility: {crypto_norm:.4f}")
    print(f"  Traditional Edge / Volatility: {trad_norm:.4f}")

    if crypto_norm > trad_norm * 1.5:
        print("\n✓ CRYPTO LUNAR EFFECTS APPEAR REAL")
        print("  Crypto shows stronger lunar effects even after volatility adjustment")
    elif crypto_norm > trad_norm:
        print("\n⚠️  CRYPTO SHOWS MODEST LUNAR ADVANTAGE")
        print("  Effects present but may be partly due to volatility")
    else:
        print("\n✗ LUNAR EFFECTS MAY BE VOLATILITY-DRIVEN")
        print("  Similar effects across asset classes when volatility-adjusted")

    # Save results
    df.to_csv('../results/asset_class_comparison.csv', index=False)
    print("\n✓ Results saved to results/asset_class_comparison.csv")


def quick_test():
    """Quick test on recent Bitcoin data."""
    print("\n" + "="*80)
    print("QUICK TEST: Bitcoin (2020-2024)")
    print("="*80)

    backtester = ComprehensiveBacktest('BTC-USD')
    backtester.run_full_analysis('2020-01-01', '2024-11-24')


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Run comprehensive backtests')
    parser.add_argument('--test', type=str, default='quick',
                       choices=['quick', 'bitcoin', 'ethereum', 'nasdaq', 'sp500',
                               'compare', 'all'],
                       help='Test to run')

    args = parser.parse_args()

    # Create results directory
    os.makedirs('../results', exist_ok=True)

    if args.test == 'quick':
        quick_test()
    elif args.test == 'bitcoin':
        test_bitcoin_comprehensive()
    elif args.test == 'ethereum':
        test_ethereum_comprehensive()
    elif args.test == 'nasdaq':
        test_nasdaq_comprehensive()
    elif args.test == 'sp500':
        test_sp500_comprehensive()
    elif args.test == 'compare':
        compare_asset_classes()
    elif args.test == 'all':
        print("Running all comprehensive tests...")
        test_bitcoin_comprehensive()
        test_ethereum_comprehensive()
        test_nasdaq_comprehensive()
        test_sp500_comprehensive()
        compare_asset_classes()

    print("\n\n" + "="*80)
    print("TESTING COMPLETE")
    print("="*80)
    print("\nAll results saved to results/ directory")
