"""SuperTrend indicator implementation."""

import fixedta as ta
import pandas as pd
from ..base import BaseIndicator


class SuperTrend(BaseIndicator):
    """SuperTrend indicator class."""

    def __init__(self):
        super().__init__("SuperTrend")

    def calculate(self, data: pd.DataFrame, period: int = 10, multiplier: float = 3.0) -> pd.DataFrame:
        """
        Calculate the SuperTrend indicator.

        :param data: DataFrame containing OHLCV data with columns 'open', 'high', 'low', 'close', and 'volume'.
        :param period: The period for the ATR calculation.
        :param multiplier: The multiplier for the ATR to calculate the SuperTrend.
        :return: DataFrame with SuperTrend values and direction.
        """
        self.validate_period(period)
        self.validate_multiplier(multiplier)

        # Validate and normalize data
        required_cols = {'high', 'low', 'close'}
        normalized_data = self.validate_data(data, required_cols)

        high = normalized_data['high']
        low = normalized_data['low']
        close = normalized_data['close']

        st = ta.supertrend(
            high=high,
            low=low,
            close=close,
            period=period,
            multiplier=multiplier
        )

        return pd.DataFrame({
            'Supertrend': st[st.columns[0]],
            'Direction': st[st.columns[1]],
        })


def supertrend(data: pd.DataFrame, period: int = 10, multiplier: float = 3.0) -> pd.DataFrame:
    """
    Calculate the SuperTrend indicator (functional interface).

    :param data: DataFrame containing OHLCV data with columns 'open', 'high', 'low', 'close', and 'volume'.
    :param period: The period for the ATR calculation.
    :param multiplier: The multiplier for the ATR to calculate the SuperTrend.
    :return: DataFrame with SuperTrend values and direction.
    """
    indicator = SuperTrend()
    return indicator.calculate(data, period=period, multiplier=multiplier)
