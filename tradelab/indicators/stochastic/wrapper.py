"""Stochastic Oscillator Python wrapper for preserving docstring visibility in IDEs."""

from ...utils.validate_data import validate_series

try:
    from .stochastic import STOCHASTIC as _STOCHASTIC_cython
except ImportError:
    # Fallback for development (before Cython compilation)
    def _STOCHASTIC_cython(high, low, close, k_period=14, d_period=3):
        raise ImportError("Cython module not compiled. Please run 'pip install -e .' first.")


def STOCHASTIC(high, low, close, k_period=14, d_period=3):
    """
    Calculate Stochastic Oscillator (%K and %D) indicator.
    
    The Stochastic Oscillator is a momentum indicator that shows the location
    of the close relative to the high-low range over a set number of periods.
    It is useful for identifying overbought and oversold conditions.
    
    Parameters
    ----------
    high : array-like
        High prices (numpy array or pandas Series)
    low : array-like
        Low prices (numpy array or pandas Series)
    close : array-like
        Close prices (numpy array or pandas Series)
    k_period : int, optional
        The lookback period for %K calculation (default: 14)
    d_period : int, optional
        The period for %D smoothing (SMA of %K) (default: 3)
        
    Returns
    -------
    pandas.DataFrame
        DataFrame with columns ['%K', '%D']
        - %K: Fast stochastic indicator (0-100)
        - %D: Slow stochastic indicator (0-100), SMA of %K
        
    Raises
    -------
    ValueError
        If k_period or d_period is less than 1
        If data contains null or infinite values
        If input arrays have different lengths
    
    Notes
    -----
    - %K = ((Close - Lowest Low) / (Highest High - Lowest Low)) × 100
    - %D = Simple Moving Average of %K
    - Values range from 0 to 100
    - Readings above 80 indicate overbought conditions
    - Readings below 20 indicate oversold conditions
    - Crossovers between %K and %D can signal trend changes
    
    Examples
    --------
    >>> # Basic Stochastic calculation
    >>> stoch = STOCHASTIC(data['High'], data['Low'], data['Close'])
    >>> print(stoch.columns)
    Index(['%K', '%D'], dtype='object')
    
    >>> # Custom parameters
    >>> stoch_custom = STOCHASTIC(data['High'], data['Low'], data['Close'], 
    ...                           k_period=21, d_period=5)
    
    >>> # Check for overbought/oversold conditions
    >>> overbought = stoch['%K'] > 80
    >>> oversold = stoch['%K'] < 20
    """
    # Validate input data using utils validation
    high = validate_series(high, "High")
    low = validate_series(low, "Low")
    close = validate_series(close, "Close")
    
    # Check that all series have the same length
    if len(high) != len(low) or len(high) != len(close):
        raise ValueError("High, low, and close arrays must have the same length")
    
    # Validate parameters
    if not isinstance(k_period, int) or k_period <= 0:
        raise ValueError("k_period must be a positive integer")
    
    if not isinstance(d_period, int) or d_period <= 0:
        raise ValueError("d_period must be a positive integer")
    
    if len(high) < k_period:
        raise ValueError(f"Insufficient data: need at least {k_period} periods, got {len(high)}")
    
    return _STOCHASTIC_cython(high, low, close, k_period, d_period)
