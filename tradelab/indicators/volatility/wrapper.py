"""ATR Python wrapper for preserving docstring visibility in IDEs."""

from .atr import ATR as _ATR_cython
from ...utils.validate_data import validate_series


def ATR(high, low, close, period=14, smoothing="RMA"):
    """
    Calculate Average True Range (ATR) using Cython for performance.

    The ATR is a volatility indicator that measures market volatility by 
    decomposing the entire range of an asset price for that period.

    Parameters
    ----------
    high : array-like
        High prices (numpy array or pandas Series)
    low : array-like
        Low prices (numpy array or pandas Series)
    close : array-like
        Close prices (numpy array or pandas Series)
    period : int, optional
        The period for ATR calculation (default: 14)
    smoothing : str, optional
        Smoothing type: "RMA", "SMA", "EMA", or "WMA" (default: "RMA")

    Returns
    -------
    pandas.Series
        Series with ATR values, indexed same as input if pandas Series

    Examples
    --------
    >>> import pandas as pd
    >>> import numpy as np
    >>> from tradelab.indicators.volatility.atr import ATR
    >>> 
    >>> # Sample OHLC data
    >>> high = pd.Series([12, 13, 11, 12, 14, 15, 13])
    >>> low = pd.Series([10, 11, 9, 10, 12, 13, 11])
    >>> close = pd.Series([11, 12, 10, 11, 13, 14, 12])
    >>> 
    >>> # Calculate 14-period ATR
    >>> atr_values = ATR(high, low, close, period=14)
    >>> print(atr_values)

    Notes
    -----
    - ATR measures volatility, not price direction
    - True Range is the maximum of:
      * Current High - Current Low
      * |Current High - Previous Close|
      * |Current Low - Previous Close|
    - ATR is the smoothed average of True Range values
    - This implementation uses Cython for optimized performance
    - RMA is equivalent to EMA with alpha = 1/period
    """
    validate_series(high, "High")
    validate_series(low, "Low")
    validate_series(close, "Close")

    if not isinstance(period, int) or period <= 0:
        raise ValueError("Period must be a positive integer")

    if not isinstance(smoothing, str):
        raise TypeError("Smoothing must be a string")

    smoothing_upper = smoothing.upper()
    if smoothing_upper not in ("RMA", "SMA", "EMA", "WMA"):
        raise ValueError("Smoothing must be one of: 'RMA', 'SMA', 'EMA', 'WMA'")

    smoothing_map = {
        "RMA": 0,
        "SMA": 1,
        "EMA": 2,
        "WMA": 3,
    }

    return _ATR_cython(high, low, close, period, smoothing_map[smoothing_upper])
