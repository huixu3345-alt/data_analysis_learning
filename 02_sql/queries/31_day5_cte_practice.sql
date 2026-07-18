WITH valid_dated_orders AS (
    SELECT
        s.order_id,
        s.order_month,
        s.net_sales,
        s.net_sales - s.quantity * p.standard_cost
            AS estimated_gross_profit
    FROM sales_orders AS s
    INNER JOIN product_info AS p
        ON s.product_name = p.product_name
    WHERE
        s.order_status = '已完成'
        AND s.sales_amount_valid = 1
        AND s.order_date IS NOT NULL
),

monthly_summary AS (
    SELECT
        order_month,
        COUNT(order_id) AS valid_order_count,
        ROUND(
            SUM(net_sales),
            2
        ) AS total_net_sales,
        ROUND(
            SUM(estimated_gross_profit),
            2
        ) AS estimated_gross_profit
    FROM valid_dated_orders
    GROUP BY order_month
)

SELECT
    order_month,
    valid_order_count,
    total_net_sales,
    estimated_gross_profit,
    CASE
        WHEN total_net_sales >= 5000 THEN '重点月份'
        ELSE '普通月份'
    END AS month_level
FROM monthly_summary
ORDER BY order_month ASC;