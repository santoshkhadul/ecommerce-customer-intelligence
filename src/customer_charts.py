import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPORTS = ROOT / "reports"

customers = pd.read_csv(REPORTS / "customer_summary.csv")
segments = pd.read_csv(REPORTS / "customer_segment_summary.csv")


def save_customer_type_chart():
    customer_counts = customers["CustomerType"].value_counts()

    plt.figure(figsize=(8, 5))
    customer_counts.plot(kind="bar")
    plt.title("Repeat Customers vs One-Time Customers")
    plt.xlabel("Customer Type")
    plt.ylabel("Number of Customers")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(REPORTS / "customer_type_chart.png", dpi=150)
    plt.close()


def save_customer_segment_chart():
    segments = pd.read_csv(REPORTS / "customer_segment_summary.csv")
    segments = segments.sort_values("TotalSalesValue", ascending=True)

    plt.figure(figsize=(10, 6))
    plt.barh(segments["CustomerSegment"], segments["TotalSalesValue"])
    plt.title("Sales Value by Customer Segment")
    plt.xlabel("Total Sales Value")
    plt.ylabel("Customer Segment")
    plt.tight_layout()
    plt.savefig(REPORTS / "customer_segment_sales_chart.png", dpi=150)
    plt.close()


save_customer_type_chart()
save_customer_segment_chart()

print("Customer charts created successfully.")
print("Saved in:", REPORTS)
