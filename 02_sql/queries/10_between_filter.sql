-- SELECT
--     order_id,
--     order_date,
--     city,
--     product_name,
--     net_sales
-- FROM sales_orders
-- WHERE
--     order_status = '已完成'
--     AND sales_amount_valid = 1
--     AND net_sales BETWEEN 800 AND 1200
-- ORDER BY net_sales DESC;

SELECT
    order_id,
    order_date,
    city,
    product_name,
    net_sales
FROM sales_orders
WHERE
    order_date BETWEEN '2026-02-01' AND '2026-02-28'
ORDER BY order_date;