# E-Commerce Customer Intelligence & Revenue Analytics

This project is based on the UCI Online Retail dataset. I built it to understand how sales and customer data can be used to find useful business insights.

I used Python for data cleaning and analysis, PostgreSQL for storing and organizing the data, and SQL for answering business-related questions.

The main focus was to work through the complete data analytics process, starting with raw transaction data and ending with reports and visualizations.

## What I worked on

- Cleaned and prepared the raw retail transaction dataset using Python.
- Checked missing values, duplicate records, cancellations, negative quantities, and invalid prices.
- Analyzed monthly sales and country-wise performance.
- Identified top-performing products and customers.
- Analyzed repeat and one-time customers.
- Used RFM (Recency, Frequency, Monetary) analysis to group customers based on their purchasing behavior.
- Created charts and summary reports using Python.
- Designed a star schema in PostgreSQL and wrote SQL queries for business analysis.

## Tools and Technologies

- **Python** – Data processing and analysis
- **Pandas & NumPy** – Data cleaning and calculations
- **Matplotlib** – Data visualization
- **PostgreSQL** – Database management
- **SQL** – Data modeling and business queries
- **Git & GitHub** – Version control

## Dataset

The project uses the Online Retail dataset from the UCI Machine Learning Repository.

Dataset: [UCI Online Retail](https://archive.ics.uci.edu/dataset/352/online+retail)

The original dataset contains 541,909 transaction records from a UK-based online retail business.

After removing exact duplicate records, 536,641 rows remained for further analysis.

The dataset contains information such as invoice numbers, product codes, descriptions, quantities, invoice dates, unit prices, customer IDs, and countries.

## Project Structure

```text
ecommerce-customer-intelligence/
│
├── data/
│   ├── Online Retail.xlsx
│   └── cleaned_online_retail.csv
│
├── reports/
│   ├── executive_kpi_summary.csv
│   ├── sales_summary.csv
│   ├── monthly_sales.csv
│   ├── country_sales_analysis.csv
│   ├── top_products.csv
│   ├── top_customers.csv
│   ├── customer_summary.csv
│   ├── customer_rfm_analysis.csv
│   └── charts
│
├── src/
│   ├── inspect_data.py
│   ├── clean_data.py
│   ├── validate_data.py
│   ├── diagnose_transactions.py
│   ├── sales_analysis.py
│   ├── customer_analysis.py
│   ├── customer_charts.py
│   └── kpi_summary.py
│
├── sql/
│   ├── create_star_schema.sql
│   ├── create_staging_table.sql
│   ├── load_star_schema.sql
│   ├── monthly_sales_analysis.sql
│   ├── country_sales_analysis.sql
│   ├── top_products.sql
│   └── top_customers.sql
│
├── requirements.txt
├── run_analysis.py
├── README.md
└── POSTGRESQL_SETUP.md
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/santoshkhadul/ecommerce-customer-intelligence.git
```

Move into the project folder:

```bash
cd ecommerce-customer-intelligence
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install the required packages

```bash
python -m pip install -r requirements.txt
```

### 4. Download the dataset

Download the Online Retail dataset from UCI:

https://archive.ics.uci.edu/dataset/352/online+retail

Place the Excel file inside the `data` folder and name it:

`Online Retail.xlsx`

### 5. Run the project

```bash
python run_analysis.py
```

The main Python file runs the analysis scripts in sequence and generates cleaned data, reports, and charts.

## PostgreSQL Setup

PostgreSQL is used to store the cleaned transaction data and organize it using a star-schema model.

The database contains:

- `staging_retail`
- `dim_customer`
- `dim_product`
- `dim_country`
- `dim_date`
- `fact_sales`

The SQL scripts cover table creation, initial data loading, monthly sales analysis, country-wise analysis, top products, and top customers.

For the complete database setup and loading instructions, see:

[POSTGRESQL_SETUP.md](POSTGRESQL_SETUP.md)

**Note:** The initial CSV import and star-schema loading process should be performed only once on a fresh database. Do not repeat these steps on an already populated database.

## Some Results

A few results from the current analysis:

| Metric | Result |
|---|---:|
| Original records | 541,909 |
| Cleaned records | 536,641 |
| Total products | 4,070 |
| Countries | 38 |
| Positive sales invoices | 19,960 |
| Positive sales value | 10,642,110.80 |
| Identified customers in positive sales | 4,338 |
| Repeat customers | 2,845 |
| One-time customers | 1,493 |
| Repeat customer rate | 65.58% |

These figures are based on the current cleaned dataset and project filters.

## Business Rules

For the main positive sales analysis, I included records where:

- The invoice is not marked as a cancellation.
- Quantity is greater than zero.
- Unit price is greater than zero.

A few limitations are worth mentioning:

- The dataset does not contain product costs, so this project analyzes sales value rather than profit.
- Negative quantities are treated as return-like records, not confirmed returns.
- Customer analysis uses records with an available customer ID.
- RFM segmentation is a descriptive analysis, not a predictive model.

## What I Learned

While building this project, I got practical experience with:

- Working with a large real-world dataset.
- Cleaning and validating transaction data.
- Writing reusable Python scripts.
- Using Pandas for data analysis.
- Designing a PostgreSQL star schema.
- Writing SQL queries for business reporting.
- Creating charts and presenting analytical results.
- Managing a project using Git and GitHub.

## Future Improvements

- Build an interactive Power BI dashboard.
- Add more detailed customer cohort analysis.
- Improve automated data-quality checks.
- Explore customer purchasing patterns over time.

---
**GitHub Repository:**  
https://github.com/santoshkhadul/ecommerce-customer-intelligence
