"""Normalized T3 Oscillator indicator implementation."""

import numpy as np
import pandas as pd
import talib
from ..base import BaseIndicator


class NormalizedT3(BaseIndicator):
    """Normalized T3 Oscillator indicator class."""

    def __init__(self):
        super().__init__("Normalized T3 Oscillator")

    def calculate(self, data: pd.DataFrame, period: int = 200, t3_period: int = 2, volume_factor: float = 0.7, column: str = 'close') -> pd.Series:
        """
        Calculate the Normalized T3 Oscillator indicator.

        :param data: DataFrame containing OHLCV data.
        :param period: The period for min-max normalization.
        :param t3_period: The period for the T3 calculation.
        :param volume_factor: Volume factor (vfactor) for T3 smoothing.
        :param column: The column to calculate T3 for (default: 'close').
        :return: Series of Normalized T3 Oscillator values.
        """
        self.validate_period(period)
        self.validate_period(t3_period)

        if not (0 < volume_factor <= 1):
            raise ValueError("Volume factor must be between 0 and 1")

        # Validate and normalize data
        required_cols = {column.lower()}
        normalized_data = self.validate_data(data, required_cols)

        if normalized_data.empty:
            raise ValueError("No data available for T3 calculation")

        prices = normalized_data[column.lower()]

        t3 = talib.T3(prices, timeperiod=t3_period, vfactor=volume_factor)

        lowest = talib.MIN(t3, timeperiod=period)
        highest = talib.MAX(t3, timeperiod=period)

        range_values = highest - lowest
        range_values = np.where(range_values == 0, 1, range_values)
        normalized_t3 = (t3 - lowest) / range_values - 0.5
        return pd.Series(normalized_t3, index=prices.index, name='Normalized T3 Oscillator')


def normalized_t3(data: pd.DataFrame, period: int = 200, t3_period: int = 2, volume_factor: float = 0.7, column: str = 'close') -> pd.Series:
    """
    Calculate the Normalized T3 Oscillator indicator (functional interface).

    :param data: DataFrame containing OHLCV data.
    :param period: The period for min-max normalization.
    :param t3_period: The period for the T3 calculation.
    :param volume_factor: Volume factor (vfactor) for T3 smoothing.
    :param column: The column to calculate T3 for (default: 'close').
    :return: Series of Normalized T3 Oscillator values.
    """
    indicator = NormalizedT3()
    return indicator.calculate(data, period=period, t3_period=t3_period, volume_factor=volume_factor, column=column)
