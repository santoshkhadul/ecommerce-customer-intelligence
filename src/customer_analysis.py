import pandas as pd
from pathlib import Path

# Project paths
ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "data" / "cleaned_online_retail.csv"
REPORTS_DIR = ROOT / "reports"
REPORTS_DIR.mkdir(exist_ok=True)

# Load dataset
df = pd.read_csv(DATA_FILE, parse_dates=["InvoiceDate"])

# Keep preliminary positive sales lines and customers with an ID
sales = df[
    (~df["IsCancellation"].astype(bool))
    & (df["Quantity"] > 0)
    & (df["UnitPrice"] > 0)
    & (df["CustomerID"].notna())
].copy()

# Create customer-level sales metrics
customer_summary = (
    sales.groupby("CustomerID", as_index=False)
    .agg(
        TotalSalesValue=("LineAmount", "sum"),
        InvoiceCount=("InvoiceNo", "nunique"),
        TotalItemsPurchased=("Quantity", "sum"),
        LastPurchaseDate=("InvoiceDate", "max"),
        FirstPurchaseDate=("InvoiceDate", "min"),
    )
)

customer_summary["TotalSalesValue"] = customer_summary["TotalSalesValue"].round(2)

# Identify repeat and one-time customers
customer_summary["CustomerType"] = customer_summary["InvoiceCount"].apply(
    lambda count: "Repeat Customer" if count > 1 else "One-Time Customer"
)

customer_summary.to_csv(
    REPORTS_DIR / "customer_summary.csv",
    index=False
)

# RFM analysis
# Use the day after the latest dataset date as the reference date
reference_date = sales["InvoiceDate"].max().normalize() + pd.Timedelta(days=1)

rfm = (
    sales.groupby("CustomerID")
    .agg(
        Recency=("InvoiceDate", lambda dates: (reference_date - dates.max().normalize()).days),
        Frequency=("InvoiceNo", "nunique"),
        Monetary=("LineAmount", "sum"),
    )
    .reset_index()
)

# Score each metric from 1 to 5
# Higher recency score means a more recent purchase
rfm["R_Score"] = pd.qcut(
    rfm["Recency"].rank(method="first", ascending=False),
    5,
    labels=[1, 2, 3, 4, 5],
).astype(int)

rfm["F_Score"] = pd.qcut(
    rfm["Frequency"].rank(method="first"),
    5,
    labels=[1, 2, 3, 4, 5],
).astype(int)

rfm["M_Score"] = pd.qcut(
    rfm["Monetary"].rank(method="first"),
    5,
    labels=[1, 2, 3, 4, 5],
).astype(int)

rfm["RFM_Score"] = (
    rfm["R_Score"].astype(str)
    + rfm["F_Score"].astype(str)
    + rfm["M_Score"].astype(str)
)

# Simple customer segments
def assign_segment(row):
    if row["R_Score"] >= 4 and row["F_Score"] >= 4 and row["M_Score"] >= 4:
        return "High-Value Active"
    elif row["R_Score"] >= 3 and row["F_Score"] >= 3:
        return "Loyal / Active"
    elif row["R_Score"] <= 2:
        return "At-Risk / Inactive"
    else:
        return "Other Customers"

rfm["CustomerSegment"] = rfm.apply(assign_segment, axis=1)
rfm["Monetary"] = rfm["Monetary"].round(2)

rfm.to_csv(REPORTS_DIR / "customer_rfm_analysis.csv", index=False)

# Summary results
repeat_counts = customer_summary["CustomerType"].value_counts()
segment_summary = (
    rfm.groupby("CustomerSegment", as_index=False)
    .agg(
        CustomerCount=("CustomerID", "count"),
        TotalSalesValue=("Monetary", "sum"),
    )
    .sort_values("TotalSalesValue", ascending=False)
)
segment_summary["TotalSalesValue"] = segment_summary["TotalSalesValue"].round(2)
segment_summary.to_csv(REPORTS_DIR / "customer_segment_summary.csv", index=False)

print("\n===== CUSTOMER ANALYSIS =====")
print(f"Customers analyzed: {len(customer_summary):,}")
print(f"Repeat customers: {(customer_summary['CustomerType'] == 'Repeat Customer').sum():,}")
print(f"One-time customers: {(customer_summary['CustomerType'] == 'One-Time Customer').sum():,}")

print("\n===== TOP 10 CUSTOMERS BY SALES VALUE =====")
print(
    customer_summary.sort_values("TotalSalesValue", ascending=False)
    .head(10)
    .to_string(index=False)
)

print("\n===== RFM CUSTOMER SEGMENTS =====")
print(segment_summary.to_string(index=False))

print("\nCustomer analysis complete!")
print("Reports saved in:", REPORTS_DIR)
