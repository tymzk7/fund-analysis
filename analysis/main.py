from __future__ import annotations

import sys
from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import Dict, List, Tuple

PACKAGE_ROOT = Path(__file__).resolve().parent
if str(PACKAGE_ROOT.parent) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT.parent))

from analysis.config import DEFAULT_CSV_PATH, DEFAULT_PLOT_PATH, DEFAULT_REPORT_PATH, OUTPUT_DIR
from analysis.data_source import load_price_data
from analysis.plot import plot_assets_analysis
from analysis.regression import RegressionResult, fit_log_price_regression
from analysis.report import generate_html_report
from analysis.statistics import AnalysisStats, compute_analysis_stats


def parse_args() -> Namespace:
    parser = ArgumentParser(description="Asset analysis framework for CSV, Yahoo Finance, and MSCI data sources.")
    parser.add_argument("--source", choices=["csv", "yahoo", "msci"], default="csv", help="Data source type")
    parser.add_argument("--asset", action="append", help="Asset identifier. CSV path for csv/msci, ticker for yahoo. Repeat for multiple assets.")
    parser.add_argument("--start-date", default=None, help="Optional start date for price history in YYYY-MM-DD")
    parser.add_argument("--end-date", default=None, help="Optional end date for price history in YYYY-MM-DD")
    parser.add_argument("--period", default=None, help="Optional Yahoo Finance period string, e.g. 1mo, 6mo, 1y, 5y")
    parser.add_argument("--output-dir", default=str(OUTPUT_DIR), help="Directory to save charts and reports")
    parser.add_argument("--save-png", action="store_true", help="Save chart as PNG")
    parser.add_argument("--save-html", action="store_true", help="Save analysis report as HTML")
    parser.add_argument("--no-show", action="store_true", help="Do not open an interactive chart window")
    return parser.parse_args()


def build_asset_list(source: str, assets: List[str] | None) -> List[str]:
    if assets:
        return assets
    if source == "csv":
        return [str(DEFAULT_CSV_PATH)]
    raise ValueError("At least one asset identifier must be provided for yahoo or msci sources.")


def main(args: Namespace | None = None) -> None:
    if args is None:
        args = parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    asset_identifiers = build_asset_list(args.source, args.asset)
    asset_results: Dict[str, Tuple[object, RegressionResult, AnalysisStats]] = {}

    for asset_identifier in asset_identifiers:
        data = load_price_data(source=args.source, identifier=asset_identifier,
                               start_date=args.start_date, end_date=args.end_date, period=args.period)
        regression_result = fit_log_price_regression(data)
        stats = compute_analysis_stats(data, regression_result)
        asset_name = Path(asset_identifier).stem if args.source in {"csv", "msci"} else asset_identifier
        asset_results[asset_name] = (data, regression_result, stats)

    plot_path = output_dir / DEFAULT_PLOT_PATH.name if (args.save_png or args.save_html) else None
    plot_assets_analysis(asset_results, save_path=plot_path, show_moving_average=True,
                         show_bollinger=True, show=not args.no_show)

    if args.save_html:
        report_path = output_dir / DEFAULT_REPORT_PATH.name
        generate_html_report({name: stats for name, (_, _, stats) in asset_results.items()},
                             plot_path or DEFAULT_PLOT_PATH, report_path)


if __name__ == "__main__":
    main()
