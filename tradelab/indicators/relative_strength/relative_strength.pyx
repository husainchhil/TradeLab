"""Relative Strength (RS) indicator calculation using Cython."""

import numpy as np
import pandas as pd
cimport numpy as cnp
cimport cython

ctypedef cnp.float64_t DTYPE_t

@cython.boundscheck(False)
@cython.wraparound(False)
def RELATIVE_STRENGTH(base_data, comparative_data, int length = 55, int base_shift = 5, int rs_ma_length = 50, int price_sma_length = 50):
    """
    Calculate the Relative Strength between two securities using Cython for performance.
    
    Parameters
    ----------
    base_data : array-like
        Source data for the base security (numpy array or pandas Series)
    comparative_data : array-like
        Source data for the comparative security (numpy array or pandas Series)
    length : int
        Period for calculating price ratios (default: 55)
    base_shift : int
        Base shift period (default: 5)
    rs_ma_length : int
        Moving average length for RS smoothing (default: 50)
    price_sma_length : int
        Moving average length for price smoothing (default: 50)
        
    Returns
    -------
    pandas.Series
        Series with Relative Strength values
    """
    # Validate inputs
    if not isinstance(base_data, pd.Series):
        base_data = pd.Series(base_data)
    if not isinstance(comparative_data, pd.Series):
        comparative_data = pd.Series(comparative_data)
    
    # Find common index (overlapping dates)
    common_index = base_data.index.intersection(comparative_data.index)
    
    if len(common_index) < max(length, rs_ma_length, price_sma_length):
        raise ValueError(
            f"Insufficient overlapping data points. Need at least {max(length, rs_ma_length, price_sma_length)} common dates")
    
    # Extract price series for common dates
    base_prices = base_data.loc[common_index]
    comparative_prices = comparative_data.loc[common_index]
    
    cdef cnp.ndarray[DTYPE_t, ndim=1] base_values = base_prices.values.astype(np.float64)
    cdef cnp.ndarray[DTYPE_t, ndim=1] comp_values = comparative_prices.values.astype(np.float64)
    cdef int data_length = len(base_values)
    cdef cnp.ndarray[DTYPE_t, ndim=1] base_ratio = np.empty(data_length, dtype=np.float64)
    cdef cnp.ndarray[DTYPE_t, ndim=1] comp_ratio = np.empty(data_length, dtype=np.float64)
    cdef cnp.ndarray[DTYPE_t, ndim=1] rs = np.empty(data_length, dtype=np.float64)
    
    cdef int i
    
    # Calculate price ratios
    for i in range(data_length):
        if i < length:
            base_ratio[i] = np.nan
            comp_ratio[i] = np.nan
            rs[i] = np.nan
        else:
            base_ratio[i] = base_values[i] / base_values[i - length]
            comp_ratio[i] = comp_values[i] / comp_values[i - length]
            
            # Calculate relative strength
            if comp_ratio[i] != 0:
                rs[i] = base_ratio[i] / comp_ratio[i] - 1.0
            else:
                rs[i] = np.nan
            
            # Round to 2 decimal places
            rs[i] = round(rs[i], 2)
    
    return pd.Series(rs, index=common_index, name='Relative Strength')