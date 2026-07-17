SELECT
    p.product_name,
    COUNT(s.order_id) AS valid_order_count,
    ROUND(COALESCE(SUM(s.net_sales), 0), 2) AS total_net_sales
FROM product_info AS p
LEFT JOIN sales_orders AS s
    ON p.product_name = s.product_name
WHERE
    s.order_status = '已完成'
    AND s.sales_amount_valid = 1
GROUP BY p.product_name
ORDER BY total_net_sales DESC;