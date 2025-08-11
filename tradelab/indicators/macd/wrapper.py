"""MACD (Moving Average Convergence Divergence) indicator wrapper."""

import pandas as pd
import numpy as np
from ...utils.validate_data import validate_series

try:
    from .macd import MACD as _MACD_cython
except ImportError:
    # Fallback for development (before Cython compilation)
    def _MACD_cython(src, fast_period=12, slow_period=26, signal_period=9):
        raise ImportError(
            "Cython module not compiled. Please run 'pip install -e .' first.")


def MACD(src, fast_period=12, slow_period=26, signal_period=9):
    """
    Calculate MACD (Moving Average Convergence Divergence) indicator.

    MACD is a trend-following momentum indicator that shows the relationship
    between two moving averages of a security's price. The MACD is calculated
    by subtracting the slow EMA from the fast EMA.

    Parameters:
    -----------
    src : pd.Series or array-like
        Source price series (typically close prices)
    fast_period : int, default 12
        Period for the fast EMA (typically 12)
    slow_period : int, default 26
        Period for the slow EMA (typically 26)
    signal_period : int, default 9
        Period for the signal line EMA (typically 9)

    Returns:
    --------
    pd.DataFrame
        DataFrame with columns ['MACD', 'Signal', 'Histogram']
        - MACD: Fast EMA - Slow EMA
        - Signal: EMA of MACD line
        - Histogram: MACD - Signal

    Raises:
    -------
    ValueError
        If fast_period >= slow_period
        If any period is less than 1
        If data contains null or infinite values

    Examples:
    ---------
    >>> # Basic MACD calculation
    >>> macd_df = MACD(data['Close'])
    >>> print(macd_df.columns)
    Index(['MACD', 'Signal', 'Histogram'], dtype='object')

    >>> # Custom parameters
    >>> custom_macd = MACD(data['Close'], fast_period=8, slow_period=21, signal_period=5)

    Notes:
    ------
    - MACD Line = Fast EMA - Slow EMA
    - Signal Line = EMA of MACD Line
    - Histogram = MACD Line - Signal Line
    - This implementation uses Cython for optimized performance
    """
    # Validate input data using utils validation
    src = validate_series(src, "Source")

    # Validate parameters
    if not isinstance(fast_period, int) or fast_period <= 0:
        raise ValueError("fast_period must be a positive integer")

    if not isinstance(slow_period, int) or slow_period <= 0:
        raise ValueError("slow_period must be a positive integer")

    if not isinstance(signal_period, int) or signal_period <= 0:
        raise ValueError("signal_period must be a positive integer")

    if fast_period >= slow_period:
        raise ValueError("fast_period must be less than slow_period")

    return _MACD_cython(src, fast_period, slow_period, signal_period)
