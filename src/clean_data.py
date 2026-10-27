
import pandas as pd
from pathlib import Path

# 1. Define project paths
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_FILE = BASE_DIR / "data" / "Online Retail.xlsx"
OUTPUT_FILE = BASE_DIR / "data" / "cleaned_online_retail.csv"

# 2. Extract data
print("Loading original dataset...")

df = pd.read_excel(RAW_FILE)

original_rows = len(df)

print(f"Original rows: {original_rows:,}")

# 3. Standardize column names
df.columns = df.columns.str.strip()

# 4. Remove exact duplicate rows
duplicate_count = int(df.duplicated().sum())

df = df.drop_duplicates().copy()

print(f"Exact duplicates removed: {duplicate_count:,}")

# 5. Standardize text columns
text_columns = ["InvoiceNo", "StockCode", "Description", "Country"]

for column in text_columns:
    df[column] = df[column].astype("string").str.strip()

# 6. Convert data types safely
df["InvoiceDate"] = pd.to_datetime(
    df["InvoiceDate"], errors="coerce"
)

df["Quantity"] = pd.to_numeric(
    df["Quantity"], errors="coerce"
)

df["UnitPrice"] = pd.to_numeric(
    df["UnitPrice"], errors="coerce"
)

df["CustomerID"] = pd.to_numeric(
    df["CustomerID"], errors="coerce"
)

# Convert valid customer IDs to nullable integers
df["CustomerID"] = df["CustomerID"].astype("Int64")

# 7. Handle missing descriptive fields
df["Description"] = df["Description"].fillna("Unknown product")

# 8. Create useful analytical columns
df["LineAmount"] = df["Quantity"] * df["UnitPrice"]

df["IsCancellation"] = (
    df["InvoiceNo"].str.startswith("C", na=False)
)

df["IsReturn"] = df["Quantity"] < 0

df["IsValidPrice"] = df["UnitPrice"] > 0

df["HasCustomerID"] = df["CustomerID"].notna()

# 9. Create data-quality flags
df["HasValidDate"] = df["InvoiceDate"].notna()

df["HasValidQuantity"] = df["Quantity"].notna()

df["HasValidPriceValue"] = df["UnitPrice"].notna()

df["HasValidInvoice"] = df["InvoiceNo"].notna()

# 10. Report data quality
print("\n--- DATA QUALITY REPORT ---")

print(f"Rows after deduplication: {len(df):,}")

print(
    "Missing customer IDs:",
    f"{df['CustomerID'].isna().sum():,}"
)

print(
    "Missing product descriptions:",
    f"{df['Description'].eq('Unknown product').sum():,}"
)

print(
    "Cancellation invoice lines:",
    f"{df['IsCancellation'].sum():,}"
)

print(
    "Negative quantity lines:",
    f"{df['IsReturn'].sum():,}"
)

print(
    "Zero or negative price lines:",
    f"{(~df['IsValidPrice']).sum():,}"
)

print(
    "Missing or invalid dates:",
    f"{(~df['HasValidDate']).sum():,}"
)

# 11. Save transformed data
df.to_csv(OUTPUT_FILE, index=False)

print("\n--- ETL COMPLETED ---")
print(f"Output file: {OUTPUT_FILE}")
print(f"Final rows: {len(df):,}")
print("Original Excel file was not modified.")
