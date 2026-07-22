WITH user_summary AS (
    SELECT
        user_id,
        COUNT(user_order_id) AS completed_order_count,
        COUNT(DISTINCT order_month) AS active_month_count,
        ROUND(SUM(net_sales), 2) AS total_net_sales
    FROM user_orders
    WHERE order_status = '已完成'
    GROUP BY user_id
)

SELECT
    COUNT(user_id) AS total_purchasing_users,

    SUM(
        CASE
            WHEN completed_order_count >= 2 THEN 1
            ELSE 0
        END
    ) AS repurchase_user_count,

    ROUND(
        100.0 * SUM(
            CASE
                WHEN completed_order_count >= 2 THEN 1
                ELSE 0
            END
        ) / COUNT(user_id),
        2
    ) AS repurchase_rate,

    SUM(
        CASE
            WHEN active_month_count >= 2 THEN 1
            ELSE 0
        END
    ) AS cross_month_repurchase_user_count,

    ROUND(
        100.0 * SUM(
            CASE
                WHEN active_month_count >= 2 THEN 1
                ELSE 0
            END
        ) / COUNT(user_id),
        2
    ) AS cross_month_repurchase_rate,

    ROUND(SUM(total_net_sales), 2) AS total_net_sales
FROM user_summary;