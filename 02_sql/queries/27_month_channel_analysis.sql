SELECT
    s.order_month,
    s.channel,
    COUNT(*) AS valid_order_count,
    ROUND(SUM(s.net_sales), 2) AS total_net_sales,
    ROUND(SUM(s.quantity * p.standard_cost), 2) AS estimated_cost,
    ROUND(SUM(s.net_sales - s.quantity * p.standard_cost), 2) AS estimated_gross_profit
FROM sales_orders AS s
INNER JOIN product_info AS p
    ON s.product_name = p.product_name
WHERE
    s.order_status = '已完成'
    AND s.sales_amount_valid = 1
    AND s.order_date IS NOT NULL
GROUP BY
    s.order_month,
    s.channel
ORDER BY
    s.order_month,
    estimated_gross_profit DESC;