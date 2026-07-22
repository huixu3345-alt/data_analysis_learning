WITH user_summary AS (
    SELECT
        user_id,
        COUNT(*) AS completed_order_count,
        COUNT(DISTINCT order_month) AS active_month_count,
        ROUND(SUM(net_sales), 2) AS total_net_sales,
        ROUND(AVG(net_sales), 2) AS avg_order_sales
    FROM user_orders
    WHERE order_status = '已完成'
    GROUP BY user_id
),

user_segments AS (
    SELECT
        user_id,
        completed_order_count,
        active_month_count,
        total_net_sales,
        avg_order_sales,

        CASE
            WHEN completed_order_count >= 2
                AND active_month_count >= 2
                AND total_net_sales >= 1000
                THEN '核心用户'

            WHEN completed_order_count >= 2
                THEN '复购用户'

            ELSE '普通用户'
        END AS user_level,

        RANK() OVER (
            ORDER BY total_net_sales DESC
        ) AS user_value_rank

    FROM user_summary
)

SELECT
    user_id,
    completed_order_count,
    active_month_count,
    total_net_sales,
    avg_order_sales,
    user_level,
    user_value_rank
FROM user_segments
ORDER BY user_value_rank;