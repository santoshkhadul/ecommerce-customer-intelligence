
CREATE TABLE IF NOT EXISTS staging_retail (
    invoice_no VARCHAR(20),
    stock_code VARCHAR(30),
    description TEXT,
    quantity INTEGER,
    invoice_date TIMESTAMP WITHOUT TIME ZONE,
    unit_price NUMERIC(12, 4),
    customer_id INTEGER,
    country VARCHAR(100),
    line_amount NUMERIC(14, 4),
    is_cancellation BOOLEAN,
    is_return BOOLEAN,
    is_valid_price BOOLEAN,
    has_customer_id BOOLEAN,
    has_valid_date BOOLEAN,
    has_valid_quantity BOOLEAN,
    has_valid_price_value BOOLEAN,
    has_valid_invoice BOOLEAN
);
