from .base import BaseCandle
import fixedta as ta
import pandas as pd


class HeikinAshi(BaseCandle):
    """Heikin-Ashi candle class."""

    def __init__(self):
        super().__init__("Heikin-Ashi")

    def calculate(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate Heikin-Ashi candles from OHLCV data.

        :param data: DataFrame containing OHLCV data with columns 'open', 'high', 'low', 'close'.
        :return: DataFrame with Heikin-Ashi candles.
        """
        ha_data = self.validate_data(data)

        return ta.ha(
            open_=ha_data['open'],
            high=ha_data['high'],
            low=ha_data['low'],
            close=ha_data['close']
        )


def heikin_ashi(data: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate Heikin-Ashi candles (functional interface).

    :param data: DataFrame containing OHLCV data with columns 'open', 'high', 'low', 'close'.
    :return: DataFrame with Heikin-Ashi candles.
    """
    ha = HeikinAshi()
    return ha.calculate(data)
