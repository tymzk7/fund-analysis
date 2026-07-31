from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Optional

import pandas as pd
import yfinance as yf

from analysis.loader import load_price_data as load_csv_price_data


def load_price_data(
    source: str,
    identifier: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    period: Optional[str] = None,
) -> pd.DataFrame:
    """Load price data from CSV, Yahoo Finance, or MSCI-compatible CSV."""
    if source == "csv":
        data = load_csv_price_data(Path(identifier))
    elif source == "yahoo":
        data = load_yahoo_data(identifier, start_date, end_date, period)
    elif source == "msci":
        data = load_msci_data(Path(identifier))
    else:
        raise ValueError(f"Unknown source: {source}")

    return _filter_date_range(data, start_date, end_date)


def load_yahoo_data(
    ticker: str,
    start_date: Optional[str],
    end_date: Optional[str],
    period: Optional[str],
) -> pd.DataFrame:
    """Download historical price data for a ticker from Yahoo Finance."""
    download_kwargs = {"auto_adjust": True, "progress": False}
    if start_date is not None or end_date is not None:
        download_kwargs["start"] = start_date
        download_kwargs["end"] = end_date
    elif period is not None:
        download_kwargs["period"] = period

    raw = yf.download(ticker, **download_kwargs)
    if raw.empty:
        raise ValueError(f"No data found for ticker: {ticker}")

    if "Close" in raw.columns:
        price_series = raw["Close"]
    elif "Adj Close" in raw.columns:
        price_series = raw["Adj Close"]
    else:
        raise ValueError("Yahoo Finance data does not contain a price column.")

    if isinstance(price_series, pd.DataFrame):
        price_series = price_series.iloc[:, 0]

    data = price_series.reset_index()
    data.columns = ["Date", "Price"]
    data["Date"] = pd.to_datetime(data["Date"])
    data = data.sort_values("Date").reset_index(drop=True)
    return data


def load_msci_data(csv_path: Path) -> pd.DataFrame:
    """Load MSCI-style CSV data. Assumes Date and Price / Close columns exist."""
    data = pd.read_csv(csv_path, parse_dates=["Date"])
    if "Price" not in data.columns and "Close" in data.columns:
        data = data.rename(columns={"Close": "Price"})
    data = data[["Date", "Price"]].dropna().copy()
    data["Date"] = pd.to_datetime(data["Date"])
    data = data.sort_values("Date").reset_index(drop=True)
    return data


def _filter_date_range(data: pd.DataFrame, start_date: Optional[str], end_date: Optional[str]) -> pd.DataFrame:
    """Filter loaded data by optional start and end dates."""
    if start_date is not None:
        data = data[data["Date"] >= pd.to_datetime(start_date)]
    if end_date is not None:
        data = data[data["Date"] <= pd.to_datetime(end_date)]
    if data.empty:
        raise ValueError("No data available in the requested date range.")
    return data
