"""
Configuration management for trading strategies.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, Optional


@dataclass
class StrategyConfig:
    """
    Configuration for trading strategies.
    """
    # General settings
    name: str = "Lunatic Trader"
    initial_capital: float = 100000.0
    commission: float = 0.001  # 0.1% commission
    slippage: float = 0.0005   # 0.05% slippage

    # Position sizing
    position_size_pct: float = 1.0  # Use 100% of capital when in position
    max_position_size: Optional[float] = None  # Maximum position size in currency

    # Risk management
    stop_loss_pct: Optional[float] = None  # Stop loss percentage (e.g., 0.02 for 2%)
    take_profit_pct: Optional[float] = None  # Take profit percentage

    # Lunar strategy specific
    lunar_green_start: str = 'new_moon'
    lunar_green_end: str = 'full_moon'

    # Data settings
    data_source: str = 'yahoo'  # 'yahoo', 'avanza', or 'csv'
    ticker: str = '^IXIC'  # Default to NASDAQ

    # Backtesting settings
    start_date: str = '2009-01-01'
    end_date: str = '2020-12-31'

    # Avanza API settings (for future use)
    avanza_credentials: Optional[Dict[str, str]] = None
    avanza_account_id: Optional[str] = None

    # Custom parameters
    custom_params: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate configuration after initialization."""
        if self.position_size_pct <= 0 or self.position_size_pct > 1:
            raise ValueError("position_size_pct must be between 0 and 1")

        if self.commission < 0 or self.commission > 0.1:
            raise ValueError("commission must be between 0 and 0.1 (10%)")

        if self.initial_capital <= 0:
            raise ValueError("initial_capital must be positive")

    def to_dict(self):
        """Convert config to dictionary."""
        return {
            'name': self.name,
            'initial_capital': self.initial_capital,
            'commission': self.commission,
            'slippage': self.slippage,
            'position_size_pct': self.position_size_pct,
            'max_position_size': self.max_position_size,
            'stop_loss_pct': self.stop_loss_pct,
            'take_profit_pct': self.take_profit_pct,
            'lunar_green_start': self.lunar_green_start,
            'lunar_green_end': self.lunar_green_end,
            'data_source': self.data_source,
            'ticker': self.ticker,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'custom_params': self.custom_params
        }

    @classmethod
    def from_dict(cls, config_dict):
        """Create config from dictionary."""
        return cls(**config_dict)


# Preset configurations
NASDAQ_LUNATIC_CONFIG = StrategyConfig(
    name="NASDAQ Lunatic Trader",
    ticker="^IXIC",
    start_date="2009-01-01",
    end_date="2020-12-31",
    initial_capital=100000.0
)

SP500_LUNATIC_CONFIG = StrategyConfig(
    name="S&P 500 Lunatic Trader",
    ticker="^GSPC",
    start_date="2009-01-01",
    end_date="2020-12-31",
    initial_capital=100000.0
)

CONSERVATIVE_CONFIG = StrategyConfig(
    name="Conservative Lunatic Trader",
    ticker="^IXIC",
    position_size_pct=0.5,  # Only use 50% of capital
    stop_loss_pct=0.05,     # 5% stop loss
    initial_capital=100000.0
)
