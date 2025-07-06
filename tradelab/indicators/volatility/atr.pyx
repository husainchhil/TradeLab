"""Average True Range (ATR) calculation using Cython."""

import numpy as np
import pandas as pd
cimport numpy as cnp
cimport cython

@cython.boundscheck(False)
@cython.wraparound(False)
def ATR(high, low, close, int period):
    """
    Calculate Average True Range (ATR) using Cython for performance.
    
    Parameters
    ----------
    high : array-like
        High prices (numpy array or pandas Series)
    low : array-like
        Low prices (numpy array or pandas Series)
    close : array-like
        Close prices (numpy array or pandas Series)
    period : int
        The period for ATR calculation
        
    Returns
    -------
    pandas.Series
        Series with ATR values, indexed same as input if pandas Series
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
    
    cdef cnp.ndarray[cnp.float64_t, ndim=1] high_data = high_values.astype(np.float64)
    cdef cnp.ndarray[cnp.float64_t, ndim=1] low_data = low_values.astype(np.float64)
    cdef cnp.ndarray[cnp.float64_t, ndim=1] close_data = close_values.astype(np.float64)
    cdef int length = len(high_data)
    cdef cnp.ndarray[cnp.float64_t, ndim=1] true_range = np.empty(length, dtype=np.float64)
    cdef cnp.ndarray[cnp.float64_t, ndim=1] atr = np.empty(length, dtype=np.float64)
    cdef double alpha = 1.0 / period
    cdef int i
    cdef double tr1, tr2, tr3
    
    # Calculate True Range
    true_range[0] = high_data[0] - low_data[0]  # First value (no previous close)
    
    for i in range(1, length):
        tr1 = high_data[i] - low_data[i]
        tr2 = abs(high_data[i] - close_data[i-1])
        tr3 = abs(low_data[i] - close_data[i-1])
        
        if tr1 >= tr2 and tr1 >= tr3:
            true_range[i] = tr1
        elif tr2 >= tr1 and tr2 >= tr3:
            true_range[i] = tr2
        else:
            true_range[i] = tr3
    
    # Calculate ATR using RMA (Rolling Moving Average) - equivalent to EMA with alpha = 1/period
    atr[0] = true_range[0]
    
    for i in range(1, length):
        atr[i] = alpha * true_range[i] + (1 - alpha) * atr[i-1]
    
    # Return as pandas Series
    if index is not None:
        return pd.Series(atr, index=index, name="ATR")
    else:
        return pd.Series(atr, name="ATR")
