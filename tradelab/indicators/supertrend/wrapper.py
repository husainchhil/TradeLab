"""SUPERTREND Python wrapper for preserving docstring visibility in IDEs."""

from .supertrend import SUPERTREND as _SUPERTREND_cython
from ...utils.validate_data import validate_series


def SUPERTREND(high, low, close, period=10, multiplier=3.0):
    """
    Calculate SuperTrend indicator using Cython for performance.

    SuperTrend is a trend-following indicator that uses Average True Range (ATR) 
    to calculate dynamic support and resistance levels. It helps identify trend 
    direction and potential reversal points.

    Parameters
    ----------
    high : array-like
        High prices (numpy array or pandas Series)
    low : array-like
        Low prices (numpy array or pandas Series)
    close : array-like
        Close prices (numpy array or pandas Series)
    period : int, optional
        The period for ATR calculation (default: 10)
    multiplier : float, optional
        The multiplier for ATR to calculate SuperTrend bands (default: 3.0)

    Returns
    -------
    pandas.DataFrame
        DataFrame with columns:
        - Supertrend: SuperTrend line values
        - Direction: Trend direction (1 for uptrend, -1 for downtrend)

    Examples
    --------
    >>> import pandas as pd
    >>> import numpy as np
    >>> from tradelab.indicators.supertrend import SUPERTREND
    >>> 
    >>> # Sample OHLC data
    >>> high = pd.Series([12, 13, 14, 13, 15, 16, 15])
    >>> low = pd.Series([10, 11, 12, 11, 13, 14, 13])
    >>> close = pd.Series([11, 12, 13, 12, 14, 15, 14])
    >>> 
    >>> # Calculate SuperTrend
    >>> st = SUPERTREND(high, low, close, period=10, multiplier=3.0)
    >>> print(st)

    Notes
    -----
    - SuperTrend formula uses ATR-based bands:
      * Upper Band = (High + Low) / 2 + (multiplier × ATR)
      * Lower Band = (High + Low) / 2 - (multiplier × ATR)
    - When price is above SuperTrend line: uptrend (Direction = 1)
    - When price is below SuperTrend line: downtrend (Direction = -1)
    - Common parameters: period=10, multiplier=3.0
    - Higher multiplier = less sensitive, fewer signals
    - Lower multiplier = more sensitive, more signals
    - This implementation uses Cython for optimized performance
    """
    if not isinstance(period, int) or period <= 0:
        raise ValueError("Period must be a positive integer")

    if not isinstance(multiplier, (int, float)) or multiplier <= 0:
        raise ValueError("Multiplier must be a positive number")
    
    validate_series(high, "High")
    validate_series(low, "Low")
    validate_series(close, "Close")

    return _SUPERTREND_cython(high, low, close, period, multiplier)
