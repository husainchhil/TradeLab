"""Average Directional Index (ADX) indicator calculation."""

import numpy as np
import pandas as pd
cimport numpy as cnp
cimport cython

@cython.boundscheck(False)
@cython.wraparound(False)
def ADX(high, low, close, int di_length=14, int adx_smoothing=14):
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
    
    # Arrays for calculations
    cdef cnp.ndarray[cnp.float64_t, ndim=1] up = np.zeros(length, dtype=np.float64)
    cdef cnp.ndarray[cnp.float64_t, ndim=1] down = np.zeros(length, dtype=np.float64)
    cdef cnp.ndarray[cnp.float64_t, ndim=1] plus_dm = np.zeros(length, dtype=np.float64)
    cdef cnp.ndarray[cnp.float64_t, ndim=1] minus_dm = np.zeros(length, dtype=np.float64)
    cdef cnp.ndarray[cnp.float64_t, ndim=1] tr = np.zeros(length, dtype=np.float64)
    
    # Result arrays
    cdef cnp.ndarray[cnp.float64_t, ndim=1] tr_rma = np.zeros(length, dtype=np.float64)
    cdef cnp.ndarray[cnp.float64_t, ndim=1] plus_dm_rma = np.zeros(length, dtype=np.float64)
    cdef cnp.ndarray[cnp.float64_t, ndim=1] minus_dm_rma = np.zeros(length, dtype=np.float64)
    cdef cnp.ndarray[cnp.float64_t, ndim=1] plus_di = np.zeros(length, dtype=np.float64)
    cdef cnp.ndarray[cnp.float64_t, ndim=1] minus_di = np.zeros(length, dtype=np.float64)
    cdef cnp.ndarray[cnp.float64_t, ndim=1] dx = np.zeros(length, dtype=np.float64)
    cdef cnp.ndarray[cnp.float64_t, ndim=1] adx_values = np.zeros(length, dtype=np.float64)
    
    cdef int i
    cdef double high_low, high_close_prev, low_close_prev
    cdef double alpha_di = 1.0 / di_length
    cdef double alpha_adx = 1.0 / adx_smoothing
    cdef double sum_plus_minus_di
    
    # Calculate up and down movements
    for i in range(1, length):
        up[i] = high_data[i] - high_data[i-1]
        down[i] = low_data[i-1] - low_data[i]
    
    # Calculate Plus and Minus Directional Movement
    for i in range(1, length):
        if up[i] > down[i] and up[i] > 0:
            plus_dm[i] = up[i]
        else:
            plus_dm[i] = 0
            
        if down[i] > up[i] and down[i] > 0:
            minus_dm[i] = down[i]
        else:
            minus_dm[i] = 0
    
    # Calculate True Range
    for i in range(1, length):
        high_low = high_data[i] - low_data[i]
        high_close_prev = abs(high_data[i] - close_data[i-1])
        low_close_prev = abs(low_data[i] - close_data[i-1])
        tr[i] = max(high_low, max(high_close_prev, low_close_prev))
    
    # Set first values for TR
    tr[0] = high_data[0] - low_data[0]
    
    # Calculate RMA (Rolling Moving Average) for TR, Plus DM, and Minus DM
    # Initialize first values
    tr_rma[0] = tr[0]
    plus_dm_rma[0] = plus_dm[0]
    minus_dm_rma[0] = minus_dm[0]
    
    # Calculate RMA using exponential smoothing
    for i in range(1, length):
        tr_rma[i] = alpha_di * tr[i] + (1 - alpha_di) * tr_rma[i-1]
        plus_dm_rma[i] = alpha_di * plus_dm[i] + (1 - alpha_di) * plus_dm_rma[i-1]
        minus_dm_rma[i] = alpha_di * minus_dm[i] + (1 - alpha_di) * minus_dm_rma[i-1]
    
    # Calculate Plus and Minus Directional Indicators
    for i in range(length):
        if tr_rma[i] != 0:
            plus_di[i] = 100 * plus_dm_rma[i] / tr_rma[i]
            minus_di[i] = 100 * minus_dm_rma[i] / tr_rma[i]
        else:
            plus_di[i] = 0
            minus_di[i] = 0
    
    # Calculate DX
    for i in range(length):
        sum_plus_minus_di = plus_di[i] + minus_di[i]
        if sum_plus_minus_di != 0:
            dx[i] = 100 * abs(plus_di[i] - minus_di[i]) / sum_plus_minus_di
        else:
            dx[i] = 0
    
    # Calculate ADX using RMA of DX
    adx_values[0] = dx[0]
    for i in range(1, length):
        adx_values[i] = alpha_adx * dx[i] + (1 - alpha_adx) * adx_values[i-1]
    
    # Return as pandas DataFrame
    if index is not None:
        return pd.DataFrame({
            'Plus_DI': plus_di,
            'Minus_DI': minus_di,
            'ADX': adx_values
        }, index=index)
    else:
        return pd.DataFrame({
            'Plus_DI': plus_di,
            'Minus_DI': minus_di,
            'ADX': adx_values
        })
