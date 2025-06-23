"""Average True Range (ATR) indicator implementation."""

import numpy as np
import talib
import pandas as pd
from ..base import BaseIndicator


class ATR(BaseIndicator):
    """Average True Range indicator class."""

    def __init__(self):
        super().__init__("ATR")

    def calculate(self, high: pd.Series, low: pd.Series, close: pd.Series, period: int = 14) -> pd.Series:
        """
        Calculate the Average True Range (ATR) indicator.

        :param data: DataFrame containing OHLCV data with columns 'high', 'low', 'close'.
        :param period: The period for the ATR calculation.
        :return: Series of ATR values.
        """
        self.validate_period(period)
        self.validate_hlc(high, low, close)

        tr1 = high - low
        tr2 = np.abs(high - close.shift(1))
        tr3 = np.abs(low - close.shift(1))
        true_range = np.maximum(tr1, np.maximum(tr2, tr3))

        # Calculate ATR using RMA (Rolling Moving Average) - equivalent to EMA with alpha = 1/period
        alpha = 1.0 / period
        atr = np.zeros(len(true_range))
        atr[0] = true_range.iloc[0] if not np.isnan(true_range.iloc[0]) else 0

        for i in range(1, len(true_range)):
            if not np.isnan(true_range.iloc[i]):
                atr[i] = alpha * true_range.iloc[i] + (1 - alpha) * atr[i-1]
            else:
                atr[i] = atr[i-1]

        return pd.Series(atr, name="ATR", index=high.index)


def atr(high: pd.Series, low: pd.Series, close: pd.Series, period: int = 14) -> pd.Series:
    """
    Calculate the Average True Range (ATR) indicator (functional interface).

    :param data: DataFrame containing OHLCV data with columns 'high', 'low', 'close'.
    :param period: The period for the ATR calculation.
    :return: Series of ATR values.
    """
    indicator = ATR()
    return indicator.calculate(high, low, close, period=period)
