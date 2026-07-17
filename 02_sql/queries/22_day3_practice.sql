SELECT
    p.standard_category,
    COUNT(s.order_id) AS valid_order_count,
    ROUND(
        COALESCE(SUM(s.net_sales), 0),
        2
    ) AS total_net_sales,
    ROUND(
        COALESCE(SUM(s.quantity * p.standard_cost), 0),
        2
    ) AS estimated_cost,
    ROUND(
        COALESCE(
            SUM(s.net_sales - s.quantity * p.standard_cost),
            0
        ),
        2
    ) AS estimated_gross_profit
FROM product_info AS p
LEFT JOIN sales_orders AS s
    ON p.product_name = s.product_name
    AND s.order_status = '已完成'
    AND s.sales_amount_valid = 1
GROUP BY p.standard_category
ORDER BY estimated_gross_profit DESC;