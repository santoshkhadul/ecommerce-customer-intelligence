import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "data" / "cleaned_online_retail.csv"
REPORTS = ROOT / "reports"

df = pd.read_csv(DATA_FILE, parse_dates=["InvoiceDate"])
customers = pd.read_csv(REPORTS / "customer_summary.csv")
segments = pd.read_csv(REPORTS / "customer_segment_summary.csv")

sales = df[
    (~df["IsCancellation"].astype(bool))
    & (df["Quantity"] > 0)
    & (df["UnitPrice"] > 0)
].copy()

total_sales = sales["LineAmount"].sum()
total_invoices = sales["InvoiceNo"].nunique()
identified_customers = customers["CustomerID"].nunique()
repeat_customers = (customers["CustomerType"] == "Repeat Customer").sum()
one_time_customers = (customers["CustomerType"] == "One-Time Customer").sum()

repeat_rate = (
    repeat_customers / len(customers) * 100
    if len(customers) else 0
)

average_order_value = (
    total_sales / total_invoices
    if total_invoices else 0
)

kpis = pd.DataFrame([
    {"Metric": "Total Sales Value", "Value": round(total_sales, 2)},
    {"Metric": "Unique Invoices", "Value": total_invoices},
    {"Metric": "Identified Customers", "Value": identified_customers},
    {"Metric": "Repeat Customers", "Value": repeat_customers},
    {"Metric": "One-Time Customers", "Value": one_time_customers},
    {"Metric": "Repeat Customer Rate (%)", "Value": round(repeat_rate, 2)},
    {"Metric": "Average Order Value", "Value": round(average_order_value, 2)},
])

kpis.to_csv(REPORTS / "executive_kpi_summary.csv", index=False)

print("\n===== EXECUTIVE KPI SUMMARY =====")
print(kpis.to_string(index=False))

print("\n===== CUSTOMER SEGMENT SUMMARY =====")
print(segments.to_string(index=False))

print("\nKPI summary saved to reports/executive_kpi_summary.csv")
