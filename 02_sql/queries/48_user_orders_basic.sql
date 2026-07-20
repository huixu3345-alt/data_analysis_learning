SELECT
    user_order_id,
    user_id,
    order_date,
    order_month,
    order_status,
    net_sales
FROM user_orders
ORDER BY
    user_id,
    order_date;