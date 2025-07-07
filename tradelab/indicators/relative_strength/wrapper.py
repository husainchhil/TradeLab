"""RELATIVE_STRENGTH Python wrapper for preserving docstring visibility in IDEs."""

from .relative_strength import RELATIVE_STRENGTH as _RELATIVE_STRENGTH_cython


def RELATIVE_STRENGTH(base_data, comparative_data, length=55, base_shift=5, rs_ma_length=50, price_sma_length=50):
    """
    Calculate Relative Strength between two securities using Cython for performance.

    Relative Strength compares the performance of one security against another,
    helping to identify which security is outperforming or underperforming relative
    to the comparison security.

    Parameters
    ----------
    base_data : array-like
        Source data for the base security (numpy array or pandas Series)
    comparative_data : array-like
        Source data for the comparative security (numpy array or pandas Series)
    length : int, optional
        Period for calculating price ratios (default: 55)
    base_shift : int, optional
        Base shift period (default: 5)
    rs_ma_length : int, optional
        Moving average length for RS smoothing (default: 50)
    price_sma_length : int, optional
        Moving average length for price smoothing (default: 50)

    Returns
    -------
    pandas.Series
        Series with Relative Strength values where:
        - Positive values indicate base security outperforming comparative
        - Negative values indicate base security underperforming comparative
        - Values near zero indicate similar performance

    Examples
    --------
    >>> import pandas as pd
    >>> import numpy as np
    >>> from tradelab.indicators.relative_strength import RELATIVE_STRENGTH
    >>> 
    >>> # Sample data for two securities
    >>> stock_a = pd.Series([100, 102, 104, 103, 105, 107, 106])
    >>> stock_b = pd.Series([50, 51, 50.5, 52, 51.5, 53, 52])
    >>> 
    >>> # Calculate relative strength
    >>> rs = RELATIVE_STRENGTH(stock_a, stock_b, length=5)
    >>> print(rs)

    Notes
    -----
    - Relative Strength formula: (Base_t / Base_t-n) / (Comp_t / Comp_t-n) - 1
    - Where n is the length parameter
    - Positive RS indicates base security outperforming comparative
    - Negative RS indicates base security underperforming comparative
    - Common length periods: 20, 55, 252 (daily), 4, 12, 52 (weekly)
    - This implementation uses Cython for optimized performance
    - Requires overlapping time periods between both securities
    """
    if not isinstance(length, int) or length <= 0:
        raise ValueError("Length must be a positive integer")

    if not isinstance(base_shift, int) or base_shift < 0:
        raise ValueError("Base shift must be a non-negative integer")

    if not isinstance(rs_ma_length, int) or rs_ma_length <= 0:
        raise ValueError("RS MA length must be a positive integer")

    if not isinstance(price_sma_length, int) or price_sma_length <= 0:
        raise ValueError("Price SMA length must be a positive integer")

    return _RELATIVE_STRENGTH_cython(base_data, comparative_data, length, base_shift, rs_ma_length, price_sma_length)
