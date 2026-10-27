
BEGIN;

-- Safety check: prevent duplicate fact loading.
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM fact_sales) THEN
        RAISE EXCEPTION
            'fact_sales is not empty. Use a fresh database for the initial load.';
    END IF;
END $$;

-- 1. Load customers
INSERT INTO dim_customer (customer_id)
SELECT DISTINCT customer_id
FROM staging_retail
WHERE customer_id IS NOT NULL
ON CONFLICT (customer_id) DO NOTHING;

-- 2. Load products
INSERT INTO dim_product (stock_code, description)
SELECT
    stock_code,
    MIN(description) AS description
FROM staging_retail
WHERE stock_code IS NOT NULL
GROUP BY stock_code
ON CONFLICT (stock_code) DO NOTHING;

-- 3. Load countries
INSERT INTO dim_country (country_name)
SELECT DISTINCT country
FROM staging_retail
WHERE country IS NOT NULL
ON CONFLICT (country_name) DO NOTHING;

-- 4. Load dates
INSERT INTO dim_date (
    date_key,
    full_date,
    year,
    month,
    month_name,
    quarter,
    day_of_month
)
SELECT DISTINCT
    TO_CHAR(invoice_date::date, 'YYYYMMDD')::INTEGER,
    invoice_date::date,
    EXTRACT(YEAR FROM invoice_date)::INTEGER,
    EXTRACT(MONTH FROM invoice_date)::INTEGER,
    TO_CHAR(invoice_date, 'FMMonth'),
    EXTRACT(QUARTER FROM invoice_date)::INTEGER,
    EXTRACT(DAY FROM invoice_date)::INTEGER
FROM staging_retail
WHERE invoice_date IS NOT NULL
ON CONFLICT DO NOTHING;

-- 5. Load sales fact rows
INSERT INTO fact_sales (
    invoice_no,
    product_key,
    customer_key,
    country_key,
    date_key,
    quantity,
    unit_price,
    line_amount,
    is_cancellation,
    is_return
)
SELECT
    s.invoice_no,
    p.product_key,
    c.customer_key,
    co.country_key,
    d.date_key,
    s.quantity,
    s.unit_price,
    s.line_amount,
    s.is_cancellation,
    s.is_return
FROM staging_retail s
JOIN dim_product p
    ON p.stock_code = s.stock_code
LEFT JOIN dim_customer c
    ON c.customer_id = s.customer_id
JOIN dim_country co
    ON co.country_name = s.country
JOIN dim_date d
    ON d.full_date = s.invoice_date::date;

COMMIT;
