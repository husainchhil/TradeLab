"""Exponential Moving Average (EMA) indicator implementation."""

import numpy as np
import pandas as pd
from ..base import BaseIndicator


class EMA(BaseIndicator):
    """Exponential Moving Average indicator class."""

    def __init__(self):
        super().__init__("EMA")

    def calculate(self, src: pd.Series, period: int = 20) -> pd.Series:
        """
        Calculate the Exponential Moving Average (EMA) indicator.

        :param src: Source prices (source for EMA calculation).
        :param period: The period for the EMA calculation.
        :return: Series of EMA values.
        """
        self.validate_period(period)
        if not isinstance(src, pd.Series):
            raise ValueError("Source must be a pandas Series.")

        values = src.values
        ema = np.empty_like(values, dtype=float)
        alpha = 2 / (period + 1)
        ema[0] = values[0]
        for i in range(1, len(values)):
            ema[i] = alpha * values[i] + (1 - alpha) * ema[i - 1]
        return pd.Series(ema, name="EMA", index=src.index)


def ema(src: pd.Series, period: int = 20) -> pd.Series:
    """
    Calculate the Exponential Moving Average (EMA) indicator (functional interface).

    :param src: Source prices (source for EMA calculation).
    :param period: The period for the EMA calculation.
    :return: Series of EMA values.
    """
    indicator = EMA()
    return indicator.calculate(src, period=period)
