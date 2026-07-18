SELECT
    order_id,
    channel,
    product_name,
    net_sales
FROM sales_orders
WHERE
    order_status = '已完成'
    AND sales_amount_valid = 1
    AND net_sales > (
        SELECT AVG(net_sales)
        FROM sales_orders
        WHERE
            order_status = '已完成'
            AND sales_amount_valid = 1
    )
ORDER BY net_sales DESC;