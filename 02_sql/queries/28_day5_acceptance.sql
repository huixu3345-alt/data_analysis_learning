SELECT
    p.standard_category,
    COUNT(s.order_id) AS valid_order_count,
    ROUND(
        SUM(s.net_sales),
        2
    ) AS total_net_sales,
    ROUND(
        SUM(s.net_sales - s.quantity * p.standard_cost),
        2
    ) AS estimated_gross_profit
FROM sales_orders AS s
INNER JOIN product_info AS p
    ON s.product_name = p.product_name
WHERE
    s.order_status = '已完成'
    AND s.sales_amount_valid = 1
GROUP BY p.standard_category
HAVING
    SUM(s.net_sales - s.quantity * p.standard_cost) > 2000
ORDER BY estimated_gross_profit DESC;