from .base import BaseCandle
import numpy as np
import pandas as pd

_MODE_dict = ['normal', 'wicks', 'nongap', 'reverse-wicks',
              'reverse-nongap', 'fake-r-wicks', 'fake-r-nongap']


class Renko(BaseCandle):
    def __init__(self, df: pd.DataFrame, brick_size: float):
        """
        Renko candle class.
        :param df: DataFrame containing OHLCV data with columns 'datetime' and 'close'.
        :param brick_size: Size of each Renko brick.
        """

        super().__init__("Renko")

        df = self.validate_data(df)

        if brick_size is None or brick_size <= 0:
            raise ValueError("brick_size cannot be 'None' or '<= 0'")
        if 'datetime' not in df.columns:
            df["datetime"] = df.index
        if 'close' not in df.columns:
            raise ValueError("Column 'close' doesn't exist!")

        self._brick_size = brick_size
        self._df_len = len(df["close"])

        first_close = df["close"].iat[0]
        initial_price = (first_close // brick_size) * brick_size
        # Renko Single Data
        self._rsd = {
            "origin_index": [0],
            "date": [df["datetime"].iat[0]],
            "price": [initial_price],
            "direction": [0],
            "wick": [initial_price],
            "volume": [1],
        }

        self._wick_min_i = initial_price
        self._wick_max_i = initial_price
        self._volume_i = 1

        for i in range(1, self._df_len):
            self._add_prices(i, df)

    def _add_prices(self, i, df):

        df_close = df["close"].iat[i]
        self._wick_min_i = df_close if df_close < self._wick_min_i else self._wick_min_i
        self._wick_max_i = df_close if df_close > self._wick_max_i else self._wick_max_i
        self._volume_i += 1

        last_price = self._rsd["price"][-1]
        current_n_bricks = (df_close - last_price) / self._brick_size
        current_direction = np.sign(current_n_bricks)
        if current_direction == 0:
            return
        last_direction = self._rsd["direction"][-1]
        is_same_direction = ((current_direction > 0 and last_direction >= 0)
                             or (current_direction < 0 and last_direction <= 0))

        total_same_bricks = current_n_bricks if is_same_direction else 0
        if not is_same_direction and abs(current_n_bricks) >= 2:
            self._add_brink_loop(df, i, 2, current_direction, current_n_bricks)
            total_same_bricks = current_n_bricks - 2 * current_direction

        # Add all bricks in the same direction
        for not_in_use in range(abs(int(total_same_bricks))):
            self._add_brink_loop(df, i, 1, current_direction, current_n_bricks)

    def _add_brink_loop(self, df, i, renko_multiply, current_direction, current_n_bricks):
        last_price = self._rsd["price"][-1]
        renko_price = last_price + \
            (current_direction * renko_multiply * self._brick_size)
        wick = self._wick_min_i if current_n_bricks > 0 else self._wick_max_i

        to_add = [i, df["datetime"].iat[i], renko_price,
                  current_direction, wick, self._volume_i]
        for name, add in zip(list(self._rsd.keys()), to_add):
            self._rsd[name].append(add)

        self._volume_i = 1
        self._wick_min_i = renko_price if current_n_bricks > 0 else self._wick_min_i
        self._wick_max_i = renko_price if current_n_bricks < 0 else self._wick_max_i

    def calculate(self, mode: str = "normal") -> pd.DataFrame:
        """
        Calculate the Renko DataFrame.
        :param mode: Mode for calculating Renko bricks.
        :return: DataFrame with Renko candles.
        """
        if mode not in _MODE_dict:
            raise ValueError(f"Only {_MODE_dict} options are valid.")

        dates = self._rsd["date"]
        prices = self._rsd["price"]
        directions = self._rsd["direction"]
        wicks = self._rsd["wick"]
        volumes = self._rsd["volume"]
        indexes = list(range(len(prices)))
        brick_size = self._brick_size

        df_dict = {
            "datetime": [],
            "open": [],
            "high": [],
            "low": [],
            "close": [],
            "volume": [],
        }

        reverse_rule = mode in ["normal", "wicks",
                                "reverse-wicks", "fake-r-wicks"]
        fake_reverse_rule = mode in ["fake-r-nongap", "fake-r-wicks"]
        same_direction_rule = mode in ["wicks", "nongap"]

        prev_direction = 0
        prev_close = 0
        prev_close_up = 0
        prev_close_down = 0
        for price, direction, date, wick, volume, index in zip(prices, directions, dates, wicks, volumes, indexes):
            if direction != 0:
                df_dict["datetime"].append(date)
                df_dict["close"].append(price)
                df_dict["volume"].append(volume)

            # Current Renko (UP)
            if direction == 1.0:
                df_dict["high"].append(price)
                # Previous same direction(UP)
                if prev_direction == 1:
                    df_dict["open"].append(
                        wick if mode == "nongap" else prev_close_up)
                    df_dict["low"].append(
                        wick if same_direction_rule else prev_close_up)
                # Previous reverse direction(DOWN)
                else:
                    if reverse_rule:
                        df_dict["open"].append(prev_close + brick_size)
                    elif mode == "fake-r-nongap":
                        df_dict["open"].append(prev_close_down)
                    else:
                        df_dict["open"].append(wick)

                    if mode == "normal":
                        df_dict["low"].append(prev_close + brick_size)
                    elif fake_reverse_rule:
                        df_dict["low"].append(prev_close_down)
                    else:
                        df_dict["low"].append(wick)
                prev_close_up = price
            # Current Renko (DOWN)
            elif direction == -1.0:
                df_dict["low"].append(price)
                # Previous same direction(DOWN)
                if prev_direction == -1:
                    df_dict["open"].append(
                        wick if mode == "nongap" else prev_close_down)
                    df_dict["high"].append(
                        wick if same_direction_rule else prev_close_down)
                # Previous reverse direction(UP)
                else:
                    if reverse_rule:
                        df_dict["open"].append(prev_close - brick_size)
                    elif mode == "fake-r-nongap":
                        df_dict["open"].append(prev_close_up)
                    else:
                        df_dict["open"].append(wick)

                    if mode == "normal":
                        df_dict["high"].append(prev_close - brick_size)
                    elif fake_reverse_rule:
                        df_dict["high"].append(prev_close_up)
                    else:
                        df_dict["high"].append(wick)
                prev_close_down = price
            # BEGIN OF DICT
            else:
                df_dict["datetime"].append(np.nan)
                df_dict["low"].append(np.nan)
                df_dict["close"].append(np.nan)
                df_dict["high"].append(np.nan)
                df_dict["open"].append(np.nan)
                df_dict["volume"].append(np.nan)

            prev_direction = direction
            prev_close = price

        df = pd.DataFrame(df_dict)
        # Removing the first 2 lines of DataFrame that are the beginning of respective loops (df_dict and self._rsd)
        df.drop(df.head(2).index, inplace=True)
        # Setting Index
        df.index = pd.DatetimeIndex(df["datetime"])
        df.drop(columns=['datetime'], inplace=True)
        df['Trend'] = np.where(
            df['close'] > df['open'], 1, -1)
        df.columns = df.columns.str.capitalize()

        return df


def renko(df: pd.DataFrame, brick_size: float, mode: str = "wicks") -> pd.DataFrame:
    """
    Calculate Renko candles (functional interface).

    :param df: DataFrame containing OHLCV data with columns 'datetime' and 'close'.
    :param brick_size: Size of each Renko brick.
    :param mode: Mode for calculating Renko bricks.
    :return: DataFrame with Renko candles.
    """
    renko = Renko(df, brick_size)
    return renko.calculate(mode)
