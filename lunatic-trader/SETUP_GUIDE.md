# Lunatic Trader - Local Setup Guide

## 📦 Download & Setup Instructions

### Method 1: Download Archive (Easiest)

1. **Download the archive:**
   - File location: `/home/user/lunatic-trader.tar.gz` (127 KB)
   - Use your file browser or download tool to get this file

2. **Extract on your local machine:**

   **On Mac/Linux:**
   ```bash
   # Navigate to your download location
   cd ~/Downloads

   # Extract
   tar -xzf lunatic-trader.tar.gz

   # Move to your projects folder
   mv lunatic-trader ~/Projects/
   cd ~/Projects/lunatic-trader
   ```

   **On Windows:**
   ```bash
   # Use 7-Zip, WinRAR, or Windows built-in
   # Right-click → Extract All

   # Or use WSL/Git Bash:
   tar -xzf lunatic-trader.tar.gz
   cd lunatic-trader
   ```

### Method 2: Clone from GitHub (After pushing)

```bash
git clone https://github.com/yourusername/lunatic-trader.git
cd lunatic-trader
```

---

## 🚀 Quick Start (After Download)

### Step 1: Install Python Requirements

```bash
# Navigate to project directory
cd lunatic-trader

# Create virtual environment (recommended)
python3 -m venv venv

# Activate virtual environment
# On Mac/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Or install individually:
pip install pandas numpy yfinance matplotlib scipy
```

### Step 2: Verify Installation

```bash
# Test lunar calculator
python3 -c "from lunatic import LunarCalculator; print('✓ Installation successful!')"

# Check current lunar status
python examples/example_lunar_calculator.py
```

### Step 3: Run Your First Backtest

```bash
# Quick test with sample data (no internet needed)
python examples/example_backtest.py

# Or try the comprehensive test (requires internet for real data)
python tests/run_comprehensive_tests.py --test quick
```

---

## 📊 Running Comprehensive Tests

### Option A: Quick Test (Bitcoin 2020-2024)

```bash
python tests/run_comprehensive_tests.py --test quick
```

**Expected output:**
- Buy-and-hold baseline
- Lunar strategy performance
- Monte Carlo statistical test (1000 simulations)
- Period analysis (green vs red)
- P-value and significance

**Time:** ~30 seconds (with internet) or ~instant (with cached data)

### Option B: Full Bitcoin Analysis

```bash
python tests/run_comprehensive_tests.py --test bitcoin
```

Tests across 5 time periods:
- 2015-2017, 2018-2019, 2020-2021, 2022-2023, 2015-2024

**Time:** ~5 minutes

### Option C: Cross-Asset Comparison (THE KEY TEST)

```bash
python tests/run_comprehensive_tests.py --test compare
```

Compares Bitcoin, Ethereum, NASDAQ, S&P 500 to determine if crypto lunar effects are real vs just volatility.

**Time:** ~10 minutes

### Option D: Run Everything

```bash
python tests/run_comprehensive_tests.py --test all
```

**Time:** ~30 minutes

---

## 🔧 Troubleshooting

### Issue: "No module named 'lunatic'"

**Solution:**
```bash
# Make sure you're in the project directory
cd lunatic-trader

# Install in development mode
pip install -e .
```

### Issue: "yfinance error" or "No data found"

**Solution 1:** Check internet connection

**Solution 2:** Use sample data instead:
```bash
# Edit examples/example_backtest.py
# Change data source from 'yahoo' to sample data
```

**Solution 3:** Install/upgrade yfinance:
```bash
pip install --upgrade yfinance
```

### Issue: "Module not found"

**Solution:** Ensure you activated virtual environment:
```bash
# Mac/Linux:
source venv/bin/activate

# Windows:
venv\Scripts\activate

# Then reinstall:
pip install -r requirements.txt
```

### Issue: Slow download / timeouts

**Solution:** Use smaller date ranges:
```python
# In the test file, change date ranges:
# From: '2015-01-01' to '2024-11-24'
# To:   '2020-01-01' to '2024-11-24'
```

---

## 📁 Project Structure

```
lunatic-trader/
├── lunatic/                    # Main package
│   ├── __init__.py
│   ├── lunar_calculator.py    # Moon phase calculations
│   ├── lunatic_strategy.py    # Trading strategy
│   ├── backtester.py          # Backtesting engine
│   ├── optimizer.py           # Optimization tools
│   ├── data_fetcher.py        # Data loading
│   ├── config.py              # Configuration
│   └── strategy_base.py       # Base classes
│
├── tests/                      # Scientific validation
│   ├── comprehensive_backtest.py   # Statistical tests
│   └── run_comprehensive_tests.py  # Test runner
│
├── examples/                   # Usage examples
│   ├── example_backtest.py
│   ├── example_lunar_calculator.py
│   └── crypto_integration_example.py
│
├── docs/                       # Documentation
│   └── OPTIMIZATION_GUIDE.md
│
├── results/                    # Output directory (auto-created)
│
├── README.md                   # Main documentation
├── PROJECT_SUMMARY.md          # Complete overview
├── setup.py                    # Package installer
├── requirements.txt            # Dependencies
└── LICENSE                     # MIT License
```

---

## 🎯 Recommended First Steps

### Day 1: Setup & Verify

```bash
# 1. Extract and navigate
cd lunatic-trader

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Test installation
python examples/example_lunar_calculator.py

# 5. Check current lunar status
python -c "from lunatic import LunarCalculator; from datetime import datetime; calc = LunarCalculator(); info = calc.get_lunar_info(datetime.now()); print(f'Current Period: {info[\"period_type\"].upper()}')"
```

### Day 1-2: Run Backtests

```bash
# Quick test (sample data)
python examples/example_backtest.py

# Quick test (real Bitcoin data)
python tests/run_comprehensive_tests.py --test quick

# Review results
cat results/*.csv  # or open in Excel
```

### Week 1: Analysis

```bash
# Run comprehensive Bitcoin analysis
python tests/run_comprehensive_tests.py --test bitcoin

# Run cross-asset comparison
python tests/run_comprehensive_tests.py --test compare

# Review all documentation
cat README.md
cat PROJECT_SUMMARY.md
cat docs/OPTIMIZATION_GUIDE.md
```

### Week 2-4: Paper Trading

```bash
# Check lunar status daily
python examples/crypto_integration_example.py --example status

# View upcoming transitions
python examples/crypto_integration_example.py --example transitions

# Log what trades you WOULD make
# (manual tracking in spreadsheet)
```

---

## 📊 Understanding the Output

### Backtest Results

**Sample Output:**
```
COMPREHENSIVE BACKTEST: BTC-USD
Period: 2020-01-01 to 2024-11-24

1. Buy-and-Hold Baseline...
  Total Return: 245.67%
  CAGR: 28.34%
  Sharpe Ratio: 0.95

2. Lunar Strategy...
  Total Return: 312.45%      ← Strategy return
  CAGR: 35.12%
  Win Rate: 57.4%
  Trades: 62

3. Statistical Significance...
  P-value: 0.0180            ← Key metric!
  Significant: YES ✓          ← p < 0.05 = significant

4. Period Analysis...
  Green Period Avg: 0.185%/day
  Red Period Avg: 0.042%/day
  Advantage: 0.143%/day      ← Daily edge
```

**What This Means:**

- **P-value < 0.05**: Strategy is statistically significant (not random)
- **P-value > 0.05**: Could be random chance
- **Strategy Return > Buy-Hold**: Strategy beats passive investing
- **Daily Advantage > 0**: Green periods outperform red periods

### Results Files

After running tests, check `results/` directory:

```bash
ls results/
# bitcoin_comprehensive_results.csv
# asset_class_comparison.csv
# backtest_trades.csv
# backtest_equity_curve.csv
```

Open in Excel or:
```bash
# View in terminal
column -t -s, results/asset_class_comparison.csv | less -S
```

---

## 🔑 Next Steps After Setup

### 1. Validate the Strategy

Run comprehensive tests to see if lunar effects are real:

```bash
python tests/run_comprehensive_tests.py --test compare
```

**Look for:**
- P-values < 0.05 for crypto
- Higher Sharpe ratios than buy-hold
- Consistent green > red advantage
- Edge persists after volatility adjustment

### 2. Decide on Asset

Based on results:
- **Bitcoin**: Best liquidity, most tested
- **Ethereum**: Good alternative
- **Both**: Diversification

### 3. Set Up Exchange

**For Crypto (Recommended):**
```bash
# Install Binance SDK
pip install python-binance

# Follow crypto_integration_example.py for setup
python examples/crypto_integration_example.py --example binance
```

### 4. Paper Trade

Track lunar transitions and log hypothetical trades for 2-3 months:

```bash
# Check status daily
python examples/crypto_integration_example.py --example status

# View next 10 transitions
python examples/crypto_integration_example.py --example transitions
```

### 5. Go Live (Only if paper trading successful)

Start with $1,000-5,000 and execute at lunar transitions.

---

## 💡 Pro Tips

### Tip 1: Use Virtual Environment

Always activate before running:
```bash
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
```

### Tip 2: Cache Data

First run downloads data and can be slow. Subsequent runs are faster.

### Tip 3: Start Small

Run `--test quick` first before full analysis.

### Tip 4: Read Documentation

- `README.md`: Overview and quick start
- `PROJECT_SUMMARY.md`: Complete technical details
- `docs/OPTIMIZATION_GUIDE.md`: Implementation guide

### Tip 5: Track Results

Keep a log of all backtests and paper trades:
```bash
# Append to log file
python tests/run_comprehensive_tests.py --test quick | tee -a backtest_log.txt
```

---

## 🆘 Getting Help

### Common Questions

**Q: Do I need an API key?**
A: Not for backtesting! Only for live trading with exchanges.

**Q: Can I run without internet?**
A: Yes, use the example files with sample data. For real backtests, you need internet once to download data.

**Q: How much capital do I need?**
A: For backtesting: $0. For paper trading: $0. For live trading: Start with $1,000-5,000.

**Q: Is this guaranteed to make money?**
A: NO! This is a statistical edge, not a guarantee. Always risk only what you can afford to lose.

### Support

- Check `README.md` for documentation
- Review `PROJECT_SUMMARY.md` for technical details
- Read example files in `examples/` directory
- Test files in `tests/` show how to use everything

---

## ✅ Checklist: First Hour

- [ ] Extract `lunatic-trader.tar.gz`
- [ ] Navigate to directory: `cd lunatic-trader`
- [ ] Create virtual environment: `python3 -m venv venv`
- [ ] Activate: `source venv/bin/activate`
- [ ] Install deps: `pip install -r requirements.txt`
- [ ] Test: `python examples/example_lunar_calculator.py`
- [ ] Run quick backtest: `python tests/run_comprehensive_tests.py --test quick`
- [ ] Review README.md
- [ ] Check results in `results/` directory

**After completing checklist, you're ready to explore! 🚀**

---

## 📞 Quick Reference

```bash
# Installation
pip install -r requirements.txt

# Check current lunar phase
python examples/example_lunar_calculator.py

# Quick backtest
python tests/run_comprehensive_tests.py --test quick

# Full analysis
python tests/run_comprehensive_tests.py --test all

# Crypto integration examples
python examples/crypto_integration_example.py --example status
python examples/crypto_integration_example.py --example transitions

# View results
ls results/
cat results/asset_class_comparison.csv
```

---

**You're all set! Extract the archive and start exploring. Good luck! 🌙📊**
