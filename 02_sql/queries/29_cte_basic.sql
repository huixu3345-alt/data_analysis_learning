WITH valid_order_details AS (
    SELECT
        s.order_id,
        s.channel,
        p.standard_category,
        s.quantity,
        s.net_sales,
        s.quantity * p.standard_cost AS estimated_cost,
        s.net_sales - s.quantity * p.standard_cost
            AS estimated_gross_profit
    FROM sales_orders AS s
    INNER JOIN product_info AS p
        ON s.product_name = p.product_name
    WHERE
        s.order_status = '已完成'
        AND s.sales_amount_valid = 1
)

SELECT
    standard_category,
    COUNT(order_id) AS valid_order_count,
    ROUND(SUM(net_sales), 2) AS total_net_sales,
    ROUND(SUM(estimated_cost), 2) AS estimated_cost,
    ROUND(
        SUM(estimated_gross_profit),
        2
    ) AS estimated_gross_profit
FROM valid_order_details
GROUP BY standard_category
ORDER BY estimated_gross_profit DESC;