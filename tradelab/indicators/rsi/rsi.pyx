"""Relative Strength Index (RSI) calculation using Cython."""

import numpy as np
import pandas as pd
cimport numpy as cnp
cimport cython

ctypedef cnp.float64_t DTYPE_t

@cython.boundscheck(False)
@cython.wraparound(False)
def RSI(src, int period = 14):
    """
    Calculate the Relative Strength Index (RSI) using Cython for performance.
    
    Parameters
    ----------
    src : array-like
        Source prices (numpy array or pandas Series)
    period : int
        RSI period (default: 14)
        
    Returns
    -------
    pandas.Series
        Series with RSI values (0-100), indexed same as input if pandas Series
    """
    # Handle pandas Series input
    if isinstance(src, pd.Series):
        src_values = src.values
        index = src.index
    else:
        src_values = np.asarray(src)
        index = None
    
    cdef cnp.ndarray[DTYPE_t, ndim=1] src_data = src_values.astype(np.float64)
    cdef int length = len(src_data)
    cdef cnp.ndarray[DTYPE_t, ndim=1] change = np.empty(length, dtype=np.float64)
    cdef cnp.ndarray[DTYPE_t, ndim=1] gains = np.empty(length, dtype=np.float64)
    cdef cnp.ndarray[DTYPE_t, ndim=1] losses = np.empty(length, dtype=np.float64)
    cdef cnp.ndarray[DTYPE_t, ndim=1] avg_gains = np.empty(length, dtype=np.float64)
    cdef cnp.ndarray[DTYPE_t, ndim=1] avg_losses = np.empty(length, dtype=np.float64)
    cdef cnp.ndarray[DTYPE_t, ndim=1] rsi = np.empty(length, dtype=np.float64)
    
    cdef double alpha = 1.0 / period
    cdef double rs
    cdef int i
    
    # Calculate price changes
    change[0] = 0.0  # First change is 0
    for i in range(1, length):
        change[i] = src_data[i] - src_data[i-1]
    
    # Separate gains and losses
    for i in range(length):
        gains[i] = change[i] if change[i] > 0 else 0.0
        losses[i] = -change[i] if change[i] < 0 else 0.0
    
    # Calculate exponential weighted moving averages (equivalent to EMA with alpha = 1/period)
    avg_gains[0] = gains[0]
    avg_losses[0] = losses[0]
    
    for i in range(1, length):
        avg_gains[i] = alpha * gains[i] + (1 - alpha) * avg_gains[i-1]
        avg_losses[i] = alpha * losses[i] + (1 - alpha) * avg_losses[i-1]
    
    # Calculate RSI
    for i in range(length):
        if avg_losses[i] == 0:
            rsi[i] = 100.0
        else:
            rs = avg_gains[i] / avg_losses[i]
            rsi[i] = 100.0 - (100.0 / (1.0 + rs))
        
        # Handle edge cases
        if rsi[i] != rsi[i]:  # Check for NaN
            rsi[i] = 50.0
    
    # Return as pandas Series
    if index is not None:
        return pd.Series(rsi, index=index, name="RSI")
    else:
        return pd.Series(rsi, name="RSI")