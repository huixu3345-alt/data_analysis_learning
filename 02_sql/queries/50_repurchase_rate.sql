WITH user_purchase_summary AS (
    SELECT
        user_id,
        COUNT(user_order_id) AS completed_order_count,
        COUNT(
            DISTINCT order_month
        ) AS active_month_count
    FROM user_orders
    WHERE order_status = '已完成'
    GROUP BY user_id
)

SELECT
    COUNT(*) AS total_purchasing_users,

    SUM(
        CASE
            WHEN completed_order_count >= 2 THEN 1
            ELSE 0
        END
    ) AS repurchase_user_count,

    ROUND(
        SUM(
            CASE
                WHEN completed_order_count >= 2 THEN 1
                ELSE 0
            END
        ) * 100.0 / COUNT(*),
        2
    ) AS repurchase_rate,

    SUM(
        CASE
            WHEN active_month_count >= 2 THEN 1
            ELSE 0
        END
    ) AS cross_month_repurchase_user_count,

    ROUND(
        SUM(
            CASE
                WHEN active_month_count >= 2 THEN 1
                ELSE 0
            END
        ) * 100.0 / COUNT(*),
        2
    ) AS cross_month_repurchase_rate

FROM user_purchase_summary;