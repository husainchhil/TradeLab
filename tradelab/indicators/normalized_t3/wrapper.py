"""Normalized T3 Python wrapper for preserving docstring visibility in IDEs."""

from .normalized_t3 import NORMALIZED_T3 as _NORMALIZED_T3_cython
from ...utils import validate_series


def NORMALIZED_T3(src, period=200, t3_period=2, volume_factor=0.7):
    """
    Calculate the Normalized T3 Oscillator using Cython for performance.

    The Normalized T3 is a smoothed oscillator that combines the T3 moving average
    with min-max normalization to create a bounded oscillator between 0 and 1.

    Parameters
    ----------
    src : array-like
        Source prices (numpy array or pandas Series)
    period : int, default 200
        The period for min-max normalization
    t3_period : int, default 2
        The period for the T3 calculation
    volume_factor : float, default 0.7
        Volume factor (vfactor) for T3 smoothing (between 0 and 1)

    Returns
    -------
    pandas.Series
        Series with Normalized T3 Oscillator values (0 to 1), indexed same as input if pandas Series

    Examples
    --------
    >>> import pandas as pd
    >>> import numpy as np
    >>> from tradelab.indicators.normalized_t3 import NORMALIZED_T3
    >>> 
    >>> # Sample data
    >>> prices = pd.Series([10, 11, 12, 11, 10, 9, 8, 9, 10, 11] * 25)  # 250 points
    >>> 
    >>> # Calculate Normalized T3
    >>> nt3 = NORMALIZED_T3(prices, period=200, t3_period=2, volume_factor=0.7)
    >>> print(nt3)

    Notes
    -----
    - Values range from 0 to 1 due to normalization
    - Higher volume_factor values create smoother results
    - T3 provides multiple stages of exponential smoothing
    - This implementation uses Cython for optimized performance
    """
    validate_series(src, "Source")
    if not isinstance(period, int) or period <= 0:
        raise ValueError("Period must be a positive integer")
    if not isinstance(t3_period, int) or t3_period <= 0:
        raise ValueError("T3 period must be a positive integer")
    if not isinstance(volume_factor, (int, float)) or not (0 < volume_factor < 1):
        raise ValueError("Volume factor must be a float between 0 and 1")

    return _NORMALIZED_T3_cython(src, period, t3_period, volume_factor)
