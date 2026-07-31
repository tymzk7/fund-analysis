from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_CSV_PATH = BASE_DIR / "data" / "sample.csv"
OUTPUT_DIR = BASE_DIR / "outputs"
DEFAULT_PLOT_PATH = OUTPUT_DIR / "analysis_chart.png"
DEFAULT_REPORT_PATH = OUTPUT_DIR / "analysis_report.html"
