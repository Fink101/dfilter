"""
Test the trading strategy with sample data.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from datetime import datetime
from trading_strategy import (
    LunaticStrategy,
    Backtester,
    StrategyConfig,
    create_sample_data
)

# Create sample data
print("Creating sample market data...")
data = create_sample_data(days=365*12, start_price=2000)
data.index = pd.date_range(start='2009-01-01', periods=len(data), freq='D')

print(f"✓ Created {len(data)} days of data")
print(f"  Date range: {data.index[0]} to {data.index[-1]}")
print(f"  Price range: ${data['Close'].min():.2f} - ${data['Close'].max():.2f}")

# Configure strategy
config = StrategyConfig(
    name="Lunatic Trader Test",
    ticker="TEST",
    start_date="2009-01-01",
    end_date="2020-12-31",
    initial_capital=100000.0,
    position_size_pct=1.0,
    commission=0.001,
    slippage=0.0005
)

print("\n" + "=" * 70)
print("Initializing strategy...")
strategy = LunaticStrategy(config)

print("Running backtest...")
backtester = Backtester(strategy, data)
results = backtester.run()

# Print results
results.print_summary()

# Print period stats
strategy.print_period_stats()

# Show first few signals
print("\nFIRST 5 TRADING SIGNALS:")
print("=" * 70)
signals_df = strategy.signals[strategy.signals['signal'] != 0].head(5)

for date, row in signals_df.iterrows():
    signal = int(row['signal'])
    print(f"\nDate: {date.strftime('%Y-%m-%d')}")
    print(f"Price: ${row['Close']:.2f}")
    print(f"Lunar Phase: {row['lunar_phase']}")
    print(f"Period: {row['period_type']}")
    print(f"Signal: {'BUY' if signal == 1 else 'SELL'}")
    print("-" * 70)

print("\n✓ Strategy test completed successfully!")
