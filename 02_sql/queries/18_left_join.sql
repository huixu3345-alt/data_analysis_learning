SELECT
    p.product_name,
    p.standard_category,
    p.standard_cost,
    s.order_id,
    s.quantity,
    s.net_sales
FROM product_info AS p
LEFT JOIN sales_orders AS s
    ON p.product_name = s.product_name
ORDER BY
    p.product_name,
    s.order_id;