"""Moving Average (SMA/EMA) calculation using Cython."""

import numpy as np
import pandas as pd
cimport numpy as cnp
cimport cython

@cython.boundscheck(False)
@cython.wraparound(False)
def MOVING_AVERAGE(src, int period, int ma_type):
    """
    Calculate Moving Average using Cython for performance.

    Parameters
    ----------
    src : array-like
        Source prices (numpy array or pandas Series)
    period : int
        The period for moving average calculation
    ma_type : int
        0 for SMA, 1 for EMA

    Returns
    -------
    pandas.Series
        Series with moving average values, indexed same as input if pandas Series
    """
    if isinstance(src, pd.Series):
        values = src.values
        index = src.index
    else:
        values = np.asarray(src)
        index = None

    cdef cnp.ndarray[cnp.float64_t, ndim=1] data = values.astype(np.float64)
    cdef int length = len(data)
    cdef cnp.ndarray[cnp.float64_t, ndim=1] out = np.empty(length, dtype=np.float64)
    cdef int i
    cdef double alpha
    cdef double window_sum

    if ma_type == 1:
        alpha = 2.0 / (period + 1)
        out[0] = data[0]
        for i in range(1, length):
            out[i] = alpha * data[i] + (1 - alpha) * out[i - 1]
        name = "EMA"
    else:
        window_sum = 0.0
        for i in range(length):
            window_sum += data[i]
            if i >= period:
                window_sum -= data[i - period]
                out[i] = window_sum / period
            else:
                out[i] = window_sum / (i + 1)
        name = "SMA"

    if index is not None:
        return pd.Series(out, index=index, name=name)
    else:
        return pd.Series(out, name=name)
