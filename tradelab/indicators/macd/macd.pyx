"""MACD (Moving Average Convergence Divergence) indicator calculation."""

import numpy as np
import pandas as pd
cimport numpy as cnp
cimport cython

@cython.boundscheck(False)
@cython.wraparound(False)
def MACD(src, int fast_period=12, int slow_period=26, int signal_period=9):
    """
    Calculate MACD (Moving Average Convergence Divergence) using Cython for performance.
    
    Parameters:
    -----------
    src : pd.Series or array-like
        Source price series (typically close prices)
    fast_period : int, default 12
        Period for fast EMA
    slow_period : int, default 26
        Period for slow EMA  
    signal_period : int, default 9
        Period for signal line EMA
        
    Returns:
    --------
    pd.DataFrame
        DataFrame with columns ['MACD', 'Signal', 'Histogram']
    """
    if isinstance(src, pd.Series):
        values = src.values
        index = src.index
    else:
        values = np.asarray(src)
        index = None
    
    if fast_period >= slow_period:
        raise ValueError("fast_period must be less than slow_period")
    
    cdef cnp.ndarray[cnp.float64_t, ndim=1] data = values.astype(np.float64)
    cdef int length = len(data)
    
    # EMA calculation arrays
    cdef cnp.ndarray[cnp.float64_t, ndim=1] fast_ema = np.zeros(length, dtype=np.float64)
    cdef cnp.ndarray[cnp.float64_t, ndim=1] slow_ema = np.zeros(length, dtype=np.float64)
    cdef cnp.ndarray[cnp.float64_t, ndim=1] macd_line = np.zeros(length, dtype=np.float64)
    cdef cnp.ndarray[cnp.float64_t, ndim=1] signal_line = np.zeros(length, dtype=np.float64)
    cdef cnp.ndarray[cnp.float64_t, ndim=1] histogram = np.zeros(length, dtype=np.float64)
    
    # Calculate smoothing factors
    cdef double fast_alpha = 2.0 / (fast_period + 1)
    cdef double slow_alpha = 2.0 / (slow_period + 1)
    cdef double signal_alpha = 2.0 / (signal_period + 1)
    
    cdef int i
    
    # Initialize first values
    fast_ema[0] = slow_ema[0] = data[0]
    
    # Calculate Fast and Slow EMAs
    for i in range(1, length):
        fast_ema[i] = fast_alpha * data[i] + (1 - fast_alpha) * fast_ema[i-1]
        slow_ema[i] = slow_alpha * data[i] + (1 - slow_alpha) * slow_ema[i-1]
    
    # Calculate MACD line (Fast EMA - Slow EMA)
    for i in range(length):
        macd_line[i] = fast_ema[i] - slow_ema[i]
    
    # Initialize signal line with first MACD value
    signal_line[0] = macd_line[0]
    
    # Calculate Signal line (EMA of MACD)
    for i in range(1, length):
        signal_line[i] = signal_alpha * macd_line[i] + (1 - signal_alpha) * signal_line[i-1]
    
    # Calculate Histogram (MACD - Signal)
    for i in range(length):
        histogram[i] = macd_line[i] - signal_line[i]
    
    # Create result DataFrame
    result = pd.DataFrame({
        'MACD': macd_line,
        'Signal': signal_line,
        'Histogram': histogram
    }, index=index)
    
    return result