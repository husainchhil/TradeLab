"""Renko candles calculation using Cython."""

import numpy as np
import pandas as pd
cimport numpy as cnp
cimport cython
from libc.math cimport fabs

ctypedef cnp.float64_t DTYPE_t

cdef list _MODE_dict = ['normal', 'wicks', 'nongap', 'reverse-wicks',
                        'reverse-nongap', 'fake-r-wicks', 'fake-r-nongap']

@cython.boundscheck(False)
@cython.wraparound(False)
def RENKO(data, double brick_size, str mode = "wicks"):
    """
    Calculate Renko candles using Cython for performance.

    :param data: DataFrame containing OHLCV data with columns 'datetime' and 'close'.
    :param brick_size: Size of each Renko brick.
    :param mode: Mode for calculating Renko bricks.
    :return: DataFrame with Renko candles.
    """
    
    # Step 1: Validate inputs
    if not isinstance(data, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame")

    # Normalize column names to lowercase
    normalized_data = data.copy()
    normalized_data.columns = [col.lower() for col in normalized_data.columns]

    required_columns = {'open', 'high', 'low', 'close', 'volume'}

    # Check for required columns
    if not required_columns.issubset(normalized_data.columns):
        missing_cols = required_columns - set(normalized_data.columns)
        raise ValueError(f"DataFrame must contain columns: {missing_cols}")
    
    if not isinstance(brick_size, (int, float)):
        raise TypeError("brick_size must be an int or float")
    
    if brick_size <= 0:
        raise ValueError("brick_size cannot be 'None' or '<= 0'")
    
    if mode not in _MODE_dict:
        raise ValueError(f"Only {_MODE_dict} options are valid.")
    
    # Step 2: Prepare DataFrame
    df = normalized_data.copy()
    if 'datetime' not in df.columns:
        df["datetime"] = df.index
    
    if 'close' not in df.columns:
        raise ValueError("Column 'close' doesn't exist!")
    
    cdef int df_len = len(df["close"])
    cdef cnp.ndarray[DTYPE_t, ndim=1] close_data = df["close"].values.astype(np.float64)
    
    # Step 3: Initialize Renko Single Data structure
    cdef double first_close = close_data[0]
    cdef double initial_price = (first_close // brick_size) * brick_size
    
    # Initialize lists for results
    origin_index = [0]
    date = [df["datetime"].iat[0]]
    price = [initial_price]
    direction = [0]
    wick = [initial_price]
    volume = [1]
    
    # Step 4: Initialize tracking variables
    cdef double wick_min_i = initial_price
    cdef double wick_max_i = initial_price
    cdef int volume_i = 1
    cdef int i
    cdef double df_close
    cdef double last_price
    cdef double current_n_bricks
    cdef double current_direction
    cdef double last_direction
    cdef bint is_same_direction
    cdef double total_same_bricks
    cdef double renko_price
    cdef double wick_val
    cdef int j
    
    # Step 5: Process each price point
    for i in range(1, df_len):
        df_close = close_data[i]
        wick_min_i = df_close if df_close < wick_min_i else wick_min_i
        wick_max_i = df_close if df_close > wick_max_i else wick_max_i
        volume_i += 1
        
        last_price = price[len(price)-1]
        current_n_bricks = (df_close - last_price) / brick_size
        current_direction = 1.0 if current_n_bricks > 0 else (-1.0 if current_n_bricks < 0 else 0.0)
        
        if current_direction == 0:
            continue
            
        last_direction = direction[len(direction)-1]
        is_same_direction = ((current_direction > 0 and last_direction >= 0)
                            or (current_direction < 0 and last_direction <= 0))
        
        total_same_bricks = current_n_bricks if is_same_direction else 0
        
        # Handle direction reversal
        if not is_same_direction and fabs(current_n_bricks) >= 2:
            # Add reversal bricks
            last_price = price[len(price)-1]
            renko_price = last_price + (current_direction * 2 * brick_size)
            wick_val = wick_min_i if current_n_bricks > 0 else wick_max_i
            
            origin_index.append(i)
            date.append(df["datetime"].iat[i])
            price.append(renko_price)
            direction.append(current_direction)
            wick.append(wick_val)
            volume.append(volume_i)
            
            volume_i = 1
            wick_min_i = renko_price if current_n_bricks > 0 else wick_min_i
            wick_max_i = renko_price if current_n_bricks < 0 else wick_max_i
            
            total_same_bricks = current_n_bricks - 2 * current_direction
        
        # Add all bricks in the same direction
        for j in range(int(fabs(total_same_bricks))):
            last_price = price[len(price)-1]
            renko_price = last_price + (current_direction * 1 * brick_size)
            wick_val = wick_min_i if current_n_bricks > 0 else wick_max_i
            
            origin_index.append(i)
            date.append(df["datetime"].iat[i])
            price.append(renko_price)
            direction.append(current_direction)
            wick.append(wick_val)
            volume.append(volume_i)
            
            volume_i = 1
            wick_min_i = renko_price if current_n_bricks > 0 else wick_min_i
            wick_max_i = renko_price if current_n_bricks < 0 else wick_max_i
    
    # Step 6: Calculate final DataFrame
    dates = date
    prices = price
    directions = direction
    wicks = wick
    volumes = volume
    indexes = list(range(len(prices)))
    
    # Initialize result dictionary
    df_dict = {
        "datetime": [],
        "open": [],
        "high": [],
        "low": [],
        "close": [],
        "volume": [],
    }
    
    # Step 7: Apply mode rules
    cdef bint reverse_rule = mode in ["normal", "wicks", "reverse-wicks", "fake-r-wicks"]
    cdef bint fake_reverse_rule = mode in ["fake-r-nongap", "fake-r-wicks"]
    cdef bint same_direction_rule = mode in ["wicks", "nongap"]
    
    cdef double prev_direction = 0
    cdef double prev_close = 0
    cdef double prev_close_up = 0
    cdef double prev_close_down = 0
    cdef double price_val, direction_val, wick_val_final
    cdef int volume_val
    
    # Step 8: Build OHLCV data
    for k in range(len(prices)):
        price_val = prices[k]
        direction_val = directions[k]
        date_val = dates[k]
        wick_val_final = wicks[k]
        volume_val = volumes[k]
        
        if direction_val != 0:
            df_dict["datetime"].append(date_val)
            df_dict["close"].append(price_val)
            df_dict["volume"].append(volume_val)
        
        # Current Renko (UP)
        if direction_val == 1.0:
            df_dict["high"].append(price_val)
            # Previous same direction(UP)
            if prev_direction == 1:
                df_dict["open"].append(
                    wick_val_final if mode == "nongap" else prev_close_up)
                df_dict["low"].append(
                    wick_val_final if same_direction_rule else prev_close_up)
            # Previous reverse direction(DOWN)
            else:
                if reverse_rule:
                    df_dict["open"].append(prev_close + brick_size)
                elif mode == "fake-r-nongap":
                    df_dict["open"].append(prev_close_down)
                else:
                    df_dict["open"].append(wick_val_final)
                
                if mode == "normal":
                    df_dict["low"].append(prev_close + brick_size)
                elif fake_reverse_rule:
                    df_dict["low"].append(prev_close_down)
                else:
                    df_dict["low"].append(wick_val_final)
            prev_close_up = price_val
            
        # Current Renko (DOWN)
        elif direction_val == -1.0:
            df_dict["low"].append(price_val)
            # Previous same direction(DOWN)
            if prev_direction == -1:
                df_dict["open"].append(
                    wick_val_final if mode == "nongap" else prev_close_down)
                df_dict["high"].append(
                    wick_val_final if same_direction_rule else prev_close_down)
            # Previous reverse direction(UP)
            else:
                if reverse_rule:
                    df_dict["open"].append(prev_close - brick_size)
                elif mode == "fake-r-nongap":
                    df_dict["open"].append(prev_close_up)
                else:
                    df_dict["open"].append(wick_val_final)
                
                if mode == "normal":
                    df_dict["high"].append(prev_close - brick_size)
                elif fake_reverse_rule:
                    df_dict["high"].append(prev_close_up)
                else:
                    df_dict["high"].append(wick_val_final)
            prev_close_down = price_val
            
        # BEGIN OF DICT
        else:
            df_dict["datetime"].append(np.nan)
            df_dict["low"].append(np.nan)
            df_dict["close"].append(np.nan)
            df_dict["high"].append(np.nan)
            df_dict["open"].append(np.nan)
            df_dict["volume"].append(np.nan)
        
        prev_direction = direction_val
        prev_close = price_val
    
    # Step 9: Create and format final DataFrame
    result_df = pd.DataFrame(df_dict)
    
    # Remove the first 2 lines that are initialization artifacts
    result_df = result_df.drop(result_df.head(2).index)
    
    # Set datetime index
    result_df.index = pd.DatetimeIndex(result_df["datetime"])
    result_df = result_df.drop(columns=['datetime'])
    
    # Add trend column using .loc to avoid chained assignment warning
    result_df.loc[:, 'Trend'] = np.where(result_df.loc[:, 'close'] > result_df.loc[:, 'open'], 1, -1)
    
    # Capitalize column names
    result_df.columns = [col.capitalize() for col in result_df.columns]
    
    return result_df