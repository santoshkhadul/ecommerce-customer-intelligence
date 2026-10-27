-- Monthly sales analysis
SELECT
    d.year,
    d.month,
    d.month_name,
    ROUND(SUM(f.line_amount), 2) AS total_sales_value,
    COUNT(DISTINCT f.invoice_no) AS invoice_count
FROM fact_sales f
JOIN dim_date d
    ON f.date_key = d.date_key
WHERE f.is_cancellation = FALSE
  AND f.quantity > 0
  AND f.unit_price > 0
GROUP BY
    d.year,
    d.month,
    d.month_name
ORDER BY
    d.year,
    d.month;
