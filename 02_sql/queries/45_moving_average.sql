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

    ROUND(
        AVG(total_net_sales) OVER (
            ORDER BY order_month
            ROWS BETWEEN 1 PRECEDING
                     AND CURRENT ROW
        ),
        2
    ) AS two_month_moving_avg

FROM monthly_sales
ORDER BY order_month;