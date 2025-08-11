"""Donchian Channels calculation using Cython."""

import numpy as np
import pandas as pd
cimport numpy as cnp
cimport cython

@cython.boundscheck(False)
@cython.wraparound(False)
def DONCHIAN_CHANNELS(high, low, int period):
    """
    Calculate Donchian Channels using Cython for performance.
    
    Parameters
    ----------
    high : array-like
        High prices (numpy array or pandas Series)
    low : array-like
        Low prices (numpy array or pandas Series)
    period : int
        The lookback period for calculating channels
        
    Returns
    -------
    pandas.DataFrame
        DataFrame with Upper, Middle, and Lower channel values
    """
    # Handle pandas Series input
    if isinstance(high, pd.Series):
        high_values = high.values
        low_values = low.values
        index = high.index
    else:
        high_values = np.asarray(high)
        low_values = np.asarray(low)
        index = None
    
    cdef cnp.ndarray[cnp.float64_t, ndim=1] high_data = high_values.astype(np.float64)
    cdef cnp.ndarray[cnp.float64_t, ndim=1] low_data = low_values.astype(np.float64)
    cdef int length = len(high_data)
    cdef cnp.ndarray[cnp.float64_t, ndim=1] upper_channel = np.empty(length, dtype=np.float64)
    cdef cnp.ndarray[cnp.float64_t, ndim=1] lower_channel = np.empty(length, dtype=np.float64)
    cdef cnp.ndarray[cnp.float64_t, ndim=1] middle_channel = np.empty(length, dtype=np.float64)
    
    cdef int i, start_idx
    cdef double max_high, min_low
    
    # Calculate Donchian Channels
    for i in range(length):
        start_idx = max(0, i - period + 1)
        
        # Find maximum high in the period
        max_high = high_data[start_idx]
        for j in range(start_idx + 1, i + 1):
            if high_data[j] > max_high:
                max_high = high_data[j]
        
        # Find minimum low in the period
        min_low = low_data[start_idx]
        for j in range(start_idx + 1, i + 1):
            if low_data[j] < min_low:
                min_low = low_data[j]
        
        upper_channel[i] = max_high
        lower_channel[i] = min_low
        middle_channel[i] = (max_high + min_low) / 2.0
    
    # Create result DataFrame
    if index is not None:
        result = pd.DataFrame({
            'Upper': upper_channel,
            'Middle': middle_channel,
            'Lower': lower_channel
        }, index=index)
    else:
        result = pd.DataFrame({
            'Upper': upper_channel,
            'Middle': middle_channel,
            'Lower': lower_channel
        })
    
    return result