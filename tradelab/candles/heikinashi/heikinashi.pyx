"""Heikin-Ashi candles calculation using Cython."""

import numpy as np
import pandas as pd
cimport numpy as cnp
cimport cython

ctypedef cnp.float64_t DTYPE_t

@cython.boundscheck(False)
@cython.wraparound(False)
def HEIKINASHI(data, int offset = 0, **kwargs):
    """
    Calculate Heikin-Ashi candles from OHLCV data using Cython for performance.

    :param data: DataFrame containing OHLCV data with columns 'open', 'high', 'low', 'close'.
    :param offset: Number of periods to shift the result.
    :return: DataFrame with Heikin-Ashi candles.
    """
    # Step 1: Validate input data has required columns
    if not isinstance(data, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame")

    # Normalize column names to lowercase
    normalized_data = data.copy()
    normalized_data.columns = [col.lower() for col in normalized_data.columns]

    required_columns = {'open', 'high', 'low', 'close'}

    # Check for required columns
    if not required_columns.issubset(normalized_data.columns):
        missing_cols = required_columns - set(normalized_data.columns)
        raise ValueError(f"DataFrame must contain columns: {missing_cols}")

    # Step 2: Extract OHLC data
    open_ = normalized_data["open"]
    high = normalized_data["high"]
    low = normalized_data["low"]
    close = normalized_data["close"]

    cdef int length = len(data)
    cdef cnp.ndarray[DTYPE_t, ndim=1] open_data = open_.values.astype(np.float64)
    cdef cnp.ndarray[DTYPE_t, ndim=1] high_data = high.values.astype(np.float64)
    cdef cnp.ndarray[DTYPE_t, ndim=1] low_data = low.values.astype(np.float64)
    cdef cnp.ndarray[DTYPE_t, ndim=1] close_data = close.values.astype(np.float64)
    
    cdef cnp.ndarray[DTYPE_t, ndim=1] ha_open = np.empty(length, dtype=np.float64)
    cdef cnp.ndarray[DTYPE_t, ndim=1] ha_high = np.empty(length, dtype=np.float64)
    cdef cnp.ndarray[DTYPE_t, ndim=1] ha_low = np.empty(length, dtype=np.float64)
    cdef cnp.ndarray[DTYPE_t, ndim=1] ha_close = np.empty(length, dtype=np.float64)
    
    cdef int i
    cdef double temp_high, temp_low

    # Step 3: Calculate Heikin-Ashi Close (average of OHLC)
    for i in range(length):
        ha_close[i] = 0.25 * (open_data[i] + high_data[i] + low_data[i] + close_data[i])

    # Step 4: Calculate Heikin-Ashi Open
    # First HA_open is average of first open and close
    ha_open[0] = 0.5 * (open_data[0] + close_data[0])

    # Subsequent HA_open values are average of previous HA_open and HA_close
    for i in range(1, length):
        ha_open[i] = 0.5 * (ha_open[i-1] + ha_close[i-1])

    # Step 5: Calculate Heikin-Ashi High (max of HA_open, high, HA_close)
    for i in range(length):
        temp_high = ha_open[i] if ha_open[i] > high_data[i] else high_data[i]
        ha_high[i] = temp_high if temp_high > ha_close[i] else ha_close[i]

    # Step 6: Calculate Heikin-Ashi Low (min of HA_open, low, HA_close)
    for i in range(length):
        temp_low = ha_open[i] if ha_open[i] < low_data[i] else low_data[i]
        ha_low[i] = temp_low if temp_low < ha_close[i] else ha_close[i]

    # Step 7: Create result DataFrame
    df = pd.DataFrame({
        "Open": ha_open,
        "High": ha_high,
        "Low": ha_low,
        "Close": ha_close,
    }, index=data.index)

    # Add trend column using .loc to avoid chained assignment warning
    df.loc[:, 'Trend'] = np.where(df.loc[:, 'Close'] > df.loc[:, 'Open'], 1, -1)

    # Step 8: Apply offset if specified
    if offset != 0:
        df = df.shift(offset)

    # Step 9: Handle fills
    if "fillna" in kwargs:
        df = df.fillna(kwargs["fillna"])
    if "fill_method" in kwargs:
        df = df.fillna(method=kwargs["fill_method"])

    # Step 10: Set metadata
    df.name = "Heikin-Ashi"
    df.category = "candles"

    return df