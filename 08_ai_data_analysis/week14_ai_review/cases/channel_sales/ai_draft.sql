SELECT
    channel,
    ROUND(SUM(net_sales), 2) AS valid_net_sales,
    COUNT(order_date) AS valid_order_count
FROM sales_orders
WHERE sales_amount_valid = 1
GROUP BY channel
ORDER BY valid_net_sales DESC;
