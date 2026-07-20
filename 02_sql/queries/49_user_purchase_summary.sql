SELECT
    user_id,

    COUNT(user_order_id) AS completed_order_count,

    COUNT(
        DISTINCT order_month
    ) AS active_month_count,

    MIN(order_date) AS first_order_date,

    MAX(order_date) AS last_order_date,

    ROUND(
        SUM(net_sales),
        2
    ) AS total_net_sales

FROM user_orders
WHERE order_status = '已完成'
GROUP BY user_id
ORDER BY user_id;