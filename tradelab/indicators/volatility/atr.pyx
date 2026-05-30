"""Average True Range (ATR) calculation using Cython."""

import numpy as np
import pandas as pd
cimport numpy as cnp
cimport cython

@cython.boundscheck(False)
@cython.wraparound(False)
def ATR(high, low, close, int period, int smoothing):
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
    smoothing : int
        Smoothing type: 0=RMA, 1=SMA, 2=EMA, 3=WMA
        
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
    cdef double alpha
    cdef int i
    cdef int j
    cdef double tr1, tr2, tr3
    cdef double window_sum
    cdef double weighted_sum
    cdef double weight_sum
    
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
    
    if smoothing == 1:
        # SMA of True Range
        window_sum = 0.0
        for i in range(length):
            window_sum += true_range[i]
            if i >= period:
                window_sum -= true_range[i - period]
                atr[i] = window_sum / period
            else:
                atr[i] = window_sum / (i + 1)
    elif smoothing == 2:
        # EMA of True Range
        alpha = 2.0 / (period + 1)
        atr[0] = true_range[0]
        for i in range(1, length):
            atr[i] = alpha * true_range[i] + (1 - alpha) * atr[i - 1]
    elif smoothing == 3:
        # WMA of True Range
        weighted_sum = 0.0
        weight_sum = 0.0
        for i in range(length):
            if i < period:
                # Expanding window with weights 1..i+1
                weight_sum += (i + 1)
                weighted_sum = 0.0
                for j in range(i + 1):
                    weighted_sum += (j + 1) * true_range[i - j]
                atr[i] = weighted_sum / weight_sum
            else:
                weight_sum = period * (period + 1) / 2.0
                weighted_sum = 0.0
                for j in range(period):
                    weighted_sum += (j + 1) * true_range[i - j]
                atr[i] = weighted_sum / weight_sum
    else:
        # RMA (Rolling Moving Average) - equivalent to EMA with alpha = 1/period
        alpha = 1.0 / period
        atr[0] = true_range[0]
        for i in range(1, length):
            atr[i] = alpha * true_range[i] + (1 - alpha) * atr[i - 1]
    
    # Return as pandas Series
    if index is not None:
        return pd.Series(atr, index=index, name="ATR")
    else:
        return pd.Series(atr, name="ATR")
