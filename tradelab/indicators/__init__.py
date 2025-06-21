"""Technical indicators package."""

# Import from categorized modules
from .trend import supertrend, SuperTrend, ema, EMA, normalized_t3, NormalizedT3
from .volatility import atr, ATR
from .momentum import adx, ADX, rsi, RSI
from .comparative import relative_strength, RelativeStrength
from .base import BaseIndicator

# Maintain backward compatibility
__all__ = [
    # Trend indicators
    'supertrend', 'SuperTrend', 'ema', 'EMA', 'normalized_t3', 'NormalizedT3',
    # Volatility indicators
    'atr', 'ATR',
    # Momentum indicators
    'adx', 'ADX', 'rsi', 'RSI',
    # Comparative indicators
    'relative_strength', 'RelativeStrength',
    # Base class
    'BaseIndicator'
]
