# E-Commerce Customer Intelligence & Revenue Analytics



## Project Overview



This project analyzes online retail transactions to understand sales performance, customer purchasing behavior, product demand, and country-wise revenue.



It uses Python for data cleaning and analysis, PostgreSQL for relational data storage and SQL analysis, and Matplotlib for charts.



## Tech Stack



\- Python

\- Pandas and NumPy

\- Matplotlib and Seaborn

\- PostgreSQL and SQL

\- CSV and Excel

\- Git and GitHub



## Project Structure



```text

ecommerce-customer-intelligence/

â”œâ”€â”€ data/             # Source dataset and cleaned data

â”œâ”€â”€ models/           # Reserved for future models

â”œâ”€â”€ notebooks/        # Exploratory notebooks

â”œâ”€â”€ powerbi/          # Reserved for optional Power BI work

â”œâ”€â”€ reports/          # Analysis results and charts

â”œâ”€â”€ sql/              # SQL queries and schema

â”œâ”€â”€ src/              # Python analysis scripts

â”œâ”€â”€ run\_analysis.py   # Runs the Python analysis pipeline

â”œâ”€â”€ requirements.txt

â”œâ”€â”€ .gitignore

â””â”€â”€ README.md

```



## Dataset



This project uses the Online Retail dataset from the UCI Machine Learning Repository.



Dataset page: https://archive.ics.uci.edu/dataset/352/online+retail



Download `Online Retail.xlsx` and place it inside the `data/` directory.



The source dataset is not included in this repository.



## Setup



### 1. Install Python and PostgreSQL



Install Python and PostgreSQL if they are not already installed.



### 2. Clone the repository



```bash

git clone YOUR\_GITHUB\_REPOSITORY\_URL

cd ecommerce-customer-intelligence

```



Replace `YOUR\_GITHUB\_REPOSITORY\_URL` with the actual GitHub repository URL.



### 3. Create and activate a virtual environment



On Windows PowerShell:



```powershell

python -m venv venv

.\\venv\\Scripts\\Activate.ps1

```



### 4. Install dependencies



```powershell

python -m pip install -r requirements.txt

```



### 5. Add the dataset



Place the downloaded Excel file here:



```text

data/Online Retail.xlsx

```



### 6. Run the Python analysis



```powershell

python run\_analysis.py

```



The pipeline cleans the dataset, validates the data, analyzes sales and customers, generates charts, and creates summary reports in the `reports/` directory.



## PostgreSQL



The SQL scripts in `sql/` support database schema creation and analysis.



The database setup and data import are separate from the Python pipeline. Configure PostgreSQL, create the database, and load the cleaned CSV into the staging table before running the SQL analysis queries.



Do not rerun data imports against an existing database without checking for duplicate records first.



## Main Reports



The `reports/` directory contains outputs such as:



\- Monthly sales analysis

\- Top products and top customers

\- Country-wise sales analysis

\- Customer summaries and RFM segments

\- Executive KPI summary

\- Sales and


