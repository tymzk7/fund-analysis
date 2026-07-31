from dataclasses import dataclass
from typing import Dict

import numpy as np
import pandas as pd

from analysis.regression import RegressionResult


@dataclass
class AnalysisStats:
    r_squared: float
    slope: float
    annual_growth_rate: float
    current_deviation_pct: float
    current_residual_percentile: float
    is_current_within_interval: bool
    lower_bound: np.ndarray
    upper_bound: np.ndarray
    residuals: np.ndarray
    max_drawdown: float
    current_drawdown_pct: float


def compute_analysis_stats(data: pd.DataFrame, regression_result: RegressionResult) -> AnalysisStats:
    """Compute statistics from regression results and residuals."""
    residuals = regression_result.log_prices - regression_result.log_predictions
    lower_bound_log = regression_result.log_predictions + np.percentile(residuals, 2.5)
    upper_bound_log = regression_result.log_predictions + np.percentile(residuals, 97.5)

    lower_bound = np.exp(lower_bound_log)
    upper_bound = np.exp(upper_bound_log)

    current_price = data["Price"].iloc[-1]
    current_predicted_price = regression_result.price_predictions[-1]
    current_residual = residuals[-1]
    current_percentile = float(np.mean(residuals <= current_residual) * 100)
    within_interval = lower_bound[-1] <= current_price <= upper_bound[-1]

    drawdown = _compute_drawdown(data["Price"].to_numpy(dtype=float))
    max_drawdown = float(np.min(drawdown))
    current_drawdown_pct = float(drawdown[-1] * 100.0)

    annual_growth_rate = _compute_annual_growth_rate(regression_result.slope)

    return AnalysisStats(
        r_squared=regression_result.model.score(regression_result.days, regression_result.log_prices),
        slope=regression_result.slope,
        annual_growth_rate=annual_growth_rate,
        current_deviation_pct=(current_price / current_predicted_price - 1.0) * 100.0,
        current_residual_percentile=current_percentile,
        is_current_within_interval=within_interval,
        lower_bound=lower_bound,
        upper_bound=upper_bound,
        residuals=residuals,
        max_drawdown=max_drawdown,
        current_drawdown_pct=current_drawdown_pct,
    )


def _compute_annual_growth_rate(daily_slope: float) -> float:
    """Convert daily log-price slope into annual CAGR-like growth rate."""
    return float(np.exp(daily_slope * 365) - 1.0)


def _compute_drawdown(prices: np.ndarray) -> np.ndarray:
    """Compute drawdown series for a price array."""
    running_max = np.maximum.accumulate(prices)
    return prices / running_max - 1.0
