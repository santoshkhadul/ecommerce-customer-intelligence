-- Top 10 customers by sales value
SELECT
    c.customer_id,
    ROUND(SUM(f.line_amount), 2) AS total_spending,
    COUNT(DISTINCT f.invoice_no) AS invoice_count
FROM fact_sales f
JOIN dim_customer c
    ON f.customer_key = c.customer_key
WHERE f.is_cancellation = FALSE
  AND f.quantity > 0
  AND f.unit_price > 0
GROUP BY c.customer_id
ORDER BY total_spending DESC
LIMIT 10;
