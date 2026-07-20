WITH monthly_sales AS (
    SELECT
        order_month,
        COUNT(order_id) AS valid_order_count,
        ROUND(
            SUM(net_sales),
            2
        ) AS total_net_sales
    FROM sales_orders
    WHERE
        order_status = '已完成'
        AND sales_amount_valid = 1
        AND order_date IS NOT NULL
    GROUP BY order_month
)

SELECT
    order_month,
    valid_order_count,
    total_net_sales,

    LAG(total_net_sales) OVER (
        ORDER BY order_month
    ) AS previous_month_sales,

    ROUND(
        total_net_sales
        - LAG(total_net_sales) OVER (
            ORDER BY order_month
        ),
        2
    ) AS sales_growth_amount

FROM monthly_sales
ORDER BY order_month;