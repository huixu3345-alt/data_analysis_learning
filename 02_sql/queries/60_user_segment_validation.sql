WITH user_summary AS (
    SELECT
        user_id,
        COUNT(*) AS completed_order_count,
        COUNT(DISTINCT order_month) AS active_month_count,
        ROUND(SUM(net_sales), 2) AS total_net_sales
    FROM user_orders
    WHERE order_status = '已完成'
    GROUP BY user_id
),

user_segments AS (
    SELECT
        user_id,
        total_net_sales,

        CASE
            WHEN completed_order_count >= 2
                AND active_month_count >= 2
                AND total_net_sales >= 1000
                THEN '核心用户'

            WHEN completed_order_count >= 2
                THEN '复购用户'

            ELSE '普通用户'
        END AS user_level

    FROM user_summary
),

segment_summary AS (
    SELECT
        user_level,
        COUNT(user_id) AS user_count,
        ROUND(SUM(total_net_sales), 2) AS segment_net_sales,
        ROUND(AVG(total_net_sales), 2) AS avg_user_sales
    FROM user_segments
    GROUP BY user_level
)

SELECT
    user_level,
    user_count,
    segment_net_sales,
    avg_user_sales,

    ROUND(
        100.0 * segment_net_sales
        / SUM(segment_net_sales) OVER (),
        2
    ) AS sales_share,

    ROUND(
        SUM(segment_net_sales) OVER (),
        2
    ) AS validated_total_net_sales

FROM segment_summary
ORDER BY
    CASE user_level
        WHEN '核心用户' THEN 1
        WHEN '复购用户' THEN 2
        ELSE 3
    END;