import pandas as pd
import numpy as np


def resample_ohlcv(
    df: pd.DataFrame,
    freq: str = "1H",
    anchor: str = "09:15:00"
) -> pd.DataFrame:
    """
    Resample OHLCV (Open, High, Low, Close, Volume) data to a specified frequency.

    This function handles both intraday and weekly resampling of financial time series data.
    For intraday resampling, it uses a custom anchor time to align the bins. For weekly
    resampling, it supports standard pandas weekly frequencies with day-of-week anchoring.

    Parameters:
    df : pd.DataFrame
        Input DataFrame containing OHLCV data with datetime index.
        Must have columns: 'Open', 'High', 'Low', 'Close', 'Volume'.
    freq : str, default "1H"
        Frequency string for resampling. Examples:
        - Intraday: "1H", "30T", "15min", "5S"
        - Weekly: "1W", "2W"
    anchor : str, default "09:15:00"
        For intraday resampling: Time string (HH:MM:SS) to anchor the bins.
        For weekly resampling: Day of week ('MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN').

    Returns:
    pd.DataFrame
        Resampled DataFrame with OHLCV data aggregated according to the specified frequency.
        - Open: First value in each bin
        - High: Maximum value in each bin
        - Low: Minimum value in each bin
        - Close: Last value in each bin
        - Volume: Sum of all values in each bin
        Index is named 'Date' and contains the bin start timestamps.

    Notes:
    - For intraday resampling, data points occurring before the anchor time are filtered out
    - Weekly resampling uses pandas' built-in resample functionality with proper labeling
    - All NaN values are dropped from the final result

    Examples:
    Resample to 1-hour bars starting at 9:15 AM
    >>> hourly_data = resample_ohlcv(df, freq="1H", anchor="09:15:00")

    Resample to weekly bars starting on Monday
    >>> weekly_data = resample_ohlcv(df, freq="1W", anchor="MON")

    Resample to 15-minute bars starting at market open
    >>> intraday_data = resample_ohlcv(df, freq="15T", anchor="09:30:00") 
    """
    # Validate input DataFrame
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame")

    if df.empty:
        raise ValueError("Input DataFrame cannot be empty")

    df.columns = df.columns.str.strip().str.capitalize()

    required_columns = {'Open', 'High', 'Low', 'Close', 'Volume'}
    if not required_columns.issubset(df.columns):
        raise ValueError(
            f"Input DataFrame must contain the following columns: {required_columns}")

    # Check if this is weekly resampling
    if freq.upper().endswith('W'):
        return _resample_weekly(df, freq, anchor)
    else:
        return _resample_intraday(df, freq, anchor)


def _resample_weekly(df: pd.DataFrame, freq: str, anchor: str) -> pd.DataFrame:
    """Handle weekly resampling with day-of-week anchor."""

    # Map day names to pandas weekly frequency strings
    day_mapping = {
        'MON': f'{freq}-MON', 'TUE': f'{freq}-TUE', 'WED': f'{freq}-WED',
        'THU': f'{freq}-THU', 'FRI': f'{freq}-FRI', 'SAT': f'{freq}-SAT', 'SUN': f'{freq}-SUN'
    }

    if anchor.upper() in day_mapping:
        weekly_freq = day_mapping[anchor.upper()]
    else:
        weekly_freq = f'{freq}-MON'  # Default to Monday if invalid anchor

    agg_rules = {
        "Open": "first",
        "High": "max",
        "Low": "min",
        "Close": "last",
        "Volume": "sum",
    }

    result = (
        df.resample(weekly_freq, label='left', closed='left')
        .agg(agg_rules)
        .dropna()
    )
    result.index.name = 'Date'
    return result


def _resample_intraday(df: pd.DataFrame, freq: str, anchor: str) -> pd.DataFrame:
    """Handle intraday resampling with time anchor."""
    freq_ns = pd.to_timedelta(freq).value
    anchor_td = pd.to_timedelta(anchor)

    # Calculate bin assignments for each timestamp
    idx = df.index
    day_start = idx.normalize()
    time_since_anchor = (idx - day_start - anchor_td).astype('int64')

    # Filter out data before anchor time
    valid_mask = time_since_anchor >= 0
    if not valid_mask.any():
        # Return empty DataFrame if no valid data
        result = df.head(0).copy()
        result.index.name = 'Date'
        return result

    df_valid = df[valid_mask].copy()
    idx_valid = df_valid.index
    day_valid = idx_valid.normalize()
    time_valid = (idx_valid - day_valid - anchor_td).astype('int64')

    # Calculate bin starts
    bin_indices = np.floor_divide(time_valid, freq_ns)
    bin_starts = day_valid + anchor_td + \
        pd.to_timedelta(bin_indices * freq_ns, unit="ns")

    df_valid["bin_start"] = bin_starts

    agg_rules = {
        "Open": "first",
        "High": "max",
        "Low": "min",
        "Close": "last",
        "Volume": "sum",
    }

    result = (
        df_valid
        .groupby("bin_start", sort=True)
        .agg(agg_rules)
        .dropna()
    )
    result.index.name = 'Date'
    return result


__all__ = ['resample_ohlcv']
