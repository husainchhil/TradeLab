"""RENKO Python wrapper for preserving docstring visibility in IDEs."""

import pandas as pd
from .renko import RENKO as _RENKO_cython


def RENKO(data, brick_size: float, mode: str = "wicks") -> pd.DataFrame:
    """
    Calculate Renko bricks using Cython for performance.

    Renko charts are a type of chart that only shows price movement above a certain threshold,
    filtering out minor price movements and focusing on significant price changes.

    Parameters
    ----------
    data : pd.DataFrame
        DataFrame containing OHLCV data with columns 'open', 'high', 'low', 'close', 'volume'.
    brick_size : float
        Size of each brick in price units.
    mode : str, optional
        Renko calculation mode (default: "wicks"). Options:
        - 'normal': Standard Renko calculation
        - 'wicks': Include wicks in calculation
        - 'nongap': No gap between bricks
        - 'reverse-wicks': Reverse wick calculation
        - 'reverse-nongap': Reverse no-gap calculation
        - 'fake-r-wicks': Fake reverse with wicks
        - 'fake-r-nongap': Fake reverse no-gap

    Returns
    -------
    pd.DataFrame
        DataFrame with Renko bricks containing columns:
        - Open: Opening price of the brick
        - High: High price of the brick
        - Low: Low price of the brick
        - Close: Closing price of the brick
        - Volume: Volume for the brick
        - Trend: Direction of the brick (1 for up, -1 for down)

    Examples
    --------
    >>> import pandas as pd
    >>> from tradelab.candles import RENKO
    >>> 
    >>> # Sample OHLCV data
    >>> data = pd.DataFrame({
    ...     'open': [100, 101, 102, 103, 104],
    ...     'high': [101, 102, 103, 104, 105],
    ...     'low': [99, 100, 101, 102, 103],
    ...     'close': [100.5, 101.5, 102.5, 103.5, 104.5],
    ...     'volume': [1000, 1100, 1200, 1300, 1400]
    ... })
    >>> 
    >>> # Calculate Renko bricks
    >>> renko_data = RENKO(data, brick_size=1.0, mode='wicks')
    >>> print(renko_data)

    Notes
    -----
    - Renko charts ignore time and focus only on price movement
    - Each brick represents a fixed price movement (brick_size)
    - This implementation uses Cython for optimized performance
    - The trend column indicates the direction of each brick
    - Different modes provide various ways to handle wicks and gaps
    """
    return _RENKO_cython(data, brick_size, mode)
