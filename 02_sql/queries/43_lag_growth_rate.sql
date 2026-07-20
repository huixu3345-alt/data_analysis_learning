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
),

monthly_comparison AS (
    SELECT
        order_month,
        valid_order_count,
        total_net_sales,
        LAG(total_net_sales) OVER (
            ORDER BY order_month
        ) AS previous_month_sales
    FROM monthly_sales
)

SELECT
    order_month,
    valid_order_count,
    total_net_sales,
    previous_month_sales,

    ROUND(
        total_net_sales - previous_month_sales,
        2
    ) AS sales_growth_amount,

    ROUND(
        (total_net_sales - previous_month_sales)
        * 100.0
        / NULLIF(previous_month_sales, 0),
        2
    ) AS sales_growth_rate

FROM monthly_comparison
ORDER BY order_month;