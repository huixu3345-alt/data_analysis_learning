SELECT
    channel,
    COUNT(order_id) AS valid_order_count,
    ROUND(
        COALESCE(SUM(net_sales), 0),
        2
    ) AS total_net_sales
FROM sales_orders
WHERE
    order_status = '已完成'
    AND sales_amount_valid = 1
GROUP BY channel
ORDER BY total_net_sales DESC;