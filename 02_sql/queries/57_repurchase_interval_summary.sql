WITH ordered_purchases AS (
    SELECT
        user_id,
        order_date,

        LAG(order_date) OVER (
            PARTITION BY user_id
            ORDER BY order_date
        ) AS previous_purchase_date

    FROM user_orders
    WHERE order_status = '已完成'
),

purchase_intervals AS (
    SELECT
        user_id,

        CAST(
            julianday(order_date)
            - julianday(previous_purchase_date)
            AS INTEGER
        ) AS days_since_previous_purchase

    FROM ordered_purchases
    WHERE previous_purchase_date IS NOT NULL
)

SELECT
    COUNT(*) AS repurchase_event_count,
    COUNT(DISTINCT user_id) AS repurchase_user_count,
    SUM(days_since_previous_purchase) AS total_interval_days,
    ROUND(AVG(days_since_previous_purchase), 2) AS avg_repurchase_interval_days,
    MIN(days_since_previous_purchase) AS min_repurchase_interval_days,
    MAX(days_since_previous_purchase) AS max_repurchase_interval_days
FROM purchase_intervals;