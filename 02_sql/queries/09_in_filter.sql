SELECT
    order_id,
    city,
    channel,
    product_name,
    net_sales
FROM sales_orders
WHERE
    order_status = '已完成'
    AND sales_amount_valid = 1
    AND (
        city NOT IN ('北京', '上海')
        OR city IS NULL
    )
ORDER BY net_sales DESC;