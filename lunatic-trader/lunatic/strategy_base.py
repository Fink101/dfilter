"""
Base class for trading strategies.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import pandas as pd


class Position:
    """Represents a trading position."""

    def __init__(self, ticker: str, quantity: float, entry_price: float,
                 entry_date: pd.Timestamp, position_type: str = 'long'):
        self.ticker = ticker
        self.quantity = quantity
        self.entry_price = entry_price
        self.entry_date = entry_date
        self.position_type = position_type
        self.exit_price: Optional[float] = None
        self.exit_date: Optional[pd.Timestamp] = None

    @property
    def is_open(self):
        """Check if position is still open."""
        return self.exit_price is None

    @property
    def value(self):
        """Get current position value (at entry if not closed)."""
        price = self.exit_price if self.exit_price else self.entry_price
        return self.quantity * price

    @property
    def pnl(self):
        """Calculate profit/loss."""
        if not self.exit_price:
            return 0.0

        if self.position_type == 'long':
            return (self.exit_price - self.entry_price) * self.quantity
        else:
            return (self.entry_price - self.exit_price) * self.quantity

    @property
    def pnl_percent(self):
        """Calculate profit/loss percentage."""
        if not self.exit_price:
            return 0.0

        if self.position_type == 'long':
            return ((self.exit_price - self.entry_price) / self.entry_price) * 100
        else:
            return ((self.entry_price - self.exit_price) / self.entry_price) * 100

    def close(self, exit_price: float, exit_date: pd.Timestamp):
        """Close the position."""
        self.exit_price = exit_price
        self.exit_date = exit_date

    def __repr__(self):
        status = "OPEN" if self.is_open else "CLOSED"
        return (f"Position({self.ticker}, {self.quantity:.2f} shares, "
                f"{status}, Entry: ${self.entry_price:.2f}, "
                f"PnL: ${self.pnl:.2f})")


class StrategyBase(ABC):
    """
    Abstract base class for all trading strategies.

    Subclasses must implement:
    - generate_signals(): Generate buy/sell signals
    - get_signal_explanation(): Explain why a signal was generated
    """

    def __init__(self, config):
        """
        Initialize the strategy.

        Args:
            config: StrategyConfig object
        """
        self.config = config
        self.positions = []
        self.current_position: Optional[Position] = None
        self.signals = None

    @abstractmethod
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Generate trading signals based on the strategy logic.

        Args:
            data: DataFrame with OHLCV price data

        Returns:
            DataFrame with added 'signal' column:
                1 = Buy signal
                -1 = Sell signal
                0 = Hold
        """
        pass

    @abstractmethod
    def get_signal_explanation(self, date: pd.Timestamp, signal: int) -> str:
        """
        Get a human-readable explanation of why a signal was generated.

        Args:
            date: Date of the signal
            signal: Signal value (1, -1, or 0)

        Returns:
            String explanation of the signal
        """
        pass

    def calculate_position_size(self, price: float, capital: float) -> float:
        """
        Calculate the number of shares to buy.

        Args:
            price: Current price per share
            capital: Available capital

        Returns:
            Number of shares to buy
        """
        # Calculate maximum shares based on position size percentage
        max_value = capital * self.config.position_size_pct

        # Apply maximum position size if set
        if self.config.max_position_size:
            max_value = min(max_value, self.config.max_position_size)

        # Calculate shares (accounting for commission and slippage)
        total_cost_multiplier = 1 + self.config.commission + self.config.slippage
        shares = max_value / (price * total_cost_multiplier)

        return shares

    def should_stop_loss(self, current_price: float) -> bool:
        """
        Check if stop loss should be triggered.

        Args:
            current_price: Current market price

        Returns:
            True if stop loss should trigger
        """
        if not self.current_position or not self.config.stop_loss_pct:
            return False

        if self.current_position.position_type == 'long':
            loss_pct = (self.current_position.entry_price - current_price) / self.current_position.entry_price
            return loss_pct >= self.config.stop_loss_pct

        return False

    def should_take_profit(self, current_price: float) -> bool:
        """
        Check if take profit should be triggered.

        Args:
            current_price: Current market price

        Returns:
            True if take profit should trigger
        """
        if not self.current_position or not self.config.take_profit_pct:
            return False

        if self.current_position.position_type == 'long':
            profit_pct = (current_price - self.current_position.entry_price) / self.current_position.entry_price
            return profit_pct >= self.config.take_profit_pct

        return False

    def open_position(self, ticker: str, quantity: float, price: float,
                     date: pd.Timestamp, position_type: str = 'long'):
        """Open a new position."""
        if self.current_position and self.current_position.is_open:
            raise ValueError("Cannot open new position while one is already open")

        position = Position(ticker, quantity, price, date, position_type)
        self.current_position = position
        self.positions.append(position)

        return position

    def close_position(self, price: float, date: pd.Timestamp):
        """Close the current position."""
        if not self.current_position or not self.current_position.is_open:
            raise ValueError("No open position to close")

        self.current_position.close(price, date)
        closed_position = self.current_position
        self.current_position = None

        return closed_position

    def get_open_position_value(self, current_price: float) -> float:
        """Get the current value of open position."""
        if not self.current_position or not self.current_position.is_open:
            return 0.0

        return self.current_position.quantity * current_price

    def get_total_pnl(self) -> float:
        """Calculate total profit/loss from all closed positions."""
        return sum(pos.pnl for pos in self.positions if not pos.is_open)

    def get_win_rate(self) -> float:
        """Calculate win rate percentage."""
        closed_positions = [pos for pos in self.positions if not pos.is_open]

        if not closed_positions:
            return 0.0

        winning_trades = sum(1 for pos in closed_positions if pos.pnl > 0)
        return (winning_trades / len(closed_positions)) * 100

    def get_stats(self) -> Dict[str, Any]:
        """Get strategy statistics."""
        closed_positions = [pos for pos in self.positions if not pos.is_open]

        if not closed_positions:
            return {
                'total_trades': 0,
                'winning_trades': 0,
                'losing_trades': 0,
                'win_rate': 0.0,
                'total_pnl': 0.0,
                'avg_win': 0.0,
                'avg_loss': 0.0,
            }

        winning_trades = [pos for pos in closed_positions if pos.pnl > 0]
        losing_trades = [pos for pos in closed_positions if pos.pnl < 0]

        return {
            'total_trades': len(closed_positions),
            'winning_trades': len(winning_trades),
            'losing_trades': len(losing_trades),
            'win_rate': self.get_win_rate(),
            'total_pnl': self.get_total_pnl(),
            'avg_win': sum(pos.pnl for pos in winning_trades) / len(winning_trades) if winning_trades else 0.0,
            'avg_loss': sum(pos.pnl for pos in losing_trades) / len(losing_trades) if losing_trades else 0.0,
        }
