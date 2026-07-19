SELECT
    order_id,
    channel,
    product_name,
    net_sales,
    ROW_NUMBER() OVER (
        ORDER BY net_sales DESC
    ) AS sales_rank
FROM sales_orders
WHERE
    order_status = '已完成'
    AND sales_amount_valid = 1
ORDER BY sales_rank;