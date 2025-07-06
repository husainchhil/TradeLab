"""ADX Python wrapper for preserving docstring visibility in IDEs."""

from .adx import ADX as _ADX_cython


def ADX(high, low, close, di_length=14, adx_smoothing=14):
    """
    Calculate the Average Directional Index (ADX) indicator using Cython for performance.

    The ADX is a trend strength indicator that ranges from 0 to 100. It's calculated from
    the smoothed averages of the differences between the Plus and Minus Directional Indicators.

    Parameters
    ----------
    high : array-like
        High prices (numpy array or pandas Series)
    low : array-like
        Low prices (numpy array or pandas Series)  
    close : array-like
        Close prices (numpy array or pandas Series)
    di_length : int, default 14
        Length for the Directional Indicators calculation
    adx_smoothing : int, default 14
        Smoothing period for ADX calculation

    Returns
    -------
    pandas.DataFrame
        DataFrame with columns:
        - Plus_DI: Plus Directional Indicator
        - Minus_DI: Minus Directional Indicator  
        - ADX: Average Directional Index

    Examples
    --------
    >>> import pandas as pd
    >>> import numpy as np
    >>> from tradelab.indicators.adx import ADX
    >>> 
    >>> # Sample data
    >>> high = pd.Series([10, 11, 12, 11, 10])
    >>> low = pd.Series([9, 10, 11, 10, 9])
    >>> close = pd.Series([9.5, 10.5, 11.5, 10.5, 9.5])
    >>> 
    >>> # Calculate ADX
    >>> result = ADX(high, low, close, di_length=14, adx_smoothing=14)
    >>> print(result)

    Notes
    -----
    - ADX values above 25 typically indicate a strong trend
    - ADX values below 20 indicate a weak trend or sideways movement
    - This implementation uses Cython for optimized performance
    """
    return _ADX_cython(high, low, close, di_length, adx_smoothing)
