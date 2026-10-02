import pandas as pd
from pathlib import Path

# Project paths
PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_DIR / "data" / "OnlineRetail.csv"
REPORT_FILE = PROJECT_DIR / "reports" / "data_quality_report.txt"

print("Loading dataset...")

df = pd.read_csv(
    DATA_FILE,
    encoding="cp1252",
    parse_dates=["InvoiceDate"],
    dayfirst=True,
)

# Build the data quality report
report = f"""
=== DATA QUALITY REPORT ===

Total rows: {len(df):,}
Total columns: {len(df.columns)}

--- Missing values ---
{df.isna().sum().to_string()}

--- Business anomalies ---
Quantity <= 0: {(df['Quantity'] <= 0).sum():,}
UnitPrice <= 0: {(df['UnitPrice'] <= 0).sum():,}
Missing CustomerID: {df['CustomerID'].isna().sum():,}
Missing Description: {df['Description'].isna().sum():,}

--- Dataset period ---
First transaction: {df['InvoiceDate'].min()}
Last transaction: {df['InvoiceDate'].max()}

Data quality analysis completed.
"""

# Display the report
print(report)

# Save the report
REPORT_FILE.write_text(report, encoding="utf-8")

print(f"Report saved to: {REPORT_FILE}")