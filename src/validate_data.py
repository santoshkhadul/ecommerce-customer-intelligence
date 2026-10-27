
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = BASE_DIR / "data" / "cleaned_online_retail.csv"
OUTPUT_FILE = BASE_DIR / "reports" / "sales_summary.csv"

# Load cleaned data
df = pd.read_csv(
    INPUT_FILE,
    dtype={"InvoiceNo": "string", "StockCode": "string"}
)

# Convert numeric columns
df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
df["UnitPrice"] = pd.to_numeric(df["UnitPrice"], errors="coerce")
df["LineAmount"] = df["Quantity"] * df["UnitPrice"]

# Identify transaction types
df["IsCancellation"] = df["InvoiceNo"].str.startswith(
    "C", na=False
)

valid_price = df["UnitPrice"] > 0
positive_quantity = df["Quantity"] > 0
negative_quantity = df["Quantity"] < 0

# Positive sales lines, excluding cancellation invoices
sales_mask = (
    ~df["IsCancellation"]
    & positive_quantity
    & valid_price
)

# Negative-quantity lines not marked as cancellations
negative_non_cancellation_mask = (
    ~df["IsCancellation"]
    & negative_quantity
    & valid_price
)

sales = df.loc[sales_mask].copy()
negative_lines = df.loc[negative_non_cancellation_mask].copy()
cancellations = df.loc[df["IsCancellation"]].copy()

# Calculate preliminary KPIs
summary = {
    "Metric": [
        "Total cleaned rows",
        "Unique invoices including cancellations",
        "Unique identified customers",
        "Positive sales line count",
        "Positive sales invoice count",
        "Positive sales value",
        "Negative-quantity non-cancellation line count",
        "Negative-quantity line value (absolute)",
        "Cancellation line count",
        "Cancellation signed value",
        "Distinct products",
        "Distinct countries",
    ],
    "Value": [
        len(df),
        df["InvoiceNo"].nunique(),
        df["CustomerID"].nunique(),
        len(sales),
        sales["InvoiceNo"].nunique(),
        sales["LineAmount"].sum(),
        len(negative_lines),
        negative_lines["LineAmount"].abs().sum(),
        len(cancellations),
        cancellations["LineAmount"].sum(),
        df["StockCode"].nunique(),
        df["Country"].nunique(),
    ],
}

summary_df = pd.DataFrame(summary)

# Display results
print("\n--- PRELIMINARY BUSINESS KPI REPORT ---")
print(summary_df.to_string(index=False))

# Save results
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
summary_df.to_csv(OUTPUT_FILE, index=False)

print(f"\nReport saved to: {OUTPUT_FILE}")
print("\nNote: These are preliminary operational metrics.")
print("They are not yet final accounting net revenue or profit.")
