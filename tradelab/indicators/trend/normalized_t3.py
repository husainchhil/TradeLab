"""Normalized T3 Oscillator indicator implementation."""

import numpy as np
import pandas as pd
from ..base import BaseIndicator


class NormalizedT3(BaseIndicator):
    """Normalized T3 Oscillator indicator class."""

    def __init__(self):
        super().__init__("Normalized T3 Oscillator")

    def calculate(self, src: pd.Series, period: int = 200, t3_period: int = 2, volume_factor: float = 0.7) -> pd.Series:
        """
        Calculate the Normalized T3 Oscillator indicator.

        :param src: Pandas Series containing source data.
        :param period: The period for min-max normalization.
        :param t3_period: The period for the T3 calculation.
        :param volume_factor: Volume factor (vfactor) for T3 smoothing.
        :return: Series of Normalized T3 Oscillator values.
        """
        self.validate_period(period)
        self.validate_period(t3_period)

        if not (0 < volume_factor <= 1):
            raise ValueError("Volume factor must be between 0 and 1")

        self.validate_series(src, "Source Data")

        # T3 calculation using numpy only
        def t3_smoothing(data, period, vfactor):
            # Initialize arrays
            ema1 = np.zeros_like(data)
            ema2 = np.zeros_like(data)
            ema3 = np.zeros_like(data)
            ema4 = np.zeros_like(data)
            ema5 = np.zeros_like(data)
            ema6 = np.zeros_like(data)
            
            # Calculate smoothing factor
            alpha = 2.0 / (period + 1)
            
            # T3 coefficients
            c1 = -vfactor * vfactor * vfactor
            c2 = 3 * vfactor * vfactor + 3 * vfactor * vfactor * vfactor
            c3 = -6 * vfactor * vfactor - 3 * vfactor - 3 * vfactor * vfactor * vfactor
            c4 = 1 + 3 * vfactor + vfactor * vfactor * vfactor + 3 * vfactor * vfactor
            
            # Initialize first values
            ema1[0] = ema2[0] = ema3[0] = ema4[0] = ema5[0] = ema6[0] = data[0]
            
            # Calculate EMAs
            for i in range(1, len(data)):
                ema1[i] = alpha * data[i] + (1 - alpha) * ema1[i-1]
                ema2[i] = alpha * ema1[i] + (1 - alpha) * ema2[i-1]
                ema3[i] = alpha * ema2[i] + (1 - alpha) * ema3[i-1]
                ema4[i] = alpha * ema3[i] + (1 - alpha) * ema4[i-1]
                ema5[i] = alpha * ema4[i] + (1 - alpha) * ema5[i-1]
                ema6[i] = alpha * ema5[i] + (1 - alpha) * ema6[i-1]
            
            # Calculate T3
            t3 = c1 * ema6 + c2 * ema5 + c3 * ema4 + c4 * ema3
            return t3

        # Calculate T3
        t3_values = t3_smoothing(src.values, t3_period, volume_factor)

        # Calculate rolling min and max for normalization
        def rolling_min_max(data, window):
            min_vals = np.full_like(data, np.nan)
            max_vals = np.full_like(data, np.nan)
            
            for i in range(window - 1, len(data)):
                start_idx = max(0, i - window + 1)
                window_data = data[start_idx:i + 1]
                min_vals[i] = np.min(window_data)
                max_vals[i] = np.max(window_data)
            
            return min_vals, max_vals

        lowest, highest = rolling_min_max(t3_values, period)

        # Normalize T3 values
        range_values = highest - lowest
        range_values = np.where(range_values == 0, 1, range_values)
        normalized_t3 = (t3_values - lowest) / range_values - 0.5
        
        return pd.Series(normalized_t3, index=src.index, name='Normalized T3 Oscillator')


def normalized_t3(src : pd.Series, period: int = 200, t3_period: int = 2, volume_factor: float = 0.7) -> pd.Series:
    """
    Convenience function to calculate Normalized T3 Oscillator.

    :param src: Pandas Series containing source data.
    :param period: The period for min-max normalization.
    :param t3_period: The period for the T3 calculation.
    :param volume_factor: Volume factor (vfactor) for T3 smoothing.
    :return: Series of Normalized T3 Oscillator values.
    """
    indicator = NormalizedT3()
    return indicator.calculate(src, period, t3_period, volume_factor)
