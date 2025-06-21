"""Average True Range (ATR) indicator implementation."""

import talib
import pandas as pd
from ..base import BaseIndicator


class ATR(BaseIndicator):
    """Average True Range indicator class."""

    def __init__(self):
        super().__init__("ATR")

    def calculate(self, data: pd.DataFrame, period: int = 14) -> pd.Series:
        """
        Calculate the Average True Range (ATR) indicator.

        :param data: DataFrame containing OHLCV data with columns 'high', 'low', 'close'.
        :param period: The period for the ATR calculation.
        :return: Series of ATR values.
        """
        self.validate_period(period)

        # Validate and normalize data
        required_cols = {'high', 'low', 'close'}
        normalized_data = self.validate_data(data, required_cols)

        high = normalized_data['high']
        low = normalized_data['low']
        close = normalized_data['close']

        return pd.Series(
            talib.ATR(
                high=high.values,
                low=low.values,
                close=close.values,
                timeperiod=period
            ),
            name="ATR",
            index=normalized_data.index
        )


def atr(data: pd.DataFrame, period: int = 14) -> pd.Series:
    """
    Calculate the Average True Range (ATR) indicator (functional interface).

    :param data: DataFrame containing OHLCV data with columns 'high', 'low', 'close'.
    :param period: The period for the ATR calculation.
    :return: Series of ATR values.
    """
    indicator = ATR()
    return indicator.calculate(data, period=period)
