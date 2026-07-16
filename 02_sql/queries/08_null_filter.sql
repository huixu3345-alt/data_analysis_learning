SELECT
    order_id,
    city,
    product_name,
    net_sales
FROM sales_orders
WHERE city IS NOT NULL
ORDER BY net_sales DESC;