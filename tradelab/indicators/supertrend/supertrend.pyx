"""SuperTrend indicator calculation using Cython."""

import numpy as np
import pandas as pd
cimport numpy as cnp
cimport cython
from ..volatility import ATR

ctypedef cnp.float64_t DTYPE_t

@cython.boundscheck(False)
@cython.wraparound(False)
def SUPERTREND(high, low, close, int period = 10, double multiplier = 3.0):
    """
    Calculate the SuperTrend indicator using Cython for performance.
    
    Parameters
    ----------
    high : array-like
        High prices (numpy array or pandas Series)
    low : array-like
        Low prices (numpy array or pandas Series)  
    close : array-like
        Close prices (numpy array or pandas Series)
    period : int
        The period for ATR calculation (default: 10)
    multiplier : float
        The multiplier for ATR to calculate SuperTrend (default: 3.0)
        
    Returns
    -------
    pandas.DataFrame
        DataFrame with SuperTrend values and direction
    """
    # Handle pandas Series input
    if isinstance(high, pd.Series):
        high_values = high.values
        low_values = low.values
        close_values = close.values
        index = high.index
    else:
        high_values = np.asarray(high)
        low_values = np.asarray(low)
        close_values = np.asarray(close)
        index = None
    
    # Calculate ATR
    atr_values = ATR(high, low, close, period=period)
    
    cdef cnp.ndarray[DTYPE_t, ndim=1] high_data = high_values.astype(np.float64)
    cdef cnp.ndarray[DTYPE_t, ndim=1] low_data = low_values.astype(np.float64)
    cdef cnp.ndarray[DTYPE_t, ndim=1] close_data = close_values.astype(np.float64)
    cdef cnp.ndarray[DTYPE_t, ndim=1] atr_data = atr_values.values.astype(np.float64)
    
    cdef int length = len(close_data)
    cdef cnp.ndarray[DTYPE_t, ndim=1] hl2 = np.empty(length, dtype=np.float64)
    cdef cnp.ndarray[DTYPE_t, ndim=1] upperband = np.empty(length, dtype=np.float64)
    cdef cnp.ndarray[DTYPE_t, ndim=1] lowerband = np.empty(length, dtype=np.float64)
    cdef cnp.ndarray[DTYPE_t, ndim=1] supertrend = np.empty(length, dtype=np.float64)
    cdef cnp.ndarray[cnp.int64_t, ndim=1] direction = np.empty(length, dtype=np.int64)
    
    cdef int i
    
    # Calculate HL2 (median price)
    for i in range(length):
        hl2[i] = (high_data[i] + low_data[i]) / 2.0
    
    # Calculate upper and lower bands
    for i in range(length):
        upperband[i] = hl2[i] + (multiplier * atr_data[i])
        lowerband[i] = hl2[i] - (multiplier * atr_data[i])
    
    # Set initial values
    supertrend[0] = lowerband[0]  # Start with lowerband
    direction[0] = 1  # Start with uptrend
    
    # Calculate SuperTrend
    for i in range(1, length):
        # Determine trend direction based on previous close vs previous supertrend
        if close_data[i] <= supertrend[i-1]:
            direction[i] = -1  # Downtrend
        else:
            direction[i] = 1   # Uptrend
        
        # Calculate supertrend value based on direction
        if direction[i] == 1:  # Uptrend
            supertrend[i] = lowerband[i]
            if direction[i-1] == 1:  # Was also uptrend
                supertrend[i] = lowerband[i] if lowerband[i] > supertrend[i-1] else supertrend[i-1]
        else:  # Downtrend
            supertrend[i] = upperband[i]
            if direction[i-1] == -1:  # Was also downtrend
                supertrend[i] = upperband[i] if upperband[i] < supertrend[i-1] else supertrend[i-1]
    
    # Create result DataFrame
    if index is not None:
        result = pd.DataFrame({
            'Supertrend': supertrend,
            'Direction': direction
        }, index=index)
    else:
        result = pd.DataFrame({
            'Supertrend': supertrend,
            'Direction': direction
        })
    
    return result