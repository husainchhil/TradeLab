"""Exponential Moving Average (EMA) calculation."""

import numpy as np
import pandas as pd
cimport numpy as cnp
cimport cython

@cython.boundscheck(False)
@cython.wraparound(False)
def EMA(src, int period):
    if isinstance(src, pd.Series):
        values = src.values
        index = src.index
    else:
        values = np.asarray(src)
        index = None
    
    cdef cnp.ndarray[cnp.float64_t, ndim=1] data = values.astype(np.float64)
    cdef int length = len(data)
    cdef cnp.ndarray[cnp.float64_t, ndim=1] ema = np.empty(length, dtype=np.float64)
    cdef double alpha = 2.0 / (period + 1)
    cdef int i
    
    # Initialize first value
    ema[0] = data[0]
    
    # Calculate EMA
    for i in range(1, length):
        ema[i] = alpha * data[i] + (1 - alpha) * ema[i - 1]
    
    # Return as pandas Series
    if index is not None:
        return pd.Series(ema, index=index, name="EMA")
    else:
        return pd.Series(ema, name="EMA")
