"""
Cryptocurrency Integration Example

Shows how to integrate the lunar strategy with crypto exchanges.
This is a template - you'll need to add your API keys.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime
import warnings
from trading_strategy import LunarCalculator

# Example 1: Check current lunar status
def check_lunar_status():
    """Check if we should be in or out of the market."""
    print("\n" + "="*70)
    print("CURRENT LUNAR STATUS")
    print("="*70)

    calc = LunarCalculator()
    today = datetime.now()
    lunar_info = calc.get_lunar_info(today)

    print(f"\nDate: {today.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Lunar Phase: {lunar_info['phase_name'].replace('_', ' ').title()}")
    print(f"Phase Progress: {lunar_info['phase_percent']*100:.1f}%")
    print(f"Period Type: {lunar_info['period_type'].upper()}")

    if lunar_info['period_type'] == 'green':
        print("\n✅ GREEN PERIOD - Should be LONG (holding crypto)")
        print("   → If not in position, consider BUYING")
    else:
        print("\n🔴 RED PERIOD - Should be in CASH (not holding)")
        print("   → If in position, consider SELLING")

    print(f"\nNext Transition: {lunar_info['next_transition_date'].strftime('%Y-%m-%d')}")
    print(f"Transitioning to: {lunar_info['next_period_type'].upper()} period")

    days_until = (lunar_info['next_transition_date'].date() - today.date()).days
    print(f"Days until transition: {days_until}")


# Example 2: Binance Integration (Template)
def binance_example():
    """
    Example Binance integration.

    To use this:
    1. Install: pip install python-binance
    2. Create Binance account and API keys
    3. Add your API keys below
    """
    print("\n" + "="*70)
    print("BINANCE INTEGRATION EXAMPLE")
    print("="*70)

    try:
        from binance.client import Client

        # TODO: Add your API keys here
        API_KEY = 'your_api_key_here'
        API_SECRET = 'your_api_secret_here'

        if API_KEY == 'your_api_key_here':
            print("\n⚠️  Please add your Binance API keys to use this example")
            print("   1. Create account at https://www.binance.com")
            print("   2. Go to API Management")
            print("   3. Create new API key")
            print("   4. Add keys to this script")
            return

        # Initialize client
        client = Client(API_KEY, API_SECRET)

        # Get account info
        account = client.get_account()
        print(f"\n✓ Connected to Binance")
        print(f"  Account Type: {account['accountType']}")

        # Get BTC balance
        btc_balance = client.get_asset_balance(asset='BTC')
        usdt_balance = client.get_asset_balance(asset='USDT')

        print(f"\nBalances:")
        print(f"  BTC: {btc_balance['free']}")
        print(f"  USDT: {usdt_balance['free']}")

        # Check lunar status
        calc = LunarCalculator()
        lunar_info = calc.get_lunar_info(datetime.now())

        print(f"\nLunar Status: {lunar_info['period_type'].upper()}")

        # Trading logic
        if lunar_info['period_type'] == 'green':
            if float(btc_balance['free']) > 0:
                print("✓ Already in position (holding BTC)")
            else:
                print("⚠️  Should be in BTC but currently in cash")
                print("   Consider buying BTC")
                # To place order (uncomment when ready):
                # order = client.order_market_buy(
                #     symbol='BTCUSDT',
                #     quoteOrderQty=1000  # Buy $1000 worth
                # )
        else:
            if float(btc_balance['free']) > 0:
                print("⚠️  Should be in cash but currently holding BTC")
                print("   Consider selling BTC")
                # To place order (uncomment when ready):
                # order = client.order_market_sell(
                #     symbol='BTCUSDT',
                #     quantity=btc_balance['free']
                # )
            else:
                print("✓ Correctly in cash position")

    except ImportError:
        print("\n⚠️  python-binance not installed")
        print("   Install with: pip install python-binance")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")


# Example 3: Coinbase Pro Integration (Template)
def coinbase_example():
    """
    Example Coinbase Pro integration.

    To use this:
    1. Install: pip install cbpro
    2. Create Coinbase Pro account and API keys
    3. Add your credentials below
    """
    print("\n" + "="*70)
    print("COINBASE PRO INTEGRATION EXAMPLE")
    print("="*70)

    try:
        import cbpro

        # TODO: Add your API credentials
        API_KEY = 'your_api_key'
        API_SECRET = 'your_api_secret'
        API_PASSPHRASE = 'your_passphrase'

        if API_KEY == 'your_api_key':
            print("\n⚠️  Please add your Coinbase Pro API credentials")
            print("   1. Create account at https://pro.coinbase.com")
            print("   2. Go to API settings")
            print("   3. Create new API key")
            print("   4. Add credentials to this script")
            return

        # Initialize client
        client = cbpro.AuthenticatedClient(
            API_KEY,
            API_SECRET,
            API_PASSPHRASE
        )

        # Get accounts
        accounts = client.get_accounts()

        print(f"\n✓ Connected to Coinbase Pro")

        # Find BTC and USD accounts
        for account in accounts:
            if account['currency'] in ['BTC', 'USD', 'USDC']:
                print(f"  {account['currency']}: {account['balance']}")

        # Check lunar status
        calc = LunarCalculator()
        lunar_info = calc.get_lunar_info(datetime.now())

        print(f"\nLunar Status: {lunar_info['period_type'].upper()}")

        # Trading logic similar to Binance example above

    except ImportError:
        print("\n⚠️  cbpro not installed")
        print("   Install with: pip install cbpro")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")


# Example 4: Scheduled Trading Bot
def create_trading_bot_example():
    """
    Example of a scheduled trading bot that checks lunar transitions.
    """
    print("\n" + "="*70)
    print("AUTOMATED TRADING BOT EXAMPLE")
    print("="*70)

    print("""
This is a template for an automated trading bot:

```python
import schedule
import time
from datetime import datetime
from trading_strategy import LunarCalculator

calc = LunarCalculator()
last_period = None

def check_and_trade():
    '''Check lunar status and execute trades if transition occurred.'''
    global last_period

    lunar_info = calc.get_lunar_info(datetime.now())
    current_period = lunar_info['period_type']

    # Check if period changed
    if last_period is not None and current_period != last_period:
        print(f"Lunar transition detected: {last_period} → {current_period}")

        if current_period == 'green':
            print("→ Executing BUY")
            # execute_buy()
        else:
            print("→ Executing SELL")
            # execute_sell()

    last_period = current_period

# Run every 4 hours
schedule.every(4).hours.do(check_and_trade)

print("Bot started - checking every 4 hours")
while True:
    schedule.run_pending()
    time.sleep(60)
```

To use this:
1. Install schedule: pip install schedule
2. Implement execute_buy() and execute_sell() functions
3. Run as background process or systemd service
4. Add logging and error handling
5. Set up alerts for trade execution
    """)


# Example 5: Get upcoming transitions for planning
def get_upcoming_transitions():
    """Show upcoming lunar transitions for the next 6 months."""
    print("\n" + "="*70)
    print("UPCOMING LUNAR TRANSITIONS (Next 6 Months)")
    print("="*70)

    calc = LunarCalculator()
    start = datetime.now()
    from datetime import timedelta
    end = start + timedelta(days=180)

    transitions = calc.get_period_transitions(start, end)

    print(f"\nTotal transitions: {len(transitions)}")
    print("\nSchedule:")

    for i, (date, period_type) in enumerate(transitions[:20], 1):
        action = "BUY (go long)" if period_type == 'green' else "SELL (go cash)"
        days_from_now = (date.date() - start.date()).days

        print(f"\n{i}. {date.strftime('%Y-%m-%d (%A)')}")
        print(f"   → {action}")
        print(f"   (in {days_from_now} days)")


# Example 6: Risk Management
def risk_management_example():
    """Example of adding risk management rules."""
    print("\n" + "="*70)
    print("RISK MANAGEMENT EXAMPLE")
    print("="*70)

    print("""
Recommended risk management rules for crypto lunar trading:

1. **Position Sizing:**
   - Start with 50% of capital
   - Scale to 100% after 3+ successful cycles
   - Never use leverage

2. **Stop Loss:**
   - Set at 10% for crypto (higher volatility)
   - Set at 5% for stocks
   - Exit immediately if triggered

3. **Portfolio Limits:**
   - Max 80% in any single crypto
   - Keep 20% cash reserve for opportunities
   - Diversify across BTC and ETH

4. **Trade Execution:**
   - Use limit orders when possible (better price)
   - Don't chase - if price moves 5%+ before entry, skip
   - Log all trades for analysis

5. **Monitoring:**
   - Check positions daily
   - Verify lunar calendar monthly
   - Review strategy quarterly

6. **Emergency Exit:**
   - Exit all positions if:
     * Market crashes 20%+ in single day
     * Major exchange hack/failure
     * Personal need for funds

Example implementation:

```python
def should_enter_trade(current_price, last_sell_price, position_size_pct):
    '''Determine if we should enter based on risk rules.'''

    # Rule 1: Don't chase
    if last_sell_price and current_price > last_sell_price * 1.05:
        print("Price moved too much, skipping entry")
        return False

    # Rule 2: Check available capital
    available_capital = get_available_capital()
    if available_capital < MIN_POSITION_SIZE:
        print("Insufficient capital")
        return False

    # Rule 3: Position sizing
    max_position = available_capital * position_size_pct
    if max_position < MIN_POSITION_SIZE:
        print("Position would be too small")
        return False

    return True
```
    """)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Crypto integration examples')
    parser.add_argument('--example', type=str, default='status',
                       choices=['status', 'binance', 'coinbase', 'bot',
                               'transitions', 'risk'],
                       help='Example to run')

    args = parser.parse_args()

    if args.example == 'status':
        check_lunar_status()
    elif args.example == 'binance':
        binance_example()
    elif args.example == 'coinbase':
        coinbase_example()
    elif args.example == 'bot':
        create_trading_bot_example()
    elif args.example == 'transitions':
        get_upcoming_transitions()
    elif args.example == 'risk':
        risk_management_example()

    print("\n" + "="*70)
    print("💡 NEXT STEPS")
    print("="*70)
    print("""
1. Choose a crypto exchange (Binance recommended)
2. Create account and generate API keys
3. Install exchange library: pip install python-binance
4. Test with paper trading first
5. Start with small capital ($1000-5000)
6. Track performance for 3-6 months
7. Scale up if results are positive

See OPTIMIZATION_GUIDE.md for detailed implementation roadmap.
    """)
