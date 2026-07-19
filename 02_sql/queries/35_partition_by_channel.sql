SELECT
    order_id,
    channel,
    product_name,
    net_sales,
    ROW_NUMBER() OVER (
        PARTITION BY channel
        ORDER BY net_sales DESC
    ) AS channel_sales_rank
FROM sales_orders
WHERE
    order_status = '已完成'
    AND sales_amount_valid = 1
ORDER BY
    channel,
    channel_sales_rank;