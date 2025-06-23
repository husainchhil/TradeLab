"""Base class for all technical indicators."""

from abc import ABC, abstractmethod
import pandas as pd
from typing import Union, Dict, Any


class BaseIndicator(ABC):
    """
    Abstract base class for all technical indicators.

    This class provides a common interface and validation methods
    for all technical indicators in the package.
    """

    def __init__(self, name: str):
        """
        Initialize the base indicator.

        :param name: Name of the indicator
        """
        self.name = name

    @abstractmethod
    def calculate(self, data: pd.DataFrame, **kwargs) -> Union[pd.DataFrame, pd.Series]:
        """
        Calculate the indicator values.

        :param data: OHLCV DataFrame
        :param kwargs: Additional parameters specific to the indicator
        :return: Calculated indicator values
        """
        pass

    def validate_data(self, data: pd.DataFrame, required_columns: set) -> pd.DataFrame:
        """
        Validate input data and ensure required columns exist.

        :param data: Input DataFrame
        :param required_columns: Set of required column names
        :return: Validated and normalized DataFrame
        """
        if not isinstance(data, pd.DataFrame):
            raise TypeError("Input must be a pandas DataFrame")

        # Normalize column names to lowercase
        normalized_data = data.copy()
        normalized_data.columns = normalized_data.columns.str.lower()

        # Check for required columns
        if not required_columns.issubset(normalized_data.columns):
            missing_cols = required_columns - set(normalized_data.columns)
            raise ValueError(f"DataFrame must contain columns: {missing_cols}")

        return normalized_data

    def validate_hlc(self, high: pd.Series, low: pd.Series, close: pd.Series) -> None:
        """
        Validate the input data for SuperTrend calculation.

        :param high: High prices (Series).
        :param low: Low prices (Series).
        :param close: Close prices (Series).
        :raises ValueError: If the input data is not valid.
        """
        if not isinstance(high, pd.Series) or not isinstance(low, pd.Series) or not isinstance(close, pd.Series):
            raise ValueError("High, low, and close must be pandas Series.")
        if len(high) != len(low) or len(low) != len(close):
            raise ValueError("High, low, and close must have the same length.")

    def validate_period(self, period: int, min_value: int = 1) -> None:
        """
        Validate period parameter.

        :param period: Period value to validate
        :param min_value: Minimum allowed value
        """
        if not isinstance(period, int) or period < min_value:
            raise ValueError(f"Period must be an integer >= {min_value}")

    def validate_multiplier(self, multiplier: Union[int, float], min_value: float = 0) -> None:
        """
        Validate multiplier parameter.

        :param multiplier: Multiplier value to validate
        :param min_value: Minimum allowed value
        """
        if not isinstance(multiplier, (int, float)) or multiplier <= min_value:
            raise ValueError(f"Multiplier must be a number > {min_value}")
            
    def __repr__(self) -> str:
        """
        String representation of the indicator.

        :return: Name of the indicator
        """
        return f"{self.name} Indicator"