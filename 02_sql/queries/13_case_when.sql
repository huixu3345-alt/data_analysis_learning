-- SELECT
--     order_id,
--     product_name,
--     channel,
--     net_sales,
--     CASE
--         WHEN net_sales >= 1200 THEN '高销售额'
--         WHEN net_sales >= 800 THEN '中销售额'
--         ELSE '低销售额'
--     END AS sales_level
-- FROM sales_orders
-- WHERE
--     order_status = '已完成'
--     AND sales_amount_valid = 1
-- ORDER BY net_sales DESC;
SELECT
    CASE
        WHEN net_sales >= 1200 THEN '高销售额'
        WHEN net_sales >= 800 THEN '中销售额'
        ELSE '低销售额'
    END AS sales_level,
    COUNT(*) AS order_count,
    ROUND(SUM(net_sales), 2) AS total_net_sales,
    ROUND(AVG(net_sales), 2) AS avg_order_sales
FROM sales_orders
WHERE
    order_status = '已完成'
    AND sales_amount_valid = 1
GROUP BY sales_level
ORDER BY avg_order_sales DESC;