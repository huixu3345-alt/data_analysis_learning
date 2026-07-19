SELECT
    order_date,
    order_id,
    channel,
    product_name,
    net_sales,

    ROUND(
        SUM(net_sales) OVER (
            PARTITION BY channel
            ORDER BY order_date
            ROWS BETWEEN UNBOUNDED PRECEDING
                     AND CURRENT ROW
        ),
        2
    ) AS channel_running_sales

FROM sales_orders
WHERE
    order_status = '已完成'
    AND sales_amount_valid = 1
    AND order_date IS NOT NULL
ORDER BY
    channel,
    order_date;