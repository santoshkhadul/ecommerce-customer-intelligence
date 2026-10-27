-- Country-wise sales analysis
SELECT
    co.country_name,
    ROUND(SUM(f.line_amount), 2) AS total_sales_value,
    COUNT(DISTINCT f.invoice_no) AS invoice_count,
    COUNT(DISTINCT f.customer_key) AS identified_customers
FROM fact_sales f
JOIN dim_country co
    ON f.country_key = co.country_key
WHERE f.is_cancellation = FALSE
  AND f.quantity > 0
  AND f.unit_price > 0
GROUP BY co.country_name
ORDER BY total_sales_value DESC;
