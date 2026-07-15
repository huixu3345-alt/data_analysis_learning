SELECT
    COUNT(*) AS order_count,
    SUM(quantity) AS total_quantity,
    ROUND(
        SUM(net_sales),
        2
    ) AS total_net_sales,
    ROUND(
        AVG(net_sales),
        2
    ) AS avg_order_sales,
    MIN(net_sales) AS min_order_sales,
    MAX(net_sales) AS max_order_sales
FROM sales_orders
WHERE
    order_status = '已完成'
    AND sales_amount_valid = 1;