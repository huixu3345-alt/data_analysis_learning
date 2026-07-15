SELECT
    channel,
    COUNT(*) AS order_count,
    SUM(quantity) AS total_quantity,
    ROUND(
        SUM(net_sales),
        2
    ) AS total_net_sales
FROM sales_orders
WHERE
    order_status = '已完成'
    AND sales_amount_valid = 1
GROUP BY
    channel
HAVING
    SUM(net_sales) > 4000
ORDER BY
    total_net_sales DESC;