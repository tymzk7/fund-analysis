from pathlib import Path

import pandas as pd


def load_price_data(csv_path: Path) -> pd.DataFrame:
    """Load CSV data with Date and Price columns and return a clean DataFrame."""
    data = pd.read_csv(csv_path, parse_dates=["Date"])
    data = data[["Date", "Price"]].dropna().copy()
    data["Date"] = pd.to_datetime(data["Date"])
    data = data.sort_values("Date").reset_index(drop=True)
    return data
