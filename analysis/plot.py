from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from analysis.indicators import compute_bollinger_bands, compute_moving_average
from analysis.regression import RegressionResult
from analysis.statistics import AnalysisStats


def plot_price_with_regression(
    data: pd.DataFrame,
    regression_result: RegressionResult,
    stats: AnalysisStats,
    save_path: Path | None = None,
) -> None:
    plot_assets_analysis({"Asset": (data, regression_result, stats)}, save_path=save_path)


def plot_assets_analysis(
    asset_results: dict[str, tuple[pd.DataFrame, RegressionResult, AnalysisStats]],
    show_moving_average: bool = False,
    show_bollinger: bool = False,
    save_path: Path | None = None,
) -> None:
    """Plot one or more assets with regression and optional technical indicators."""
    fig, ax = plt.subplots(figsize=(14, 8))
    colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]

    for index, (label, (data, regression_result, stats)) in enumerate(asset_results.items()):
        color = colors[index % len(colors)]
        ax.plot(data["Date"], data["Price"], label=f"{label} Price", color=color, linewidth=1.5)
        ax.plot(
            data["Date"],
            regression_result.price_predictions,
            label=f"{label} Regression",
            color=color,
            linestyle="--",
            linewidth=1.2,
        )
        ax.fill_between(
            data["Date"],
            stats.lower_bound,
            stats.upper_bound,
            color=color,
            alpha=0.15,
            label=f"{label} 95% Interval",
        )

        if show_moving_average:
            moving_average = compute_moving_average(data["Price"], window=50)
            ax.plot(data["Date"], moving_average, label=f"{label} 50-day MA", linestyle=":", color=color)

        if show_bollinger:
            middle, upper, lower = compute_bollinger_bands(data["Price"], window=20)
            ax.plot(data["Date"], middle, label=f"{label} BB Mid", color=color, linewidth=0.8)
            ax.plot(data["Date"], upper, label=f"{label} BB Upper", color=color, linewidth=0.6, alpha=0.7)
            ax.plot(data["Date"], lower, label=f"{label} BB Lower", color=color, linewidth=0.6, alpha=0.7)

    ax.set_yscale("log")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.set_title("Long-Term Trend Analysis with Log-Linear Regression")
    ax.legend(loc="upper left", fontsize=8)
    ax.grid(True, which="both", linestyle="--", linewidth=0.4, alpha=0.7)

    _annotate_statistics(ax, asset_results)

    fig.tight_layout()

    if save_path is not None:
        save_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=150)
    plt.show()


def _annotate_statistics(ax: plt.Axes, asset_results: dict[str, tuple[pd.DataFrame, RegressionResult, AnalysisStats]]) -> None:
    """Add a summary statistics box to the plot."""
    lines: list[str] = []
    for label, (_, _, stats) in asset_results.items():
        lines.append(
            f"[{label}] R²={stats.r_squared:.4f}, CAGR={stats.annual_growth_rate*100:.2f}%",
        )
        lines.append(
            f"     Dev={stats.current_deviation_pct:.2f}%, Pctl={stats.current_residual_percentile:.1f}%, "
            f"Drawdown={stats.current_drawdown_pct:.2f}%"
        )
    annotation = "\n".join(lines)

    ax.text(
        0.01,
        0.99,
        annotation,
        transform=ax.transAxes,
        fontsize=9,
        verticalalignment="top",
        bbox={"boxstyle": "round", "facecolor": "white", "alpha": 0.85, "edgecolor": "gray"},
    )
