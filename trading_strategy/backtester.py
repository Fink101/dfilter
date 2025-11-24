"""
Backtesting engine for trading strategies.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, Optional, List
from datetime import datetime


class BacktestResults:
    """Container for backtest results and performance metrics."""

    def __init__(self, equity_curve: pd.Series, positions: List,
                 trades: pd.DataFrame, config: Any):
        self.equity_curve = equity_curve
        self.positions = positions
        self.trades = trades
        self.config = config

        # Calculate metrics
        self._calculate_metrics()

    def _calculate_metrics(self):
        """Calculate performance metrics."""
        # Basic metrics
        self.initial_capital = self.equity_curve.iloc[0]
        self.final_capital = self.equity_curve.iloc[-1]
        self.total_return = self.final_capital - self.initial_capital
        self.total_return_pct = (self.total_return / self.initial_capital) * 100

        # Trade statistics
        closed_positions = [pos for pos in self.positions if not pos.is_open]
        self.num_trades = len(closed_positions)

        if self.num_trades > 0:
            winning_trades = [pos for pos in closed_positions if pos.pnl > 0]
            losing_trades = [pos for pos in closed_positions if pos.pnl < 0]

            self.num_winning = len(winning_trades)
            self.num_losing = len(losing_trades)
            self.win_rate = (self.num_winning / self.num_trades) * 100

            self.avg_win = sum(pos.pnl for pos in winning_trades) / len(winning_trades) if winning_trades else 0
            self.avg_loss = sum(pos.pnl for pos in losing_trades) / len(losing_trades) if losing_trades else 0

            self.largest_win = max((pos.pnl for pos in winning_trades), default=0)
            self.largest_loss = min((pos.pnl for pos in losing_trades), default=0)

            # Profit factor
            total_wins = sum(pos.pnl for pos in winning_trades)
            total_losses = abs(sum(pos.pnl for pos in losing_trades))
            self.profit_factor = total_wins / total_losses if total_losses > 0 else float('inf')
        else:
            self.num_winning = 0
            self.num_losing = 0
            self.win_rate = 0
            self.avg_win = 0
            self.avg_loss = 0
            self.largest_win = 0
            self.largest_loss = 0
            self.profit_factor = 0

        # Drawdown analysis
        self.max_drawdown, self.max_drawdown_pct = self._calculate_max_drawdown()

        # Returns analysis
        self.daily_returns = self.equity_curve.pct_change().dropna()

        if len(self.daily_returns) > 0:
            self.sharpe_ratio = self._calculate_sharpe_ratio()
            self.sortino_ratio = self._calculate_sortino_ratio()
        else:
            self.sharpe_ratio = 0
            self.sortino_ratio = 0

        # Time-based metrics
        self.start_date = self.equity_curve.index[0]
        self.end_date = self.equity_curve.index[-1]
        self.duration_days = (self.end_date - self.start_date).days

        if self.duration_days > 0:
            self.cagr = self._calculate_cagr()
        else:
            self.cagr = 0

    def _calculate_max_drawdown(self):
        """Calculate maximum drawdown."""
        cumulative_max = self.equity_curve.expanding().max()
        drawdown = self.equity_curve - cumulative_max
        max_dd = drawdown.min()
        max_dd_pct = (max_dd / cumulative_max.loc[drawdown.idxmin()]) * 100

        return max_dd, max_dd_pct

    def _calculate_sharpe_ratio(self, risk_free_rate=0.02):
        """Calculate Sharpe ratio (annualized)."""
        if len(self.daily_returns) == 0 or self.daily_returns.std() == 0:
            return 0

        excess_returns = self.daily_returns - (risk_free_rate / 252)
        sharpe = np.sqrt(252) * (excess_returns.mean() / self.daily_returns.std())

        return sharpe

    def _calculate_sortino_ratio(self, risk_free_rate=0.02):
        """Calculate Sortino ratio (annualized)."""
        if len(self.daily_returns) == 0:
            return 0

        excess_returns = self.daily_returns - (risk_free_rate / 252)
        downside_returns = self.daily_returns[self.daily_returns < 0]

        if len(downside_returns) == 0 or downside_returns.std() == 0:
            return 0

        sortino = np.sqrt(252) * (excess_returns.mean() / downside_returns.std())

        return sortino

    def _calculate_cagr(self):
        """Calculate Compound Annual Growth Rate."""
        years = self.duration_days / 365.25
        if years == 0:
            return 0

        cagr = (((self.final_capital / self.initial_capital) ** (1 / years)) - 1) * 100

        return cagr

    def summary(self) -> Dict[str, Any]:
        """Get summary of backtest results."""
        return {
            'start_date': self.start_date,
            'end_date': self.end_date,
            'duration_days': self.duration_days,
            'initial_capital': self.initial_capital,
            'final_capital': self.final_capital,
            'total_return': self.total_return,
            'total_return_pct': self.total_return_pct,
            'cagr': self.cagr,
            'num_trades': self.num_trades,
            'num_winning': self.num_winning,
            'num_losing': self.num_losing,
            'win_rate': self.win_rate,
            'avg_win': self.avg_win,
            'avg_loss': self.avg_loss,
            'largest_win': self.largest_win,
            'largest_loss': self.largest_loss,
            'profit_factor': self.profit_factor,
            'max_drawdown': self.max_drawdown,
            'max_drawdown_pct': self.max_drawdown_pct,
            'sharpe_ratio': self.sharpe_ratio,
            'sortino_ratio': self.sortino_ratio,
        }

    def print_summary(self):
        """Print a formatted summary of results."""
        print("\n" + "=" * 70)
        print(f"BACKTEST RESULTS: {self.config.name}")
        print("=" * 70)

        print(f"\nPERIOD: {self.start_date.strftime('%Y-%m-%d')} to {self.end_date.strftime('%Y-%m-%d')}")
        print(f"Duration: {self.duration_days} days")

        print("\n--- RETURNS ---")
        print(f"Initial Capital:    ${self.initial_capital:,.2f}")
        print(f"Final Capital:      ${self.final_capital:,.2f}")
        print(f"Total Return:       ${self.total_return:,.2f} ({self.total_return_pct:.2f}%)")
        print(f"CAGR:               {self.cagr:.2f}%")

        print("\n--- TRADES ---")
        print(f"Total Trades:       {self.num_trades}")
        print(f"Winning Trades:     {self.num_winning}")
        print(f"Losing Trades:      {self.num_losing}")
        print(f"Win Rate:           {self.win_rate:.2f}%")

        print("\n--- PROFIT/LOSS ---")
        print(f"Average Win:        ${self.avg_win:,.2f}")
        print(f"Average Loss:       ${self.avg_loss:,.2f}")
        print(f"Largest Win:        ${self.largest_win:,.2f}")
        print(f"Largest Loss:       ${self.largest_loss:,.2f}")
        print(f"Profit Factor:      {self.profit_factor:.2f}")

        print("\n--- RISK METRICS ---")
        print(f"Max Drawdown:       ${self.max_drawdown:,.2f} ({self.max_drawdown_pct:.2f}%)")
        print(f"Sharpe Ratio:       {self.sharpe_ratio:.2f}")
        print(f"Sortino Ratio:      {self.sortino_ratio:.2f}")

        print("\n" + "=" * 70 + "\n")


class Backtester:
    """
    Backtesting engine for trading strategies.
    """

    def __init__(self, strategy, data: pd.DataFrame):
        """
        Initialize the backtester.

        Args:
            strategy: Strategy object (inherits from StrategyBase)
            data: DataFrame with OHLCV price data
        """
        self.strategy = strategy
        self.data = data.copy()
        self.config = strategy.config

        # Portfolio tracking
        self.cash = self.config.initial_capital
        self.equity_curve = []
        self.trades = []

    def run(self) -> BacktestResults:
        """
        Run the backtest.

        Returns:
            BacktestResults object
        """
        print(f"\nRunning backtest: {self.config.name}")
        print(f"Period: {self.data.index[0]} to {self.data.index[-1]}")
        print(f"Initial Capital: ${self.config.initial_capital:,.2f}\n")

        # Generate signals
        self.data = self.strategy.generate_signals(self.data)

        # Simulate trading
        for date, row in self.data.iterrows():
            current_price = row['Close']

            # Check for stop loss or take profit
            if self.strategy.current_position:
                if self.strategy.should_stop_loss(current_price):
                    self._execute_sell(date, current_price, "Stop Loss")
                elif self.strategy.should_take_profit(current_price):
                    self._execute_sell(date, current_price, "Take Profit")

            # Process signals
            signal = row.get('signal', 0)

            if signal == 1 and not self.strategy.current_position:
                # Buy signal
                self._execute_buy(date, current_price)

            elif signal == -1 and self.strategy.current_position:
                # Sell signal
                self._execute_sell(date, current_price, "Signal")

            # Calculate current portfolio value
            portfolio_value = self.cash
            if self.strategy.current_position:
                portfolio_value += self.strategy.current_position.quantity * current_price

            self.equity_curve.append({'date': date, 'equity': portfolio_value})

        # Close any remaining open position
        if self.strategy.current_position:
            last_date = self.data.index[-1]
            last_price = self.data.loc[last_date, 'Close']
            self._execute_sell(last_date, last_price, "End of Backtest")

        # Create results
        equity_df = pd.DataFrame(self.equity_curve).set_index('date')
        trades_df = pd.DataFrame(self.trades)

        results = BacktestResults(
            equity_curve=equity_df['equity'],
            positions=self.strategy.positions,
            trades=trades_df,
            config=self.config
        )

        return results

    def _execute_buy(self, date: pd.Timestamp, price: float):
        """Execute a buy order."""
        # Calculate position size
        quantity = self.strategy.calculate_position_size(price, self.cash)

        if quantity <= 0:
            return

        # Calculate costs
        cost = quantity * price
        commission = cost * self.config.commission
        slippage = cost * self.config.slippage
        total_cost = cost + commission + slippage

        if total_cost > self.cash:
            # Adjust quantity if not enough cash
            quantity = self.cash / (price * (1 + self.config.commission + self.config.slippage))
            total_cost = self.cash

        if quantity <= 0:
            return

        # Update cash
        self.cash -= total_cost

        # Open position
        self.strategy.open_position(
            ticker=self.config.ticker,
            quantity=quantity,
            price=price,
            date=date
        )

        # Record trade
        self.trades.append({
            'date': date,
            'action': 'BUY',
            'price': price,
            'quantity': quantity,
            'cost': total_cost,
            'cash_remaining': self.cash
        })

    def _execute_sell(self, date: pd.Timestamp, price: float, reason: str = "Signal"):
        """Execute a sell order."""
        if not self.strategy.current_position:
            return

        position = self.strategy.current_position
        quantity = position.quantity

        # Calculate proceeds
        proceeds = quantity * price
        commission = proceeds * self.config.commission
        slippage = proceeds * self.config.slippage
        net_proceeds = proceeds - commission - slippage

        # Update cash
        self.cash += net_proceeds

        # Close position
        closed_position = self.strategy.close_position(price, date)

        # Record trade
        self.trades.append({
            'date': date,
            'action': f'SELL ({reason})',
            'price': price,
            'quantity': quantity,
            'proceeds': net_proceeds,
            'pnl': closed_position.pnl,
            'pnl_pct': closed_position.pnl_percent,
            'cash_remaining': self.cash
        })

    def plot_results(self, results: BacktestResults, save_path: Optional[str] = None):
        """
        Plot backtest results.

        Args:
            results: BacktestResults object
            save_path: Optional path to save the plot
        """
        try:
            import matplotlib.pyplot as plt

            fig, axes = plt.subplots(2, 1, figsize=(14, 10))

            # Plot equity curve
            ax1 = axes[0]
            results.equity_curve.plot(ax=ax1, label='Portfolio Value', linewidth=2)
            ax1.set_title(f'{self.config.name} - Equity Curve', fontsize=14, fontweight='bold')
            ax1.set_xlabel('Date')
            ax1.set_ylabel('Portfolio Value ($)')
            ax1.grid(True, alpha=0.3)
            ax1.legend()

            # Plot price with buy/sell signals
            ax2 = axes[1]
            self.data['Close'].plot(ax=ax2, label='Price', linewidth=1.5, alpha=0.7)

            # Mark buy and sell signals
            buy_signals = self.data[self.data['signal'] == 1]
            sell_signals = self.data[self.data['signal'] == -1]

            ax2.scatter(buy_signals.index, buy_signals['Close'],
                       marker='^', color='green', s=100, label='Buy', zorder=5)
            ax2.scatter(sell_signals.index, sell_signals['Close'],
                       marker='v', color='red', s=100, label='Sell', zorder=5)

            ax2.set_title(f'{self.config.ticker} - Price & Signals', fontsize=14, fontweight='bold')
            ax2.set_xlabel('Date')
            ax2.set_ylabel('Price ($)')
            ax2.grid(True, alpha=0.3)
            ax2.legend()

            plt.tight_layout()

            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches='tight')
                print(f"\nPlot saved to: {save_path}")

            plt.show()

        except ImportError:
            print("\nWarning: matplotlib not installed. Skipping plot generation.")
            print("Install with: pip install matplotlib")
