"""Relative Strength (RS) indicator implementation."""

import pandas as pd
import numpy as np
from typing import Union, Tuple, Optional
from ..base import BaseIndicator


class RelativeStrength(BaseIndicator):
    """Relative Strength indicator class for comparing two securities."""

    def __init__(self):
        super().__init__("Relative Strength")

    def calculate(self, base_data: pd.DataFrame, comparative_data: pd.DataFrame,
                  length: int = 55, base_shift: int = 5, rs_ma_length: int = 50,
                  price_sma_length: int = 50, base_column: str = 'close',
                  comparative_column: str = 'close') -> pd.DataFrame:
        """
        Calculate the Relative Strength between two securities.

        :param base_data: DataFrame containing OHLCV data for the base security
        :param comparative_data: DataFrame containing OHLCV data for the comparative security
        :param length: Period for calculating price ratios (default: 55)
        :param base_shift: Base shift period (default: 5)
        :param rs_ma_length: Moving average length for RS smoothing (default: 50)
        :param price_sma_length: Moving average length for price smoothing (default: 50)
        :param base_column: Column to use from base data (default: 'close')
        :param comparative_column: Column to use from comparative data (default: 'close')
        :return: DataFrame with RS calculations and signals
        """
        self.validate_period(length)
        self.validate_period(base_shift)
        self.validate_period(rs_ma_length)
        self.validate_period(price_sma_length)

        # Validate and normalize data
        required_cols = {base_column.lower()}
        normalized_base = self.validate_data(base_data, required_cols)

        required_cols = {comparative_column.lower()}
        normalized_comparative = self.validate_data(
            comparative_data, required_cols)

        # Find common index (overlapping dates)
        common_index = normalized_base.index.intersection(
            normalized_comparative.index)

        if len(common_index) < max(length, rs_ma_length, price_sma_length):
            raise ValueError(
                f"Insufficient overlapping data points. Need at least {max(length, rs_ma_length, price_sma_length)} common dates")

        # Extract price series for common dates
        base_prices = normalized_base[base_column.lower()].loc[common_index]
        comparative_prices = normalized_comparative[comparative_column.lower(
        )].loc[common_index]

        # Calculate price ratios
        base_ratio = base_prices / base_prices.shift(length)
        comparative_ratio = comparative_prices / \
            comparative_prices.shift(length)

        # Calculate relative strength
        rs = base_ratio / comparative_ratio - 1
        rs = np.round(rs, 2)

        return pd.Series(
            rs,
            index=common_index,
            name='Relative Strength'
        )


def relative_strength(base_data: pd.DataFrame, comparative_data: pd.DataFrame,
                      length: int = 55, base_shift: int = 5, rs_ma_length: int = 50,
                      price_sma_length: int = 50, base_column: str = 'close',
                      comparative_column: str = 'close') -> pd.DataFrame:
    """
    Calculate Relative Strength between two securities (functional interface).

    :param base_data: DataFrame containing OHLCV data for the base security
    :param comparative_data: DataFrame containing OHLCV data for the comparative security
    :param length: Period for calculating price ratios (default: 55)
    :param base_shift: Base shift period (default: 5)
    :param rs_ma_length: Moving average length for RS smoothing (default: 50)
    :param price_sma_length: Moving average length for price smoothing (default: 50)
    :param base_column: Column to use from base data (default: 'close')
    :param comparative_column: Column to use from comparative data (default: 'close')
    :return: DataFrame with RS calculations and signals
    """
    indicator = RelativeStrength()
    return indicator.calculate(
        base_data, comparative_data, length, base_shift,
        rs_ma_length, price_sma_length, base_column, comparative_column
    )
