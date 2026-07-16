-- SELECT
--     order_id,
--     product_name,
--     channel,
--     net_sales
-- FROM sales_orders
-- WHERE
--     order_status = '已完成'
--     AND sales_amount_valid = 1
--     AND (
--         product_name = '蓝牙耳机'
--         OR product_name = '机械键盘'
--     )
-- ORDER BY net_sales DESC;

SELECT
    order_id,
    product_name,
    channel,
    net_sales
FROM sales_orders
WHERE
    order_status = '已完成'
    AND sales_amount_valid = 1
    AND product_name NOT LIKE '%鼠标%'
ORDER BY net_sales DESC;