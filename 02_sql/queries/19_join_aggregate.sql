-- SELECT
--     p.product_name,
--     COUNT(*) AS joined_row_count,
--     COUNT(s.order_id) AS order_count
-- FROM product_info AS p
-- LEFT JOIN sales_orders AS s
--     ON p.product_name = s.product_name
-- GROUP BY p.product_name
-- ORDER BY order_count DESC;

SELECT
    p.product_name,
    p.standard_category,
    COUNT(s.order_id) AS valid_order_count,
    ROUND(COALESCE(SUM(s.net_sales), 0), 2) AS total_net_sales
FROM product_info AS p
LEFT JOIN sales_orders AS s
    ON p.product_name = s.product_name
    AND s.order_status = '已完成'
    AND s.sales_amount_valid = 1
GROUP BY
    p.product_name,
    p.standard_category
ORDER BY total_net_sales DESC;