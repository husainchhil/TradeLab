"""Stochastic Oscillator calculation using Cython."""

import numpy as np
import pandas as pd
cimport numpy as cnp
cimport cython

ctypedef cnp.float64_t DTYPE_t

@cython.boundscheck(False)
@cython.wraparound(False)
def STOCHASTIC(high, low, close, int k_period=14, int d_period=3):
    """
    Calculate Stochastic Oscillator (%K and %D) using Cython for performance.
    
    The Stochastic Oscillator is a momentum indicator that shows the location
    of the close relative to the high-low range over a set number of periods.
    
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
        - %K: Fast stochastic indicator
        - %D: Slow stochastic indicator (SMA of %K)
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
    
    cdef cnp.ndarray[DTYPE_t, ndim=1] high_data = high_values.astype(np.float64)
    cdef cnp.ndarray[DTYPE_t, ndim=1] low_data = low_values.astype(np.float64)
    cdef cnp.ndarray[DTYPE_t, ndim=1] close_data = close_values.astype(np.float64)
    cdef int length = len(high_data)
    
    cdef cnp.ndarray[DTYPE_t, ndim=1] k_values = np.empty(length, dtype=np.float64)
    cdef cnp.ndarray[DTYPE_t, ndim=1] d_values = np.empty(length, dtype=np.float64)
    
    cdef int i, j, start_idx
    cdef double highest_high, lowest_low, close_val
    cdef double k_sum
    
    # Calculate %K values
    for i in range(length):
        if i < k_period - 1:
            # Not enough data yet
            k_values[i] = np.nan
        else:
            # Find highest high and lowest low over k_period
            start_idx = i - k_period + 1
            highest_high = high_data[start_idx]
            lowest_low = low_data[start_idx]
            
            for j in range(start_idx + 1, i + 1):
                if high_data[j] > highest_high:
                    highest_high = high_data[j]
                if low_data[j] < lowest_low:
                    lowest_low = low_data[j]
            
            # Calculate %K
            close_val = close_data[i]
            if highest_high == lowest_low:
                # Avoid division by zero
                k_values[i] = 50.0
            else:
                k_values[i] = ((close_val - lowest_low) / (highest_high - lowest_low)) * 100.0
    
    # Calculate %D values (Simple Moving Average of %K)
    for i in range(length):
        if i < k_period + d_period - 2:
            # Not enough data yet for %D
            d_values[i] = np.nan
        else:
            # Calculate SMA of %K over d_period
            start_idx = i - d_period + 1
            k_sum = 0.0
            
            for j in range(start_idx, i + 1):
                k_sum += k_values[j]
            
            d_values[i] = k_sum / d_period
    
    # Create result DataFrame
    result = pd.DataFrame({
        '%K': k_values,
        '%D': d_values
    }, index=index)
    
    return result
