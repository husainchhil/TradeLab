"""SuperTrend indicator implementation."""

import fixedta as ta
import pandas as pd
from ..base import BaseIndicator
from ..volatility import atr
import numpy as np


class SuperTrend(BaseIndicator):
    """SuperTrend indicator class."""

    def __init__(self):
        super().__init__("SuperTrend")

    def calculate(self, high: pd.Series, low: pd.Series, close: pd.Series, period: int = 10, multiplier: float = 3.0) -> pd.DataFrame:
        """
        Calculate the SuperTrend indicator.

        :param data: DataFrame containing OHLCV data with columns 'open', 'high', 'low', 'close', and 'volume'.
        :param period: The period for the ATR calculation.
        :param multiplier: The multiplier for the ATR to calculate the SuperTrend.
        :return: DataFrame with SuperTrend values and direction.
        """
        self.validate_period(period)
        self.validate_multiplier(multiplier)
        self.validate_hlc(high, low, close)

        atr_values = atr(high, low, close, period=period)
        hl2 = (high + low) / 2

        # Calculate upper and lower bands
        upperband = hl2 + (multiplier * atr_values)
        lowerband = hl2 - (multiplier * atr_values)

        # Initialize arrays
        supertrend = np.zeros(len(close))
        direction = np.ones(len(close), dtype=int)

        # Set initial values
        supertrend[0] = lowerband.iloc[0]  # Start with lowerband
        direction[0] = 1  # Start with uptrend

        # Calculate Supertrend
        for i in range(1, len(close)):
            # Determine trend direction based on previous close vs previous supertrend
            if close.iloc[i-1] <= supertrend[i-1]:
                direction[i] = -1  # Downtrend
            else:
                direction[i] = 1   # Uptrend
            
            # Calculate supertrend value based on direction
            if direction[i] == 1:  # Uptrend
                supertrend[i] = lowerband.iloc[i]
                if direction[i-1] == 1:  # Was also uptrend
                    supertrend[i] = max(lowerband.iloc[i], supertrend[i-1])
            else:  # Downtrend
                supertrend[i] = upperband.iloc[i]
                if direction[i-1] == -1:  # Was also downtrend
                    supertrend[i] = min(upperband.iloc[i], supertrend[i-1])

        st = pd.DataFrame({'Supertrend': supertrend, 'Direction': direction}, index=high.index)

        return st


def supertrend(high: pd.Series, low: pd.Series, close: pd.Series, period: int = 10, multiplier: float = 3.0) -> pd.DataFrame:
    """
    Calculate the SuperTrend indicator (functional interface).

    :param data: DataFrame containing OHLCV data with columns 'open', 'high', 'low', 'close', and 'volume'.
    :param period: The period for the ATR calculation.
    :param multiplier: The multiplier for the ATR to calculate the SuperTrend.
    :return: DataFrame with SuperTrend values and direction.
    """
    indicator = SuperTrend()
    return indicator.calculate(high, low, close, period=period, multiplier=multiplier)
