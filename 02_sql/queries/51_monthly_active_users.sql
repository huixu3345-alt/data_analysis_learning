SELECT
    order_month,

    COUNT(
        DISTINCT user_id
    ) AS monthly_purchasing_users,

    COUNT(user_order_id) AS completed_order_count,

    ROUND(
        SUM(net_sales),
        2
    ) AS total_net_sales

FROM user_orders
WHERE order_status = '已完成'
GROUP BY order_month
ORDER BY order_month;