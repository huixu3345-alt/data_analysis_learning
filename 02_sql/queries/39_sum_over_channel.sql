SELECT
    order_id,
    channel,
    product_name,
    net_sales,

    ROUND(
        SUM(net_sales) OVER (
            PARTITION BY channel
        ),
        2
    ) AS channel_total_sales,

    ROUND(
        net_sales * 100.0
        / SUM(net_sales) OVER (
            PARTITION BY channel
        ),
        2
    ) AS order_channel_share

FROM sales_orders
WHERE
    order_status = '已完成'
    AND sales_amount_valid = 1
ORDER BY
    channel,
    net_sales DESC;