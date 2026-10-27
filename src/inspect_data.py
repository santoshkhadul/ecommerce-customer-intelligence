import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FILE_PATH = ROOT / "data" / "Online Retail.xlsx"

df = pd.read_excel(FILE_PATH)

print("\n--- DATASET SHAPE ---")
print(df.shape)

print("\n--- COLUMN NAMES ---")
print(df.columns.tolist())

print("\n--- FIRST 5 ROWS ---")
print(df.head())

print("\n--- DATA TYPES ---")
print(df.dtypes)

print("\n--- MISSING VALUES ---")
print(df.isnull().sum())

print("\n--- DUPLICATE ROWS ---")
print(df.duplicated().sum())

print("\n--- DATE RANGE ---")
print(df["InvoiceDate"].min())
print(df["InvoiceDate"].max())

print("\n--- BASIC STATISTICS ---")
print(df.describe(include="all"))
