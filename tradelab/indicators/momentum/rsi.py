"""Relative Strength Index (RSI) indicator implementation."""

import talib
import pandas as pd
from ..base import BaseIndicator


class RSI(BaseIndicator):
    """Relative Strength Index indicator class."""

    def __init__(self):
        super().__init__("RSI")
        
    def validate_period(self, period, min_value = 1):
        """
        Validate the RSI period.

        Args:
            period: RSI period to validate
            min_value: Minimum valid value for the period (default 1)
        
        Raises:
            ValueError: If the period is not valid.
        """
        if not isinstance(period, int) or period < min_value:
            raise ValueError(f"RSI period must be an integer greater than or equal to {min_value}.")

    def calculate(self, src: pd.Series, period: int = 14) -> pd.Series:
        """
        Calculate the Relative Strength Index (RSI) indicator.

        Args:
            src: Source prices (source for RSI calculation)
            period: RSI period (default 14)
        
        Returns:
            pd.Series: RSI values
        """

        self.validate_period(period)
        if not isinstance(src, pd.Series):
            raise ValueError("Source must be a pandas Series.")

        # Calculate price changes
        change = src.diff()

        # Separate gains and losses
        gains = change.where(change > 0, 0)
        losses = -change.where(change < 0, 0)

        # Calculate exponential weighted moving averages (equivalent to Pine Script's ta.rma)
        alpha = 1.0 / period
        avg_gains = gains.ewm(alpha=alpha, adjust=False).mean()
        avg_losses = losses.ewm(alpha=alpha, adjust=False).mean()

        # Calculate RSI
        rs = avg_gains / avg_losses
        rsi = 100 - (100 / (1 + rs))

        # Handle edge cases
        rsi = rsi.fillna(50)  # Fill NaN values with neutral RSI

        return pd.Series(rsi, index=src.index, name='RSI')


def rsi(src: pd.Series, period: int = 14) -> pd.Series:
    """
    Calculate the Relative Strength Index (RSI) indicator (functional interface).

    :param close: Close prices (source for RSI calculation)
    :param period: The period for the RSI calculation.
    :return: Series of RSI values (0-100).
    """
    indicator = RSI()
    return indicator.calculate(src=src, period=period)
