SELECT
    s.channel,
    p.standard_category,
    COUNT(s.order_id) AS valid_order_count,
    ROUND(
        SUM(s.net_sales),
        2
    ) AS total_net_sales,
    ROUND(
        SUM(s.quantity * p.standard_cost),
        2
    ) AS estimated_cost,
    ROUND(
        SUM(s.net_sales - s.quantity * p.standard_cost),
        2
    ) AS estimated_gross_profit,
    ROUND(
    SUM(s.net_sales - s.quantity * p.standard_cost)
    * 100.0
    / SUM(s.net_sales),
    2
) AS estimated_gross_margin_rate
FROM sales_orders AS s
INNER JOIN product_info AS p
    ON s.product_name = p.product_name
WHERE
    s.order_status = '已完成'
    AND s.sales_amount_valid = 1
GROUP BY
    s.channel,
    p.standard_category
HAVING
    COUNT(s.order_id) >= 2
    AND (
        SUM(s.net_sales - s.quantity * p.standard_cost)
        * 100.0
        / SUM(s.net_sales)
    ) >= 45
ORDER BY estimated_gross_profit DESC;