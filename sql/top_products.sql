-- Top 10 products by sales value
SELECT
    p.stock_code,
    p.description,
    ROUND(SUM(f.line_amount), 2) AS total_sales_value,
    SUM(f.quantity) AS total_quantity_sold
FROM fact_sales f
JOIN dim_product p
    ON f.product_key = p.product_key
WHERE f.is_cancellation = FALSE
  AND f.quantity > 0
  AND f.unit_price > 0
GROUP BY
    p.stock_code,
    p.description
ORDER BY
    total_sales_value DESC
LIMIT 10;
