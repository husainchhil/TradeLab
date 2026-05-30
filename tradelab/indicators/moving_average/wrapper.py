"""Moving Average (SMA/EMA) Python wrapper for preserving docstring visibility in IDEs."""

from typing import Literal

from .moving_average import MOVING_AVERAGE as _MOVING_AVERAGE_cython
from ...utils.validate_data import validate_series


def MOVING_AVERAGE(src, period=14, ma_type: Literal["SMA", "EMA"] = "SMA"):
    """
    Calculate Moving Average (SMA or EMA) using Cython for performance.

    This function supports both Simple Moving Average (SMA) and
    Exponential Moving Average (EMA), selected by the `ma_type` argument.

    Parameters
    ----------
    src : array-like
        Source prices (numpy array or pandas Series)
    period : int, optional
        The period for moving average calculation (default: 14)
    ma_type : str, optional
        Moving average type: "SMA" or "EMA" (default: "SMA")

    Returns
    -------
    pandas.Series
        Series with moving average values, indexed same as input if pandas Series

    Examples
    --------
    >>> import pandas as pd
    >>> from tradelab.indicators.moving_average import MOVING_AVERAGE
    >>>
    >>> prices = pd.Series([10, 11, 12, 11, 10, 9, 8, 9, 10, 11])
    >>>
    >>> sma_values = MOVING_AVERAGE(prices, period=5, ma_type="SMA")
    >>> ema_values = MOVING_AVERAGE(prices, period=5, ma_type="EMA")
    >>> print(sma_values)
    >>> print(ema_values)

    Notes
    -----
    - SMA gives equal weight to all points in the window
    - EMA gives more weight to recent prices (alpha = 2/(period + 1))
    - This implementation uses Cython for optimized performance
    """
    validate_series(src, "Source")
    if not isinstance(period, int) or period <= 0:
        raise ValueError("Period must be a positive integer")
    if not isinstance(ma_type, str):
        raise TypeError("ma_type must be a string")

    ma_type_upper = ma_type.upper()
    if ma_type_upper not in ("SMA", "EMA"):
        raise ValueError("ma_type must be either 'SMA' or 'EMA'")

    ma_flag = 1 if ma_type_upper == "EMA" else 0
    return _MOVING_AVERAGE_cython(src, period, ma_flag)
