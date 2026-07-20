WITH monthly_sales AS (
    SELECT
        order_month,
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
    total_net_sales,

    LEAD(total_net_sales) OVER (
        ORDER BY order_month
    ) AS next_month_sales,

    ROUND(
        LEAD(total_net_sales) OVER (
            ORDER BY order_month
        ) - total_net_sales,
        2
    ) AS change_to_next_month

FROM monthly_sales
ORDER BY order_month;