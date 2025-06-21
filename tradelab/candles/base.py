# tradelab/candles/base.py
from abc import ABC, abstractmethod
import pandas as pd


class BaseCandle(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def calculate(self, data: pd.DataFrame) -> pd.DataFrame:
        return "Calculate method must be implemented by subclasses"

    def validate_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Validate input data and ensure required columns exist.

        :param data: Input DataFrame
        :return: Validated and normalized DataFrame
        """
        if not isinstance(data, pd.DataFrame):
            raise TypeError("Input must be a pandas DataFrame")

        # Normalize column names to lowercase
        normalized_data = data.copy()
        normalized_data.columns = normalized_data.columns.str.lower()

        required_columns = {'open', 'high', 'low', 'close', 'volume'}

        # Check for required columns
        if not required_columns.issubset(normalized_data.columns):
            missing_cols = required_columns - set(normalized_data.columns)
            raise ValueError(f"DataFrame must contain columns: {missing_cols}")

        return normalized_data

    def __repr__(self) -> str:
        """
        String representation of the candle.

        :return: Name of the candle
        """
        return f"{self.name} candle"
