import pandas as pd
import numpy as np


def validate_series(series, name):
    """Validate pandas Series input."""
    if isinstance(series, np.ndarray):
        if series.ndim > 1:
            raise ValueError(f"{name} must be a 1-dimensional array")
        series = pd.Series(data=series, name=name)

    if not isinstance(series, (pd.Series, np.ndarray)):
        raise TypeError(f"{name} must be a pandas Series or numpy array")
    if series.empty:
        raise ValueError(f"{name} series cannot be empty")
    if not np.isfinite(series).all():
        raise ValueError(f"{name} series contains null or infinite values")

    return series
