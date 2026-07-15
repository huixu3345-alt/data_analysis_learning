SELECT
    order_id,
    product_name,
    city,
    channel,
    net_sales
FROM sales_orders
WHERE
    order_status = '已完成'
    AND sales_amount_valid = 1
ORDER BY
    net_sales DESC
LIMIT 5;