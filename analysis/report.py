from datetime import datetime, timezone
from pathlib import Path
from typing import Dict

import pandas as pd

from analysis.statistics import AnalysisStats


def generate_html_report(
    symbol_stats: Dict[str, AnalysisStats],
    plot_path: Path,
    output_path: Path,
) -> None:
    """Generate a self-contained static HTML report suitable for GitHub Pages."""
    rows = []
    for symbol, stats in symbol_stats.items():
        rows.append({
            "Symbol": symbol,
            "R²": f"{stats.r_squared:.4f}",
            "Annual Growth": f"{stats.annual_growth_rate * 100:.2f}%",
            "Current Deviation": f"{stats.current_deviation_pct:.2f}%",
            "Residual Percentile": f"{stats.current_residual_percentile:.1f}%",
            "Within 95% Interval": "Yes" if stats.is_current_within_interval else "No",
            "Max Drawdown": f"{stats.max_drawdown * 100:.2f}%",
            "Current Drawdown": f"{stats.current_drawdown_pct:.2f}%",
        })

    summary_table = pd.DataFrame(rows)
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Fund Analysis Dashboard</title>
<style>
:root {{ color-scheme: light dark; font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }}
body {{ max-width: 1200px; margin: 0 auto; padding: 32px 20px 64px; line-height: 1.5; }}
header {{ margin-bottom: 28px; }}
h1 {{ margin-bottom: 6px; }}
.meta {{ opacity: .7; font-size: .9rem; }}
.table-wrap {{ overflow-x: auto; }}
table {{ border-collapse: collapse; width: 100%; margin: 20px 0 32px; }}
th, td {{ border-bottom: 1px solid #8886; padding: 10px 12px; text-align: right; white-space: nowrap; }}
th:first-child, td:first-child {{ text-align: left; }}
th {{ font-weight: 650; }}
img {{ display: block; max-width: 100%; height: auto; margin: 0 auto; }}
.note {{ margin-top: 28px; opacity: .75; font-size: .9rem; }}
</style>
</head>
<body>
<header>
<h1>Fund Analysis Dashboard</h1>
<p>公開市場データを用いた長期トレンド分析です。</p>
<p class="meta">Assets: {', '.join(symbol_stats.keys())} · Updated: {generated_at}</p>
</header>
<main>
<section>
<h2>Summary</h2>
<div class="table-wrap">{summary_table.to_html(index=False, escape=True, border=0)}</div>
</section>
<section>
<h2>Long-term trend</h2>
<img src="{plot_path.name}" alt="Long-term fund analysis chart" />
</section>
<p class="note">This dashboard is for analysis and reference only and does not constitute investment advice.</p>
</main>
</body>
</html>
"""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")
