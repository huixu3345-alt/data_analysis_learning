SELECT
    s.order_id,
    s.product_name,
    p.standard_category,
    s.quantity,
    s.net_sales,
    p.standard_cost
FROM sales_orders AS s
INNER JOIN product_info AS p
    ON s.product_name = p.product_name
ORDER BY s.order_id;