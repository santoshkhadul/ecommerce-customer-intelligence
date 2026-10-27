
# PostgreSQL Setup Guide

This guide explains how to set up PostgreSQL for the E-Commerce Customer Intelligence & Revenue Analytics project.

## 1. Project Overview

This project analyzes online retail transactions using Python, SQL, and PostgreSQL.

It includes:
- Data inspection and cleaning with Python
- Sales and revenue analysis
- Customer segmentation and RFM analysis
- Monthly sales and country analysis
- PostgreSQL star-schema data modeling
- CSV reports and charts

Power BI is optional. The core project works with Python and PostgreSQL.

## 2. Prerequisites

Install the following:

- Python 3.10 or a compatible version
- PostgreSQL
- PostgreSQL command-line tools (`psql`)
- Git (optional)

Download the Online Retail dataset from the UCI Machine Learning Repository:

https://archive.ics.uci.edu/dataset/352/online+retail

Place the downloaded Excel file in the project's `data` folder:

`data/Online Retail.xlsx`

Your project directory should contain:

```text
ecommerce-customer-intelligence/
├── data/
│   └── Online Retail.xlsx
├── reports/
├── sql/
│   ├── create_star_schema.sql
│   ├── create_staging_table.sql
│   ├── load_star_schema.sql
│   ├── monthly_sales_analysis.sql
│   ├── country_sales_analysis.sql
│   ├── top_products.sql
│   └── top_customers.sql
├── src/
├── requirements.txt
├── run_analysis.py
└── POSTGRESQL_SETUP.md
```

## 3. Open the Project Folder

Open PowerShell in the project root directory.

Example:

```powershell
cd "$HOME\OneDrive\Desktop\aksh\ecommerce-customer-intelligence"
```

Use your actual project path if it is different.

## 4. Create a Python Virtual Environment

Create the virtual environment:

```powershell
python -m venv venv
```

Activate it:

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell says script execution is disabled, use this command for the current terminal session:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate the environment again:

```powershell
.\venv\Scripts\Activate.ps1
```

## 5. Install Python Dependencies

Install the required packages:

```powershell
python -m pip install -r requirements.txt
```

## 6. Run the Python Analysis

Run the main analysis pipeline:

```powershell
python run_analysis.py
```

The pipeline performs data inspection, cleaning, validation, sales analysis, customer analysis, chart creation, and KPI reporting.

The cleaned dataset is expected at:

`data/cleaned_online_retail.csv`

Generated reports are saved in the `reports` directory.

Important: Running the Python pipeline does not automatically create or populate PostgreSQL tables.

## 7. Create the PostgreSQL Database

Make sure the PostgreSQL service is running.

Create the project database:

```powershell
psql -U postgres -c "CREATE DATABASE ecommerce_analytics;"
```

Enter your PostgreSQL password if prompted.

If the database already exists, do not create it again. For a new setup, use a fresh database so the initial loading process starts cleanly.

## 8. Create the Star-Schema Tables

Run:

```powershell
psql -v ON_ERROR_STOP=1 -U postgres -d ecommerce_analytics -f sql/create_star_schema.sql
```

This creates the following tables:

- `dim_customer`
- `dim_product`
- `dim_country`
- `dim_date`
- `fact_sales`

## 9. Create the Staging Table

Run:

```powershell
psql -v ON_ERROR_STOP=1 -U postgres -d ecommerce_analytics -f sql/create_staging_table.sql
```

The `staging_retail` table stores the cleaned transaction data before it is loaded into the star schema.

## 10. Import the Cleaned CSV

First, ensure the Python pipeline has generated:

`data/cleaned_online_retail.csv`

Open PostgreSQL:

```powershell
psql -U postgres -d ecommerce_analytics
```

At the PostgreSQL prompt, run the following command.

Replace the example path with the full path to your own project:

```sql
\copy staging_retail FROM 'C:/FULL/PATH/TO/ecommerce-customer-intelligence/data/cleaned_online_retail.csv' WITH (FORMAT csv, HEADER true);
```

For example, if your project is located at:

`C:\Users\HP\OneDrive\Desktop\aksh\ecommerce-customer-intelligence`

the command would be:

```sql
\copy staging_retail FROM 'C:/Users/HP/OneDrive/Desktop/aksh/ecommerce-customer-intelligence/data/cleaned_online_retail.csv' WITH (FORMAT csv, HEADER true);
```

Exit PostgreSQL:

```sql
\q
```

Important:
- Run the CSV import only once for the initial setup.
- Importing the same CSV again will duplicate staging records.
- The path must point to the actual CSV file.
- Do not run the import if the staging table already contains the dataset.

## 11. Load the Star Schema

Important: This is the initial load step for a fresh database.

Run:

```powershell
psql -v ON_ERROR_STOP=1 -U postgres -d ecommerce_analytics -f sql/load_star_schema.sql
```

The loading script populates:

- `dim_customer` from customer IDs
- `dim_product` from product codes and descriptions
- `dim_country` from country names
- `dim_date` from invoice dates
- `fact_sales` from transaction line items

The script checks whether `fact_sales` already contains data and stops if it is populated. This prevents accidental duplicate fact loading.

Do not run this loading script against a database that already has rows in `fact_sales`.

## 12. Verify the Database

Connect to the database:

```powershell
psql -U postgres -d ecommerce_analytics
```

Run these queries:

```sql
SELECT COUNT(*) AS staging_rows FROM staging_retail;

SELECT COUNT(*) AS customer_count FROM dim_customer;

SELECT COUNT(*) AS product_count FROM dim_product;

SELECT COUNT(*) AS country_count FROM dim_country;

SELECT COUNT(*) AS date_count FROM dim_date;

SELECT COUNT(*) AS sales_fact_rows FROM fact_sales;
```

For the supplied cleaned dataset, expected counts are approximately:

| Table | Expected rows |
|---|---:|
| staging_retail | 536641 |
| dim_customer | 4372 |
| dim_product | 4070 |
| dim_country | 38 |
| dim_date | 305 |
| fact_sales | 536641 |

Counts may vary if the dataset or cleaning logic changes.

Exit PostgreSQL:

```sql
\q
```

## 13. Run SQL Analysis Queries

Run these commands from PowerShell in the project root:

```powershell
psql -U postgres -d ecommerce_analytics -f sql/monthly_sales_analysis.sql
```

```powershell
psql -U postgres -d ecommerce_analytics -f sql/country_sales_analysis.sql
```

```powershell
psql -U postgres -d ecommerce_analytics -f sql/top_products.sql
```

```powershell
psql -U postgres -d ecommerce_analytics -f sql/top_customers.sql
```

These scripts analyze monthly sales, country performance, top products, and top customers.

## 14. Business Rules and Data Limitations

### Sales calculation

Sales analysis uses the following conditions:

- Cancellation flag is false
- Quantity is greater than zero
- Unit price is greater than zero

This prevents cancellation lines and non-positive transaction lines from being included in the positive sales calculation.

### Revenue versus profit

The dataset does not include product purchase costs. Therefore, the project calculates sales revenue, not profit.

### Returns

Negative-quantity records are treated as return-like records for analysis. They are not independently verified customer returns.

### Customer identification

Some transactions have missing customer IDs. Customer-level analysis only includes records that can be associated with a customer ID.

### RFM analysis

RFM segmentation is a descriptive customer analysis based on recency, frequency, and monetary value. It is not a predictive machine-learning model.

## 15. Troubleshooting

### Error: `psql is not recognized`

Check whether PostgreSQL's `bin` folder is in your Windows PATH.

An example location is:

`C:\Program Files\PostgreSQL\18\bin`

Restart PowerShell after updating PATH.

### Error: Database already exists

Do not create the database again. Check whether it already contains tables or data before continuing.

### Error: CSV file not found

Check that `data/cleaned_online_retail.csv` exists and that the path in the `\copy` command is correct.

### Error: Duplicate staging records

The CSV may have been imported more than once. Do not repeat the import. Check the existing database before deciding how to recover.

### Error: Star-schema load stops because `fact_sales` is not empty

This is a safety check. Do not delete existing data just to make the script run. Use a fresh database for a new initial load, or inspect the existing database first.

### Error: Table does not exist

Create the star-schema tables and staging table before attempting to load the data.

## 16. Project GitHub Repository

GitHub repository:

https://github.com/santoshkhadul/ecommerce-customer-intelligence

## 17. Final Notes

- Use Python for data cleaning, exploratory analysis, customer analysis, and charts.
- Use PostgreSQL for structured storage and SQL analysis.
- Use Power BI only if you want an optional interactive dashboard.
- Keep the original dataset and cleaned CSV out of Git if they are excluded by `.gitignore`.
- Never share your PostgreSQL password in the README or setup guide.
