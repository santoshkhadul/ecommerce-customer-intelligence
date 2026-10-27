import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Project paths
ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "data" / "cleaned_online_retail.csv"
REPORTS_DIR = ROOT / "reports"
REPORTS_DIR.mkdir(exist_ok=True)

# Load cleaned data
df = pd.read_csv(DATA_FILE, parse_dates=["InvoiceDate"])

print("\n===== DATASET OVERVIEW =====")
print(f"Total rows: {len(df):,}")
print(f"Unique invoices: {df['InvoiceNo'].nunique():,}")
print(f"Unique products: {df['StockCode'].nunique():,}")
print(f"Unique countries: {df['Country'].nunique():,}")
print(f"Identified customers: {df['CustomerID'].nunique():,}")

# Select preliminary positive sales lines
sales = df[
    (~df["IsCancellation"].astype(bool))
    & (df["Quantity"] > 0)
    & (df["UnitPrice"] > 0)
].copy()

# Monthly sales
sales["YearMonth"] = sales["InvoiceDate"].dt.to_period("M").astype(str)

monthly = (
    sales.groupby("YearMonth", as_index=False)
    .agg(
        TotalSalesValue=("LineAmount", "sum"),
        InvoiceCount=("InvoiceNo", "nunique"),
    )
)

monthly["TotalSalesValue"] = monthly["TotalSalesValue"].round(2)
monthly.to_csv(REPORTS_DIR / "python_monthly_sales.csv", index=False)

# Chart
plt.figure(figsize=(12, 6))
plt.plot(
    monthly["YearMonth"],
    monthly["TotalSalesValue"],
    marker="o",
)
plt.title("Monthly Sales Value")
plt.xlabel("Month")
plt.ylabel("Sales Value")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(REPORTS_DIR / "monthly_sales_chart.png", dpi=150)
plt.close()

# Top 10 products
top_products = (
    sales.groupby(["StockCode", "Description"], as_index=False)
    .agg(
        TotalSalesValue=("LineAmount", "sum"),
        TotalQuantitySold=("Quantity", "sum"),
    )
    .sort_values("TotalSalesValue", ascending=False)
    .head(10)
)

top_products["TotalSalesValue"] = top_products["TotalSalesValue"].round(2)
top_products.to_csv(REPORTS_DIR / "python_top_products.csv", index=False)

# Country sales
country_sales = (
    sales.groupby("Country", as_index=False)
    .agg(
        TotalSalesValue=("LineAmount", "sum"),
        InvoiceCount=("InvoiceNo", "nunique"),
    )
    .sort_values("TotalSalesValue", ascending=False)
)

country_sales["TotalSalesValue"] = country_sales["TotalSalesValue"].round(2)
country_sales.to_csv(REPORTS_DIR / "python_country_sales.csv", index=False)

print("\n===== TOP 10 PRODUCTS =====")
print(top_products.to_string(index=False))

print("\n===== TOP 10 COUNTRIES =====")
print(country_sales.head(10).to_string(index=False))

print("\nAnalysis complete!")
print("Reports saved in:", REPORTS_DIR)
