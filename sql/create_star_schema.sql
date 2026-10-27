CREATE TABLE IF NOT EXISTS dim_customer (
    customer_key SERIAL PRIMARY KEY,
    customer_id INTEGER UNIQUE
);

CREATE TABLE IF NOT EXISTS dim_product (
    product_key SERIAL PRIMARY KEY,
    stock_code VARCHAR(30) UNIQUE,
    description TEXT
);

CREATE TABLE IF NOT EXISTS dim_country (
    country_key SERIAL PRIMARY KEY,
    country_name VARCHAR(100) UNIQUE
);

CREATE TABLE IF NOT EXISTS dim_date (
    date_key INTEGER PRIMARY KEY,
    full_date DATE UNIQUE,
    year INTEGER,
    month INTEGER,
    month_name VARCHAR(20),
    quarter INTEGER,
    day_of_month INTEGER
);

CREATE TABLE IF NOT EXISTS fact_sales (
    sales_key BIGSERIAL PRIMARY KEY,
    invoice_no VARCHAR(20),
    product_key INTEGER REFERENCES dim_product(product_key),
    customer_key INTEGER REFERENCES dim_customer(customer_key),
    country_key INTEGER REFERENCES dim_country(country_key),
    date_key INTEGER REFERENCES dim_date(date_key),
    quantity INTEGER,
    unit_price NUMERIC(12,4),
    line_amount NUMERIC(14,4),
    is_cancellation BOOLEAN,
    is_return BOOLEAN
);
