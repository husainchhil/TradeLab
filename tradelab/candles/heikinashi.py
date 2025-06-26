from .base import BaseCandle
import pandas as pd


class HeikinAshi(BaseCandle):
    """Heikin-Ashi candle class."""

    def __init__(self):
        super().__init__("Heikin-Ashi")

    def calculate(self, data: pd.DataFrame, offset: int = 0, **kwargs) -> pd.DataFrame:
        """
        Calculate Heikin-Ashi candles from OHLCV data.

        :param data: DataFrame containing OHLCV data with columns 'open', 'high', 'low', 'close'.
        :return: DataFrame with Heikin-Ashi candles.
        """
        data = self.validate_data(data)

        open_ = data["open"]
        high = data["high"]
        low = data["low"]
        close = data["close"]

        # Calculate Heikin-Ashi values using vectorized operations
        ha_close = 0.25 * (open_ + high + low + close)
        
        # Initialize HA_open array
        ha_open = pd.Series(index=data.index, dtype=float)
        ha_open.iloc[0] = 0.5 * (open_.iloc[0] + close.iloc[0])
        
        # Vectorized calculation for HA_open (avoiding loop)
        for i in range(1, len(data)):
            ha_open.iloc[i] = 0.5 * (ha_open.iloc[i-1] + ha_close.iloc[i-1])
        
        # Calculate HA_high and HA_low using vectorized operations
        ha_high = pd.concat([ha_open, high, ha_close], axis=1).max(axis=1)
        ha_low = pd.concat([ha_open, low, ha_close], axis=1).min(axis=1)
        
        # Create result DataFrame
        df = pd.DataFrame({
            "HA_open": ha_open,
            "HA_high": ha_high,
            "HA_low": ha_low,
            "HA_close": ha_close,
        }, index=data.index)

        # Apply offset
        if offset != 0:
            df = df.shift(offset)

        # Handle fills
        if "fillna" in kwargs:
            df.fillna(kwargs["fillna"], inplace=True)
        if "fill_method" in kwargs:
            df.fillna(method=kwargs["fill_method"], inplace=True)

        # Set metadata
        df.name = "Heikin-Ashi"
        df.category = "candles"

        return df


def heikin_ashi(data: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate Heikin-Ashi candles (functional interface).

    :param data: DataFrame containing OHLCV data with columns 'open', 'high', 'low', 'close'.
    :return: DataFrame with Heikin-Ashi candles.
    """
    ha = HeikinAshi()
    return ha.calculate(data)
