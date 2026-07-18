SELECT
    order_id,
    order_date,
    channel,
    product_name,
    net_sales
FROM sales_orders
WHERE
    order_status = '已完成'
    AND sales_amount_valid = 1
    AND channel = (
        SELECT
            channel
        FROM sales_orders
        WHERE
            order_status = '已完成'
            AND sales_amount_valid = 1
        GROUP BY channel
        ORDER BY SUM(net_sales) DESC
        LIMIT 1
    )
ORDER BY net_sales DESC;