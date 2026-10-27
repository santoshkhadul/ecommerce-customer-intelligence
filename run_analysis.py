import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"

steps = [
    ("Inspect original dataset", "inspect_data.py"),
    ("Clean dataset", "clean_data.py"),
    ("Validate cleaned data", "validate_data.py"),
    ("Diagnose transactions", "diagnose_transactions.py"),
    ("Analyze sales", "sales_analysis.py"),
    ("Analyze customers", "customer_analysis.py"),
    ("Create customer charts", "customer_charts.py"),
    ("Create KPI summary", "kpi_summary.py"),
]

print("\nE-COMMERCE CUSTOMER INTELLIGENCE")
print("Starting Python analysis pipeline...\n")

for description, filename in steps:
    script = SRC / filename

    print(f"\n{'=' * 60}")
    print(f"STEP: {description}")
    print(f"FILE: {filename}")
    print("=" * 60)

    result = subprocess.run(
        [sys.executable, str(script)],
        cwd=ROOT,
    )

    if result.returncode != 0:
        print(f"\nPipeline stopped. Failed script: {filename}")
        sys.exit(result.returncode)

print("\n" + "=" * 60)
print("ALL PYTHON ANALYSIS STEPS COMPLETED")
print(f"Reports folder: {ROOT / 'reports'}")
print("=" * 60)
