"""Donchian Channels Python wrapper for preserving docstring visibility in IDEs."""

import pandas as pd
import numpy as np

try:
    from .donchian_channels import DONCHIAN_CHANNELS as _DONCHIAN_CHANNELS_cython
except ImportError:
    # Fallback for development (before Cython compilation)
    def _DONCHIAN_CHANNELS_cython(high, low, period):
        raise ImportError(
            "Cython module not compiled. Please run 'pip install -e .' first.")


def DONCHIAN_CHANNELS(high, low, period=20):
    """
    Calculate Donchian Channels using Cython for performance.

    Donchian Channels are volatility indicators that show the highest high and 
    lowest low over a specific period, creating dynamic support and resistance levels.

    Parameters
    ----------
    high : array-like
        High prices (numpy array or pandas Series)
    low : array-like
        Low prices (numpy array or pandas Series)
    period : int, optional
        The lookback period for calculating channels (default: 20)

    Returns
    -------
    pandas.DataFrame
        DataFrame with columns:
        - Upper: Highest high over the period
        - Middle: Average of upper and lower channels
        - Lower: Lowest low over the period

    Examples
    --------
    >>> import pandas as pd
    >>> import numpy as np
    >>> from tradelab.indicators.donchian_channels import DONCHIAN_CHANNELS
    >>> 
    >>> # Sample OHLC data
    >>> high = pd.Series([12, 13, 14, 13, 15, 16, 15, 17, 16, 18])
    >>> low = pd.Series([10, 11, 12, 11, 13, 14, 13, 15, 14, 16])
    >>> 
    >>> # Calculate 20-period Donchian Channels
    >>> channels = DONCHIAN_CHANNELS(high, low, period=20)
    >>> print(channels)

    Notes
    -----
    - Upper channel = Highest high over the lookback period
    - Lower channel = Lowest low over the lookback period  
    - Middle channel = (Upper + Lower) / 2
    - Common periods: 10, 20, 55 days
    - Used for trend following and breakout strategies
    - This implementation uses Cython for optimized performance
    """
    # Validate input data
    if high is None or low is None:
        raise ValueError("High and low data cannot be None")

    # Convert to numpy arrays if needed
    if hasattr(high, 'values'):  # pandas Series
        high_array = high.values
    else:
        high_array = np.asarray(high)

    if hasattr(low, 'values'):  # pandas Series
        low_array = low.values
    else:
        low_array = np.asarray(low)

    if len(high_array) == 0 or len(low_array) == 0:
        raise ValueError("High and low arrays cannot be empty")

    if len(high_array) != len(low_array):
        raise ValueError("High and low arrays must have the same length")

    if not isinstance(period, int) or period <= 0:
        raise ValueError("Period must be a positive integer")

    return _DONCHIAN_CHANNELS_cython(high, low, period)
