"""
Lunatic Trader - Lunar Cycle Trading Strategy

A modular Python implementation of the Lunatic Trader strategy based on
lunar cycle trading methodology.

Main components:
- LunarCalculator: Calculate lunar phases and periods
- LunaticStrategy: Core trading strategy
- Backtester: Backtest the strategy
- DataFetcher: Fetch market data from multiple sources
- StrategyConfig: Configuration management
"""

from .lunar_calculator import LunarCalculator
from .strategy_base import StrategyBase, Position
from .lunatic_strategy import (
    LunaticStrategy,
    LunaticStrategyAlternate,
    LunaticStrategyCustomizable
)
from .backtester import Backtester, BacktestResults
from .data_fetcher import DataFetcher, AvanzaTrader, create_sample_data
from .config import (
    StrategyConfig,
    NASDAQ_LUNATIC_CONFIG,
    SP500_LUNATIC_CONFIG,
    CONSERVATIVE_CONFIG
)

__version__ = '1.0.0'
__author__ = 'Lunatic Trader Strategy Implementation'

__all__ = [
    'LunarCalculator',
    'StrategyBase',
    'Position',
    'LunaticStrategy',
    'LunaticStrategyAlternate',
    'LunaticStrategyCustomizable',
    'Backtester',
    'BacktestResults',
    'DataFetcher',
    'AvanzaTrader',
    'create_sample_data',
    'StrategyConfig',
    'NASDAQ_LUNATIC_CONFIG',
    'SP500_LUNATIC_CONFIG',
    'CONSERVATIVE_CONFIG',
]
