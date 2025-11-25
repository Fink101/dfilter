"""
Example: Running a backtest of the Lunatic Trader strategy

This script demonstrates how to:
1. Fetch historical data
2. Configure the strategy
3. Run a backtest
4. Analyze results
"""

from trading_strategy import (
    LunaticStrategy,
    Backtester,
    DataFetcher,
    StrategyConfig,
    NASDAQ_LUNATIC_CONFIG
)


def main():
    """Run a basic backtest example."""

    print("=" * 70)
    print("LUNATIC TRADER STRATEGY - BACKTEST EXAMPLE")
    print("=" * 70)

    # Option 1: Use preset configuration
    config = NASDAQ_LUNATIC_CONFIG

    # Option 2: Create custom configuration
    # config = StrategyConfig(
    #     name="My Custom Strategy",
    #     ticker="^IXIC",
    #     start_date="2009-01-01",
    #     end_date="2020-12-31",
    #     initial_capital=100000.0,
    #     position_size_pct=1.0,
    #     commission=0.001,
    #     slippage=0.0005
    # )

    # Fetch data
    fetcher = DataFetcher(source='yahoo')

    try:
        data = fetcher.fetch(
            ticker=config.ticker,
            start_date=config.start_date,
            end_date=config.end_date
        )
    except Exception as e:
        print(f"\nError fetching data: {e}")
        print("\nFalling back to sample data for demonstration...")

        from trading_strategy import create_sample_data
        import pandas as pd

        # Create sample data
        data = create_sample_data(days=365*12, start_price=2000)
        data.index = pd.date_range(start='2009-01-01', periods=len(data), freq='D')

    print(f"\nData loaded: {len(data)} trading days")
    print(f"Date range: {data.index[0]} to {data.index[-1]}")

    # Initialize strategy
    strategy = LunaticStrategy(config)

    # Run backtest
    backtester = Backtester(strategy, data)
    results = backtester.run()

    # Print results
    results.print_summary()

    # Print lunar period statistics
    strategy.print_period_stats()

    # Show some example signals
    print("\nSAMPLE TRADING SIGNALS:")
    print("=" * 70)

    signals_df = strategy.signals[strategy.signals['signal'] != 0].head(10)

    for date, row in signals_df.iterrows():
        signal = int(row['signal'])
        print(f"\nDate: {date.strftime('%Y-%m-%d')}")
        print(f"Price: ${row['Close']:.2f}")
        print(strategy.get_signal_explanation(date, signal))
        print("-" * 70)

    # Optionally save results to CSV
    print("\nSaving results to CSV...")
    results.trades.to_csv('backtest_trades.csv', index=False)
    results.equity_curve.to_csv('backtest_equity_curve.csv')
    print("Results saved to: backtest_trades.csv and backtest_equity_curve.csv")

    # Try to plot results (requires matplotlib)
    try:
        backtester.plot_results(results, save_path='backtest_results.png')
    except ImportError:
        print("\nNote: Install matplotlib to generate plots: pip install matplotlib")

    print("\n" + "=" * 70)
    print("BACKTEST COMPLETE")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
