# Lunatic Trader - Lunar Cycle Trading Strategy

A comprehensive Python implementation of the Lunatic Trader strategy based on lunar cycle trading methodology from [blog.lunatictrader.com](https://blog.lunatictrader.com/performance/).

## 📖 Overview

The Lunatic Trader strategy is based on the observation that stock market performance varies with lunar cycles:

- **Green Periods** (New Moon → Full Moon): Bullish phase - Hold stocks
- **Red Periods** (Full Moon → New Moon): Bearish phase - Hold cash

**Strategy Rules:**
- ✅ **BUY** at the end of red periods (transition to green/new moon)
- ✅ **SELL** at the end of green periods (transition to red/full moon)
- 🌙 Trades occur approximately every 14-15 days

**Historical Performance (2009-2020 NASDAQ):**
- Green periods gained **6,147 points**
- Red periods gained only **2,019 points**
- Green periods outperformed in **8 of 12 years** tested

## 🏗️ Architecture

The implementation is modular and easily extensible:

```
trading_strategy/
├── lunar_calculator.py      # Lunar cycle calculations
├── strategy_base.py         # Base strategy class
├── lunatic_strategy.py      # Lunatic Trader implementation
├── backtester.py           # Backtesting engine
├── data_fetcher.py         # Data fetching (Yahoo, Avanza, CSV)
├── config.py               # Configuration management
├── example_backtest.py     # Backtest example
└── example_lunar_calculator.py  # Lunar calculator demo
```

## ✨ Features

- 🌙 **Accurate Lunar Calculations** - Precise lunar phase tracking
- 📊 **Comprehensive Backtesting** - Full performance metrics (Sharpe, Sortino, drawdown, etc.)
- 🔧 **Highly Customizable** - Easy to modify and extend
- 📈 **Multiple Data Sources** - Yahoo Finance, Avanza API (planned), CSV
- 🎯 **Position Sizing & Risk Management** - Stop loss, take profit, position sizing
- 📉 **Performance Analytics** - Period-by-period comparison (green vs red)
- 🔄 **Strategy Variants** - Standard, inverted, customizable entry/exit points

## 🚀 Quick Start

### Installation

```bash
# Install required packages
pip install pandas numpy yfinance matplotlib

# Optional: For Avanza API (future)
# pip install avanza
```

### Basic Usage

```python
from trading_strategy import (
    LunaticStrategy,
    Backtester,
    DataFetcher,
    NASDAQ_LUNATIC_CONFIG
)

# Fetch data
fetcher = DataFetcher(source='yahoo')
data = fetcher.fetch(
    ticker='^IXIC',
    start_date='2009-01-01',
    end_date='2020-12-31'
)

# Initialize strategy
strategy = LunaticStrategy(NASDAQ_LUNATIC_CONFIG)

# Run backtest
backtester = Backtester(strategy, data)
results = backtester.run()

# View results
results.print_summary()
strategy.print_period_stats()
```

### Run Examples

```bash
# Run backtest example
python example_backtest.py

# Explore lunar calculator
python example_lunar_calculator.py
```

## 📝 Configuration

### Preset Configurations

```python
from trading_strategy import (
    NASDAQ_LUNATIC_CONFIG,
    SP500_LUNATIC_CONFIG,
    CONSERVATIVE_CONFIG
)
```

### Custom Configuration

```python
from trading_strategy import StrategyConfig

config = StrategyConfig(
    name="My Strategy",
    ticker="^IXIC",
    start_date="2009-01-01",
    end_date="2020-12-31",
    initial_capital=100000.0,
    position_size_pct=1.0,      # Use 100% of capital
    commission=0.001,            # 0.1% commission
    slippage=0.0005,            # 0.05% slippage
    stop_loss_pct=0.05,         # 5% stop loss (optional)
    take_profit_pct=0.15        # 15% take profit (optional)
)
```

## 🎯 Strategy Variants

### Standard Strategy

```python
from trading_strategy import LunaticStrategy

strategy = LunaticStrategy(config)
# Buy at new moon, sell at full moon
```

### Inverted Strategy (Contrarian)

```python
from trading_strategy import LunaticStrategyAlternate

strategy = LunaticStrategyAlternate(config)
# Sell at new moon, buy at full moon
```

### Customizable Entry/Exit Points

```python
from trading_strategy import LunaticStrategyCustomizable

strategy = LunaticStrategyCustomizable(
    config,
    entry_phase_range=(0.0, 0.1),   # Enter in first 10% of cycle
    exit_phase_range=(0.45, 0.55)   # Exit around full moon
)
```

## 📊 Data Sources

### Yahoo Finance (Default)

```python
fetcher = DataFetcher(source='yahoo')
data = fetcher.fetch('^IXIC', '2009-01-01', '2020-12-31')
```

### CSV File

```python
fetcher = DataFetcher(source='csv')
data = fetcher.fetch('', '', '', file_path='my_data.csv')
```

### Avanza API (Planned)

```python
# Future implementation
fetcher = DataFetcher(source='avanza')
data = fetcher.fetch(
    ticker='INSTRUMENT_ID',
    start_date='2020-01-01',
    end_date='2024-01-01',
    credentials={'username': 'user', 'password': 'pass'},
    instrument_id='12345'
)
```

## 🔮 Lunar Calculator

The lunar calculator can be used independently:

```python
from trading_strategy import LunarCalculator
from datetime import datetime

calc = LunarCalculator()

# Get lunar info for a date
info = calc.get_lunar_info(datetime.now())
print(f"Phase: {info['phase_name']}")
print(f"Period: {info['period_type']}")  # 'green' or 'red'

# Check if date is in green period
is_green = calc.is_green_period('2024-01-15')

# Get upcoming transitions
transitions = calc.get_period_transitions('2024-01-01', '2024-12-31')
```

## 📈 Backtest Results

The backtester provides comprehensive metrics:

- **Returns:** Total return, CAGR, period-by-period analysis
- **Trade Statistics:** Win rate, avg win/loss, profit factor
- **Risk Metrics:** Max drawdown, Sharpe ratio, Sortino ratio
- **Equity Curve:** Complete portfolio value history
- **Trade Log:** Detailed log of all trades

## 🔧 Extending the Strategy

### Create Your Own Strategy

```python
from trading_strategy import StrategyBase
import pandas as pd

class MyCustomStrategy(StrategyBase):
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        # Your custom logic here
        data['signal'] = 0
        # Set data['signal'] = 1 for buy, -1 for sell
        return data

    def get_signal_explanation(self, date, signal):
        return f"Custom explanation for signal {signal}"
```

### Add Custom Indicators

```python
class EnhancedLunaticStrategy(LunaticStrategy):
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        # Get base lunar signals
        data = super().generate_signals(data)

        # Add your custom filters
        data['SMA_50'] = data['Close'].rolling(50).mean()
        data['SMA_200'] = data['Close'].rolling(200).mean()

        # Only take signals when price > SMA_200
        data.loc[data['Close'] < data['SMA_200'], 'signal'] = 0

        return data
```

## 🔜 Avanza API Integration (Planned)

The framework is designed for easy Avanza integration:

```python
from trading_strategy import AvanzaTrader

# Future implementation
trader = AvanzaTrader(
    credentials={'username': 'user', 'password': 'pass'},
    account_id='ACCOUNT_ID'
)

trader.authenticate()
positions = trader.get_positions()
trader.place_order(
    instrument_id='12345',
    order_type='limit',
    price=100.0,
    volume=10,
    side='buy'
)
```

**Integration Steps (TODO):**
1. Install `avanza` package
2. Implement authentication in `AvanzaTrader`
3. Add live data fetching
4. Implement order execution
5. Add position monitoring

## 📚 Examples

### Example 1: Basic Backtest

```python
from trading_strategy import *

config = NASDAQ_LUNATIC_CONFIG
fetcher = DataFetcher(source='yahoo')
data = fetcher.fetch('^IXIC', '2009-01-01', '2020-12-31')

strategy = LunaticStrategy(config)
backtester = Backtester(strategy, data)
results = backtester.run()

results.print_summary()
```

### Example 2: Compare Green vs Red Periods

```python
strategy = LunaticStrategy(config)
strategy.generate_signals(data)
strategy.print_period_stats()
```

### Example 3: Custom Risk Management

```python
config = StrategyConfig(
    name="Conservative Lunatic",
    ticker="^IXIC",
    position_size_pct=0.5,   # Only 50% of capital
    stop_loss_pct=0.03,      # 3% stop loss
    take_profit_pct=0.10     # 10% take profit
)
```

## 📄 License

This implementation is for educational and research purposes.

## 🙏 Acknowledgments

- Strategy methodology from [Lunatic Trader](https://blog.lunatictrader.com)
- Market data from Yahoo Finance
- Future integration with [Avanza API](https://qluxzz.github.io/avanza/avanza.html)

## 📞 Support

For questions or contributions, please open an issue or submit a pull request.

---

**Disclaimer:** This is for educational purposes only. Past performance does not guarantee future results. Always do your own research before trading.
