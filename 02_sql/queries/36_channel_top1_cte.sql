WITH ranked_orders AS (
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
)

SELECT
    order_id,
    channel,
    product_name,
    net_sales,
    channel_sales_rank
FROM ranked_orders
WHERE channel_sales_rank = 1
ORDER BY net_sales DESC;