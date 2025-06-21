"""Relative Strength Index (RSI) indicator implementation."""

import talib
import pandas as pd
from ..base import BaseIndicator


class RSI(BaseIndicator):
    """Relative Strength Index indicator class."""

    def __init__(self):
        super().__init__("RSI")

    def calculate(self, data: pd.DataFrame, period: int = 14, column: str = 'close') -> pd.Series:
        """
        Calculate the Relative Strength Index (RSI) indicator.

        :param data: DataFrame containing OHLCV data.
        :param period: The period for the RSI calculation.
        :param column: The column to calculate RSI for (default: 'close').
        :return: Series of RSI values (0-100).
        """
        self.validate_period(period)

        # Validate and normalize data
        required_cols = {column.lower()}
        normalized_data = self.validate_data(data, required_cols)

        if normalized_data.empty:
            raise ValueError("No data available for RSI calculation")

        prices = normalized_data[column.lower()]

        # Calculate RSI using TA-Lib
        rsi_values = talib.RSI(prices, timeperiod=period)

        return pd.Series(rsi_values, index=prices.index, name='RSI')


def rsi(data: pd.DataFrame, period: int = 14, column: str = 'close') -> pd.Series:
    """
    Calculate the Relative Strength Index (RSI) indicator (functional interface).

    :param data: DataFrame containing OHLCV data.
    :param period: The period for the RSI calculation.
    :param column: The column to calculate RSI for (default: 'close').
    :return: Series of RSI values (0-100).
    """
    indicator = RSI()
    return indicator.calculate(data, period=period, column=column)
