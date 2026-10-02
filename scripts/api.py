import pandas as pd
from pathlib import Path
from fastapi import FastAPI

app = FastAPI(
    title="Automated BI Agent API",
    version="1.0.0"
)

DATA_FILE = Path("/app/data/OnlineRetail.csv")


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "python-bi-api"
    }


@app.get("/data-quality")
def data_quality():
    df = pd.read_csv(
        DATA_FILE,
        encoding="cp1252",
        parse_dates=["InvoiceDate"],
        dayfirst=True
    )

    return {
        "total_rows": len(df),
        "total_columns": len(df.columns),
        "quantity_non_positive": int((df["Quantity"] <= 0).sum()),
        "unit_price_non_positive": int((df["UnitPrice"] <= 0).sum()),
        "missing_customer_id": int(df["CustomerID"].isna().sum()),
        "missing_description": int(df["Description"].isna().sum()),
        "first_transaction": df["InvoiceDate"].min().isoformat(),
        "last_transaction": df["InvoiceDate"].max().isoformat()
    }