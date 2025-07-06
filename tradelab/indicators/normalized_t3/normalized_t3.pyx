"""Normalized T3 Oscillator indicator calculation."""

import numpy as np
import pandas as pd
cimport numpy as cnp
cimport cython

@cython.boundscheck(False)
@cython.wraparound(False)
def NORMALIZED_T3(src, int period=200, int t3_period=2, double volume_factor=0.7):
    if isinstance(src, pd.Series):
        values = src.values
        index = src.index
    else:
        values = np.asarray(src)
        index = None
    
    if not (0 < volume_factor <= 1):
        raise ValueError("Volume factor must be between 0 and 1")
    
    cdef cnp.ndarray[cnp.float64_t, ndim=1] data = values.astype(np.float64)
    cdef int length = len(data)
    
    # T3 calculation arrays
    cdef cnp.ndarray[cnp.float64_t, ndim=1] ema1 = np.zeros(length, dtype=np.float64)
    cdef cnp.ndarray[cnp.float64_t, ndim=1] ema2 = np.zeros(length, dtype=np.float64)
    cdef cnp.ndarray[cnp.float64_t, ndim=1] ema3 = np.zeros(length, dtype=np.float64)
    cdef cnp.ndarray[cnp.float64_t, ndim=1] ema4 = np.zeros(length, dtype=np.float64)
    cdef cnp.ndarray[cnp.float64_t, ndim=1] ema5 = np.zeros(length, dtype=np.float64)
    cdef cnp.ndarray[cnp.float64_t, ndim=1] ema6 = np.zeros(length, dtype=np.float64)
    cdef cnp.ndarray[cnp.float64_t, ndim=1] t3_values = np.zeros(length, dtype=np.float64)
    
    # Calculate smoothing factor
    cdef double alpha = 2.0 / (t3_period + 1)
    
    # T3 coefficients
    cdef double c1 = -volume_factor * volume_factor * volume_factor
    cdef double c2 = 3 * volume_factor * volume_factor + 3 * volume_factor * volume_factor * volume_factor
    cdef double c3 = -6 * volume_factor * volume_factor - 3 * volume_factor - 3 * volume_factor * volume_factor * volume_factor
    cdef double c4 = 1 + 3 * volume_factor + volume_factor * volume_factor * volume_factor + 3 * volume_factor * volume_factor
    
    cdef int i
    
    # Initialize first values
    ema1[0] = ema2[0] = ema3[0] = ema4[0] = ema5[0] = ema6[0] = data[0]
    
    # Calculate EMAs
    for i in range(1, length):
        ema1[i] = alpha * data[i] + (1 - alpha) * ema1[i-1]
        ema2[i] = alpha * ema1[i] + (1 - alpha) * ema2[i-1]
        ema3[i] = alpha * ema2[i] + (1 - alpha) * ema3[i-1]
        ema4[i] = alpha * ema3[i] + (1 - alpha) * ema4[i-1]
        ema5[i] = alpha * ema4[i] + (1 - alpha) * ema5[i-1]
        ema6[i] = alpha * ema5[i] + (1 - alpha) * ema6[i-1]
    
    # Calculate T3
    for i in range(length):
        t3_values[i] = c1 * ema6[i] + c2 * ema5[i] + c3 * ema4[i] + c4 * ema3[i]
    
    # Calculate rolling min and max for normalization
    cdef cnp.ndarray[cnp.float64_t, ndim=1] min_vals = np.full(length, np.nan, dtype=np.float64)
    cdef cnp.ndarray[cnp.float64_t, ndim=1] max_vals = np.full(length, np.nan, dtype=np.float64)
    cdef int start_idx, j
    cdef double min_val, max_val
    
    for i in range(period - 1, length):
        start_idx = max(0, i - period + 1)
        min_val = t3_values[start_idx]
        max_val = t3_values[start_idx]
        
        for j in range(start_idx, i + 1):
            if t3_values[j] < min_val:
                min_val = t3_values[j]
            if t3_values[j] > max_val:
                max_val = t3_values[j]
        
        min_vals[i] = min_val
        max_vals[i] = max_val
    
    # Normalize T3 values
    cdef cnp.ndarray[cnp.float64_t, ndim=1] normalized_t3 = np.zeros(length, dtype=np.float64)
    cdef double range_val
    
    for i in range(length):
        if not np.isnan(min_vals[i]) and not np.isnan(max_vals[i]):
            range_val = max_vals[i] - min_vals[i]
            if range_val == 0:
                range_val = 1
            normalized_t3[i] = (t3_values[i] - min_vals[i]) / range_val - 0.5
        else:
            normalized_t3[i] = np.nan
    
    # Return as pandas Series
    if index is not None:
        return pd.Series(normalized_t3, index=index, name='Normalized T3 Oscillator')
    else:
        return pd.Series(normalized_t3, name='Normalized T3 Oscillator')
