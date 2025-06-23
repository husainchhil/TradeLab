"""Average Directional Index (ADX) indicator implementation."""

import pandas as pd
import numpy as np
from ..base import BaseIndicator


class ADX(BaseIndicator):
    """Average Directional Index indicator class."""

    def __init__(self):
        super().__init__("ADX")

    def validate_data(self, high: pd.Series, low: pd.Series, close: pd.Series) -> None:
        """
        Validate input data for ADX calculation.

        :param high: Series of high prices.
        :param low: Series of low prices.
        :param close: Series of close prices.
        """
        if not isinstance(high, pd.Series) or not isinstance(low, pd.Series) or not isinstance(close, pd.Series):
            raise TypeError("High, low, and close must be pandas Series.")
        
        if len(high) != len(low) or len(high) != len(close):
            raise ValueError("High, low, and close must have the same length.")
        
        if any(high < 0) or any(low < 0) or any(close < 0):
            raise ValueError("High, low, and close prices must be non-negative.")
        
    def validate_period(self, di_length: int, adx_smoothing: int) -> None:
        """
        Validate period parameters for ADX calculation.

        :param di_length: Length for the Directional Indicators.
        :param adx_smoothing: Smoothing period for ADX.
        """
        if not isinstance(di_length, int) or di_length < 1:
            raise ValueError("di_length must be an integer >= 1.")
        
        if not isinstance(adx_smoothing, int) or adx_smoothing < 1:
            raise ValueError("adx_smoothing must be an integer >= 1.")

    def calculate(self, high, low, close, di_length=14, adx_smoothing=14) -> pd.DataFrame:
        """
        Calculate the Average Directional Index (ADX) indicator.

        :param data: DataFrame containing OHLCV data with columns 'high', 'low', 'close'.
        :param period: The period for the ADX calculation.
        :return: Series of ADX values.
        """

        # Validate and normalize data
        self.validate_data(high, low, close)
        self.validate_period(di_length, adx_smoothing)

        up = high.diff()
        down = -low.diff()
        
        # Calculate Plus and Minus Directional Movement
        plus_dm = np.where((up > down) & (up > 0), up, 0)
        minus_dm = np.where((down > up) & (down > 0), down, 0)
        
        # Calculate True Range
        high_low = high - low
        high_close_prev = abs(high - close.shift(1))
        low_close_prev = abs(low - close.shift(1))
        tr = np.maximum(high_low, np.maximum(high_close_prev, low_close_prev))
        
        # Calculate smoothed values using RMA (Rolling Moving Average)
        def rma(series, length):
            alpha = 1.0 / length
            return series.ewm(alpha=alpha, adjust=False).mean()
        
        tr_rma = rma(pd.Series(tr, index=high.index), di_length)
        plus_dm_rma = rma(pd.Series(plus_dm, index=high.index), di_length)
        minus_dm_rma = rma(pd.Series(minus_dm, index=high.index), di_length)
        
        # Calculate Plus and Minus Directional Indicators
        plus_di = 100 * plus_dm_rma / tr_rma
        minus_di = 100 * minus_dm_rma / tr_rma
        
        # Calculate ADX
        dx = 100 * abs(plus_di - minus_di) / (plus_di + minus_di)
        dx = dx.fillna(0)  # Handle division by zero
        adx = rma(dx, adx_smoothing)
        
        return pd.DataFrame({
            'Plus_DI': plus_di,
            'Minus_DI': minus_di,
            'ADX': adx
        }, index=high.index)


def adx(high: pd.Series, low: pd.Series, close: pd.Series, di_length=14, adx_smoothing=14) -> pd.Series:
    """
    Calculate the Average Directional Index (ADX) indicator (functional interface).

    :param data: DataFrame containing OHLCV data with columns 'high', 'low', 'close'.
    :param period: The period for the ADX calculation.
    :return: Series of ADX values.
    """
    indicator = ADX()
    return indicator.calculate(high, low, close, di_length=di_length, adx_smoothing=adx_smoothing)
