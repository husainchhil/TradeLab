"""RSI Python wrapper for preserving docstring visibility in IDEs."""

from .rsi import RSI as _RSI_cython


def RSI(src, period=14):
    """
    Calculate Relative Strength Index (RSI) using Cython for performance.

    The RSI is a momentum oscillator that measures the speed and change of price movements.
    It oscillates between 0 and 100, with readings above 70 typically considered overbought
    and readings below 30 considered oversold.

    Parameters
    ----------
    src : array-like
        Source prices (numpy array or pandas Series)
    period : int, optional
        The period for RSI calculation (default: 14)

    Returns
    -------
    pandas.Series
        Series with RSI values (0-100), indexed same as input if pandas Series

    Examples
    --------
    >>> import pandas as pd
    >>> import numpy as np
    >>> from tradelab.indicators.rsi import RSI
    >>> 
    >>> # Sample price data
    >>> prices = pd.Series([100, 102, 101, 103, 105, 104, 106, 108, 107, 109])
    >>> 
    >>> # Calculate 14-period RSI
    >>> rsi_values = RSI(prices, period=14)
    >>> print(rsi_values)

    Notes
    -----
    - RSI formula: RSI = 100 - (100 / (1 + RS))
    - RS = Average Gain / Average Loss over the specified period
    - Uses exponential moving average for smoothing (equivalent to Wilder's smoothing)
    - Values above 70 typically indicate overbought conditions
    - Values below 30 typically indicate oversold conditions
    - This implementation uses Cython for optimized performance
    """
    if not isinstance(period, int) or period <= 0:
        raise ValueError("Period must be a positive integer")

    return _RSI_cython(src, period)
