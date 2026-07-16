-- SELECT
--     order_id,
--     product_name,
--     category,
--     net_sales
-- FROM sales_orders
-- WHERE product_name LIKE '%鼠标%'
-- ORDER BY net_sales DESC;

SELECT
    order_id,
    order_date,
    product_name,
    category,
    net_sales
FROM sales_orders
WHERE
    order_status = '已完成'
    AND sales_amount_valid = 1
    AND product_name LIKE '%耳机%'
ORDER BY net_sales DESC;