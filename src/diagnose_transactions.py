
import pandas as pd
from pathlib import Path

base_dir = Path(__file__).resolve().parent.parent
file_path = base_dir / "data" / "cleaned_online_retail.csv"

df = pd.read_csv(file_path, dtype={"InvoiceNo": "string"})

df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
df["UnitPrice"] = pd.to_numeric(df["UnitPrice"], errors="coerce")
df["IsCancellation"] = df["InvoiceNo"].str.startswith("C", na=False)

# Categorize transaction lines
conditions = [
    df["IsCancellation"],
    df["Quantity"] < 0,
    df["Quantity"] > 0,
]

labels = [
    "Cancellation invoice",
    "Negative quantity, non-cancellation",
    "Positive quantity, non-cancellation",
]

df["TransactionType"] = pd.Series(
    pd.NA, index=df.index, dtype="string"
)

for condition, label in zip(conditions, labels):
    df.loc[condition & df["TransactionType"].isna(), "TransactionType"] = label

print("\n--- TRANSACTION TYPE COUNTS ---")
print(df["TransactionType"].value_counts(dropna=False))

print("\n--- NEGATIVE QUANTITY ANALYSIS ---")
print("Negative quantity rows:", (df["Quantity"] < 0).sum())
print("Cancellation invoice rows:", df["IsCancellation"].sum())
print(
    "Negative quantity with cancellation invoice:",
    ((df["Quantity"] < 0) & df["IsCancellation"]).sum()
)
print(
    "Negative quantity with positive price:",
    ((df["Quantity"] < 0) & (df["UnitPrice"] > 0)).sum()
)
print(
    "Negative quantity with zero/negative price:",
    ((df["Quantity"] < 0) & (df["UnitPrice"] <= 0)).sum()
)

print("\n--- PRICE QUALITY ---")
print("Zero price rows:", (df["UnitPrice"] == 0).sum())
print("Negative price rows:", (df["UnitPrice"] < 0).sum())
