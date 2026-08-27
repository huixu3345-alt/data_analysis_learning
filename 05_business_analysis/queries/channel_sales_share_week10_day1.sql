WITH channel_summary AS (
    SELECT
    channel,
    Sum(net_sales)AS channel_sales
    FROM sales_orders
    WHERE order_status = '已完成' And sales_amount_valid = 1
    GROUP BY channel

)
SELECT
    channel,
    channel_sales,
    ROUND(
        channel_sales * 100.0
        / SUM(channel_sales) OVER (),
        2
    ) AS channel_rate
FROM channel_summary
ORDER BY channel_rate DESC;