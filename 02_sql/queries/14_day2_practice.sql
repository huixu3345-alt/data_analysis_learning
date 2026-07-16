SELECT
    order_id,
    channel,
    product_name,
    net_sales,
    CASE
        WHEN net_sales >= 1000 THEN '重点订单'
        ELSE '普通订单'
    END AS order_level
FROM sales_orders
WHERE
    order_status = '已完成'
    AND sales_amount_valid = 1
    AND channel IN ('天猫', '抖音')
ORDER BY net_sales DESC;