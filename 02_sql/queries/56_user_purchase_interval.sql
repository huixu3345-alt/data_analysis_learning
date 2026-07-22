WITH ordered_purchases AS (
    SELECT
        user_order_id,
        user_id,
        order_date,
        order_month,
        net_sales,

        LAG(order_date) OVER (
            PARTITION BY user_id
            ORDER BY order_date
        ) AS previous_purchase_date

    FROM user_orders
    WHERE order_status = '已完成'
),

purchase_intervals AS (
    SELECT
        user_order_id,
        user_id,
        order_date,
        order_month,
        net_sales,
        previous_purchase_date,

        CAST(
            julianday(order_date)
            - julianday(previous_purchase_date)
            AS INTEGER
        ) AS days_since_previous_purchase

    FROM ordered_purchases
)

SELECT
    user_order_id,
    user_id,
    order_date,
    previous_purchase_date,
    days_since_previous_purchase,
    net_sales
FROM purchase_intervals
WHERE previous_purchase_date IS NOT NULL
ORDER BY
    user_id,
    order_date;