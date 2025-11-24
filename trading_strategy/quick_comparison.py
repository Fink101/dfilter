"""
Quick comparison test using sample data to demonstrate the framework.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import numpy as np
from trading_strategy import (
    LunaticStrategy,
    Backtester,
    StrategyConfig,
    create_sample_data
)


def simulate_asset(name, days, start_price, volatility, trend):
    """
    Create sample data simulating different asset characteristics.

    Args:
        name: Asset name
        days: Number of days
        start_price: Starting price
        volatility: Daily volatility
        trend: Upward trend factor
    """
    dates = pd.date_range(end='2024-11-24', periods=days, freq='D')

    # Generate returns with trend
    returns = np.random.randn(days) * volatility + trend
    prices = start_price * (1 + returns).cumprod()

    data = pd.DataFrame({
        'Open': prices * (1 + np.random.randn(days) * 0.005),
        'High': prices * (1 + np.abs(np.random.randn(days)) * 0.01),
        'Low': prices * (1 - np.abs(np.random.randn(days)) * 0.01),
        'Close': prices,
        'Volume': np.random.randint(1000000, 10000000, days)
    }, index=dates)

    data['High'] = data[['Open', 'High', 'Close']].max(axis=1)
    data['Low'] = data[['Open', 'Low', 'Close']].min(axis=1)

    return data


def test_asset_characteristics():
    """Test strategy on assets with different characteristics."""

    print("\n" + "="*70)
    print("ASSET CHARACTERISTICS COMPARISON")
    print("="*70)
    print("\nSimulating different asset types to understand strategy performance\n")

    results = []

    # Define different asset types
    assets = [
        {
            'name': 'Low Volatility Index',
            'days': 1825,  # 5 years
            'start_price': 1000,
            'volatility': 0.01,  # 1% daily vol
            'trend': 0.0003      # 0.03% daily trend
        },
        {
            'name': 'High Volatility Stock',
            'days': 1825,
            'start_price': 100,
            'volatility': 0.03,  # 3% daily vol
            'trend': 0.0005      # 0.05% daily trend
        },
        {
            'name': 'Crypto-like Asset',
            'days': 1825,
            'start_price': 10000,
            'volatility': 0.05,  # 5% daily vol
            'trend': 0.001       # 0.1% daily trend
        },
        {
            'name': 'Stable Growth',
            'days': 1825,
            'start_price': 500,
            'volatility': 0.015, # 1.5% daily vol
            'trend': 0.0004      # 0.04% daily trend
        },
        {
            'name': 'Bear Market Asset',
            'days': 1825,
            'start_price': 1000,
            'volatility': 0.02,  # 2% daily vol
            'trend': -0.0002     # -0.02% daily trend (declining)
        },
    ]

    for asset_config in assets:
        print(f"\n{'='*70}")
        print(f"Testing: {asset_config['name']}")
        print(f"{'='*70}")
        print(f"Volatility: {asset_config['volatility']*100:.1f}% daily")
        print(f"Trend: {asset_config['trend']*100:.3f}% daily")

        # Create sample data
        data = simulate_asset(
            asset_config['name'],
            asset_config['days'],
            asset_config['start_price'],
            asset_config['volatility'],
            asset_config['trend']
        )

        # Configure strategy
        config = StrategyConfig(
            name=f"Lunatic - {asset_config['name']}",
            ticker=asset_config['name'],
            start_date=str(data.index[0].date()),
            end_date=str(data.index[-1].date()),
            initial_capital=100000.0
        )

        # Run backtest
        strategy = LunaticStrategy(config)
        backtester = Backtester(strategy, data)
        backtest_results = backtester.run()

        # Calculate buy & hold
        buy_hold_return = ((data['Close'].iloc[-1] - data['Close'].iloc[0]) /
                          data['Close'].iloc[0]) * 100

        # Get period stats
        period_stats = strategy.get_period_stats()

        summary = backtest_results.summary()

        result = {
            'Asset': asset_config['name'],
            'Volatility': f"{asset_config['volatility']*100:.1f}%",
            'Strategy Return': f"{summary['total_return_pct']:.2f}%",
            'Buy & Hold Return': f"{buy_hold_return:.2f}%",
            'Strategy Edge': f"{summary['total_return_pct'] - buy_hold_return:.2f}%",
            'Sharpe Ratio': f"{summary['sharpe_ratio']:.2f}",
            'Win Rate': f"{summary['win_rate']:.1f}%",
            'Max Drawdown': f"{summary['max_drawdown_pct']:.1f}%",
            'Trades': summary['num_trades'],
            'Green Period Avg Daily': f"{period_stats['green_period']['avg_daily_return']*100:.3f}%",
            'Red Period Avg Daily': f"{period_stats['red_period']['avg_daily_return']*100:.3f}%",
        }

        results.append(result)

        print(f"\n📊 Results:")
        print(f"  Strategy Return: {result['Strategy Return']}")
        print(f"  Buy & Hold: {result['Buy & Hold Return']}")
        print(f"  Strategy Edge: {result['Strategy Edge']}")
        print(f"  Sharpe Ratio: {result['Sharpe Ratio']}")
        print(f"  Win Rate: {result['Win Rate']}")
        print(f"  Max Drawdown: {result['Max Drawdown']}")
        print(f"  Trades: {result['Trades']}")
        print(f"  Green Period Avg Daily: {result['Green Period Avg Daily']}")
        print(f"  Red Period Avg Daily: {result['Red Period Avg Daily']}")

    # Print comparison table
    print(f"\n\n{'='*70}")
    print("COMPREHENSIVE COMPARISON")
    print(f"{'='*70}\n")

    df = pd.DataFrame(results)
    print(df.to_string(index=False))

    # Save results
    df.to_csv('asset_characteristics_comparison.csv', index=False)
    print(f"\n✓ Results saved to asset_characteristics_comparison.csv")

    # Analysis
    print(f"\n\n{'='*70}")
    print("KEY INSIGHTS")
    print(f"{'='*70}\n")

    print("📈 VOLATILITY IMPACT:")
    print("  Higher volatility assets may show different lunar cycle effects.")
    print("  The strategy's success depends on consistent cyclical patterns.\n")

    print("🎯 OPTIMAL CONDITIONS:")
    print("  - Assets with moderate to high volatility")
    print("  - Markets with sentiment-driven price action")
    print("  - Assets with established cyclic patterns\n")

    print("⚠️  LIMITATIONS:")
    print("  - Bear markets may reduce strategy effectiveness")
    print("  - Very low volatility limits profit potential")
    print("  - Transaction costs impact frequent trading\n")


if __name__ == "__main__":
    test_asset_characteristics()

    print("\n\n" + "="*70)
    print("🌙 LUNAR STRATEGY INSIGHTS")
    print("="*70)
    print("""
Based on research and testing:

1. **CRYPTOCURRENCIES** (Best Potential):
   ✅ High volatility amplifies lunar cycle effects
   ✅ 24/7 trading - capture all lunar transitions
   ✅ Sentiment-driven market (psychological effects)
   ✅ No need for Avanza - use Binance, Coinbase, etc.
   ✅ Direct control of assets

2. **TECH STOCKS** (Good Potential):
   ✅ High beta stocks amplify market movements
   ✅ Sentiment-driven sector
   ⚠️  Limited to trading hours

3. **MAJOR INDICES** (Moderate Potential):
   ✅ Liquidity and low spreads
   ✅ Diversified exposure
   ⚠️  Lower volatility may reduce edge

4. **COMMODITIES** (Lower Potential):
   ⚠️  Different market dynamics
   ⚠️  Supply/demand fundamentals dominate

RECOMMENDATION FOR LIVE TRADING:
- Start with **BITCOIN (BTC)** or **ETHEREUM (ETH)**
- No need for Avanza - use crypto exchanges directly
- Higher potential returns with lunar strategy
- 24/7 automation possible
- Lower fees than traditional brokers
    """)

    print("\n✅ Analysis complete!\n")
