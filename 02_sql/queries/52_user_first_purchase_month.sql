SELECT
    user_id,

    MIN(order_month) AS first_purchase_month,

    COUNT(user_order_id) AS completed_order_count,

    ROUND(
        SUM(net_sales),
        2
    ) AS total_net_sales

FROM user_orders
WHERE order_status = '已完成'
GROUP BY user_id
ORDER BY
    first_purchase_month,
    user_id;