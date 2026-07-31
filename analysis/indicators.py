import numpy as np
import pandas as pd


def compute_moving_average(prices: pd.Series, window: int = 50) -> pd.Series:
    """Return a simple moving average series for the given window."""
    return prices.rolling(window=window, min_periods=1).mean()


def compute_bollinger_bands(
    prices: pd.Series,
    window: int = 20,
    num_std: float = 2.0,
) -> tuple[pd.Series, pd.Series, pd.Series]:
    """Return middle, upper, and lower Bollinger bands for price series."""
    rolling_mean = prices.rolling(window=window, min_periods=1).mean()
    rolling_std = prices.rolling(window=window, min_periods=1).std(ddof=0)
    upper_band = rolling_mean + num_std * rolling_std
    lower_band = rolling_mean - num_std * rolling_std
    return rolling_mean, upper_band, lower_band


def compute_drawdown(prices: pd.Series) -> pd.Series:
    """Return the drawdown series from peak to trough."""
    running_max = prices.cummax()
    return prices / running_max - 1.0
