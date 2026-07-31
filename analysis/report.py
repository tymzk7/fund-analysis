from pathlib import Path
from typing import Dict

import pandas as pd

from analysis.statistics import AnalysisStats


def generate_html_report(
    symbol_stats: Dict[str, AnalysisStats],
    plot_path: Path,
    output_path: Path,
) -> None:
    """Generate a simple HTML report for analysis results."""
    rows = []
    for symbol, stats in symbol_stats.items():
        rows.append(
            {
                "Symbol": symbol,
                "R²": f"{stats.r_squared:.4f}",
                "Slope/d": f"{stats.slope:.6f}",
                "Annual Growth": f"{stats.annual_growth_rate * 100:.2f}%",
                "Current Deviation": f"{stats.current_deviation_pct:.2f}%",
                "Residual Percentile": f"{stats.current_residual_percentile:.1f}%",
                "Within 95% Interval": "Yes" if stats.is_current_within_interval else "No",
                "Max Drawdown": f"{stats.max_drawdown * 100:.2f}%",
                "Current Drawdown": f"{stats.current_drawdown_pct:.2f}%",
            }
        )

    summary_table = pd.DataFrame(rows)
    html = f"""
<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8" />
<title>Asset Analysis Report</title>
<style>
body {{ font-family: Arial, sans-serif; margin: 24px; }}
table {{ border-collapse: collapse; width: 100%; margin-bottom: 24px; }}
th, td {{ border: 1px solid #ccc; padding: 8px; text-align: left; }}
th {{ background: #f8f8f8; }}
img {{ max-width: 100%; height: auto; }}
</style>
</head>
<body>
<h1>Analysis Report</h1>
<p>Generated analysis report for {', '.join(symbol_stats.keys())}.</p>
{summary_table.to_html(index=False, escape=False)}
<h2>Chart</h2>
<p><img src="{plot_path.name}" alt="Analysis chart" /></p>
</body>
</html>
"""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as handle:
        handle.write(html)
