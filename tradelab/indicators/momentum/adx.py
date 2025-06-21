"""Average Directional Index (ADX) indicator implementation."""

import pandas as pd
import talib
from ..base import BaseIndicator


class ADX(BaseIndicator):
    """Average Directional Index indicator class."""

    def __init__(self):
        super().__init__("ADX")

    def calculate(self, data: pd.DataFrame, period: int = 14) -> pd.Series:
        """
        Calculate the Average Directional Index (ADX) indicator.

        :param data: DataFrame containing OHLCV data with columns 'high', 'low', 'close'.
        :param period: The period for the ADX calculation.
        :return: Series of ADX values.
        """
        self.validate_period(period)

        # Validate and normalize data
        required_cols = {'high', 'low', 'close'}
        normalized_data = self.validate_data(data, required_cols)

        return pd.Series(
            talib.ADX(
                normalized_data['high'].values,
                normalized_data['low'].values,
                normalized_data['close'].values,
                timeperiod=period
            ),
            name="ADX",
            index=normalized_data.index
        )


def adx(data: pd.DataFrame, period: int = 14) -> pd.Series:
    """
    Calculate the Average Directional Index (ADX) indicator (functional interface).

    :param data: DataFrame containing OHLCV data with columns 'high', 'low', 'close'.
    :param period: The period for the ADX calculation.
    :return: Series of ADX values.
    """
    indicator = ADX()
    return indicator.calculate(data, period=period)
