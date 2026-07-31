from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression


@dataclass
class RegressionResult:
    model: LinearRegression
    dates: pd.Series
    days: np.ndarray
    log_prices: np.ndarray
    log_predictions: np.ndarray
    price_predictions: np.ndarray
    intercept: float
    slope: float


def fit_log_price_regression(data: pd.DataFrame) -> RegressionResult:
    """Fit linear regression on log(price) against elapsed days."""
    dates = data["Date"].copy()
    days = _compute_elapsed_days(dates)
    log_prices = np.log(data["Price"].to_numpy(dtype=float))

    model = LinearRegression()
    model.fit(days, log_prices)
    log_predictions = model.predict(days)
    price_predictions = np.exp(log_predictions)

    return RegressionResult(
        model=model,
        dates=dates,
        days=days,
        log_prices=log_prices,
        log_predictions=log_predictions,
        price_predictions=price_predictions,
        intercept=float(model.intercept_),
        slope=float(model.coef_[0]),
    )


def _compute_elapsed_days(dates: pd.Series) -> np.ndarray:
    """Convert dates to days elapsed from the first observation."""
    reference_date = dates.min()
    elapsed = dates.dt.floor("D") - reference_date.floor("D")
    return elapsed.dt.days.to_numpy().reshape(-1, 1)


def predict_price_from_days(days: np.ndarray, regression_result: RegressionResult) -> np.ndarray:
    """Compute price predictions from elapsed days using the fitted regression."""
    log_pred = regression_result.model.predict(days)
    return np.exp(log_pred)
