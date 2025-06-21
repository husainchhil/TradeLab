"""Exponential Moving Average (EMA) indicator implementation."""

import pandas as pd
import talib
from ..base import BaseIndicator


class EMA(BaseIndicator):
    """Exponential Moving Average indicator class."""

    def __init__(self):
        super().__init__("EMA")

    def calculate(self, data: pd.DataFrame, period: int = 20, column: str = 'close') -> pd.Series:
        """
        Calculate the Exponential Moving Average (EMA) indicator.

        :param data: DataFrame containing OHLCV data.
        :param period: The period for the EMA calculation.
        :param column: The column to calculate EMA for (default: 'close').
        :return: Series of EMA values.
        """
        self.validate_period(period)

        # Validate and normalize data
        required_cols = {column.lower()}
        normalized_data = self.validate_data(data, required_cols)

        return pd.Series(
            talib.EMA(
                normalized_data[column.lower()].values,
                timeperiod=period
            ),
            name="EMA",
            index=normalized_data.index
        )


def ema(data: pd.DataFrame, period: int = 20, column: str = 'close') -> pd.Series:
    """
    Calculate the Exponential Moving Average (EMA) indicator (functional interface).

    :param data: DataFrame containing OHLCV data.
    :param period: The period for the EMA calculation.
    :param column: The column to calculate EMA for (default: 'close').
    :return: Series of EMA values.
    """
    indicator = EMA()
    return indicator.calculate(data, period=period, column=column)
