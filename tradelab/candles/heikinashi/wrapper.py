"""HEIKINASHI Python wrapper for preserving docstring visibility in IDEs."""

import pandas as pd
from .heikinashi import HEIKINASHI as _HEIKINASHI_cython


def HEIKINASHI(data, offset: int = 0, **kwargs) -> pd.DataFrame:
    """
    Calculate Heikin-Ashi candles using Cython for performance.

    Heikin-Ashi is a type of candlestick chart that uses modified formulas to create 
    a smoother appearance and filter out market noise, making trend identification easier.

    Parameters
    ----------
    data : pd.DataFrame
        DataFrame containing OHLCV data with columns 'open', 'high', 'low', 'close'.
    offset : int, optional
        Number of periods to shift the result (default: 0).
    **kwargs : dict, optional
        Additional parameters:
        - fillna: Value to fill NaN values with
        - fill_method: Method to fill NaN values ('ffill', 'bfill', etc.)

    Returns
    -------
    pd.DataFrame
        DataFrame with Heikin-Ashi candles containing columns:
        - Open: Heikin-Ashi opening price
        - High: Heikin-Ashi high price  
        - Low: Heikin-Ashi low price
        - Close: Heikin-Ashi closing price
        - Trend: Direction of the candle (1 for up, -1 for down)

    Examples
    --------
    >>> import pandas as pd
    >>> from tradelab.candles import HEIKINASHI
    >>> 
    >>> # Sample OHLC data
    >>> data = pd.DataFrame({
    ...     'open': [100, 101, 102, 103, 104],
    ...     'high': [105, 106, 107, 108, 109],
    ...     'low': [99, 100, 101, 102, 103],
    ...     'close': [102, 103, 104, 105, 106]
    ... })
    >>> 
    >>> # Calculate Heikin-Ashi candles
    >>> ha_data = HEIKINASHI(data)
    >>> print(ha_data)

    Notes
    -----
    - Heikin-Ashi formulas:
      * HA_Close = (Open + High + Low + Close) / 4
      * HA_Open = (Previous HA_Open + Previous HA_Close) / 2
      * HA_High = Max(High, HA_Open, HA_Close)
      * HA_Low = Min(Low, HA_Open, HA_Close)
    - This implementation uses Cython for optimized performance
    - Heikin-Ashi candles help identify trend direction and strength
    - Green candles (Close > Open) indicate uptrend
    - Red candles (Close < Open) indicate downtrend
    """
    return _HEIKINASHI_cython(data, offset, **kwargs)
