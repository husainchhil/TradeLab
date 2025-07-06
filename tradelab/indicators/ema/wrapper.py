"""EMA Python wrapper for preserving docstring visibility in IDEs."""

from .ema import EMA as _EMA_cython


def EMA(src, period):
    """
    Calculate Exponential Moving Average using Cython for performance.

    The EMA is a type of moving average that gives more weight to recent prices,
    making it more responsive to new information than a simple moving average.

    Parameters
    ----------
    src : array-like
        Source prices (numpy array or pandas Series)
    period : int
        The period for EMA calculation

    Returns
    -------
    pandas.Series
        Series with EMA values, indexed same as input if pandas Series

    Examples
    --------
    >>> import pandas as pd
    >>> import numpy as np
    >>> from tradelab.indicators.ema import EMA
    >>> 
    >>> # Sample data
    >>> prices = pd.Series([10, 11, 12, 11, 10, 9, 8, 9, 10, 11])
    >>> 
    >>> # Calculate 5-period EMA
    >>> ema_values = EMA(prices, period=5)
    >>> print(ema_values)

    Notes
    -----
    - EMA reacts more quickly to price changes than SMA
    - The smoothing factor alpha = 2/(period + 1)
    - This implementation uses Cython for optimized performance
    """
    return _EMA_cython(src, period)
