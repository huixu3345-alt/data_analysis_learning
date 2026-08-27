WITH retention_orders(
    order_id,
    user_id,
    order_date,
    order_month,
    channel,
    order_status
) AS (
    VALUES
        ('O001', 'J01', '2026-01-02', '2026-01', '京东', '已完成'),
        ('O002', 'J02', '2026-01-04', '2026-01', '京东', '已完成'),
        ('O003', 'T01', '2026-01-03', '2026-01', '天猫', '已完成'),
        ('O004', 'T01', '2026-01-10', '2026-01', '京东', '已完成'),
        ('O005', 'T02', '2026-01-05', '2026-01', '天猫', '已完成'),
        ('O006', 'T03', '2026-01-07', '2026-01', '天猫', '已完成'),
        ('O007', 'D01', '2026-01-06', '2026-01', '抖音', '已完成'),
        ('O008', 'D02', '2026-01-08', '2026-01', '抖音', '已完成'),
        ('O009', 'D03', '2026-01-09', '2026-01', '抖音', '已完成'),
        ('O010', 'J01', '2026-02-02', '2026-02', '天猫', '已完成'),
        ('O011', 'J02', '2026-02-06', '2026-02', '京东', '已完成'),
        ('O012', 'T01', '2026-02-03', '2026-02', '天猫', '已完成'),
        ('O013', 'T01', '2026-02-18', '2026-02', '天猫', '已完成'),
        ('O014', 'T02', '2026-02-05', '2026-02', '天猫', '已完成'),
        ('O015', 'D01', '2026-02-04', '2026-02', '抖音', '已完成'),
        ('O016', 'D02', '2026-02-08', '2026-02', '抖音', '已完成'),
        ('O017', 'J03', '2026-02-10', '2026-02', '京东', '已完成'),
        ('O018', 'J04', '2026-02-12', '2026-02', '京东', '已完成'),
        ('O019', 'T04', '2026-02-11', '2026-02', '天猫', '已完成'),
        ('O020', 'T05', '2026-02-13', '2026-02', '天猫', '已完成'),
        ('O021', 'T06', '2026-02-15', '2026-02', '天猫', '已完成'),
        ('O022', 'D04', '2026-02-14', '2026-02', '抖音', '已完成'),
        ('O023', 'D05', '2026-02-16', '2026-02', '抖音', '已完成'),
        ('O024', 'D06', '2026-02-18', '2026-02', '抖音', '已完成'),
        ('O025', 'T04', '2026-03-03', '2026-03', '天猫', '已完成'),
        ('O026', 'T05', '2026-03-07', '2026-03', '天猫', '已完成'),
        ('O027', 'D04', '2026-03-05', '2026-03', '抖音', '已完成'),
        ('O028', 'D05', '2026-03-09', '2026-03', '抖音', '已完成'),
        ('O029', 'J03', '2026-03-06', '2026-03', '京东', '已取消'),
        ('O030', 'D06', '2026-03-11', '2026-03', '抖音', '已取消'),
        ('O031', 'J01', '2026-03-15', '2026-03', '京东', '已完成')
),
ranked_orders AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY user_id
            ORDER BY order_date
        ) AS order_rank
    FROM retention_orders
    WHERE order_status = '已完成'
),
active_months AS (
    SELECT DISTINCT
        user_id,
        order_month AS active_month
    FROM ranked_orders
),
first_orders AS (
    SELECT
        user_id,
        order_month AS cohort_month,
        channel AS acquisition_channel
    FROM ranked_orders
    WHERE order_rank = 1
),
retention_flags AS (
    SELECT
        f.user_id,
        f.cohort_month,
        f.acquisition_channel,
        CASE
            WHEN a.user_id IS NOT NULL THEN 1
            ELSE 0
        END AS month_1_retained
    FROM first_orders AS f
    LEFT JOIN active_months AS a
        ON f.user_id = a.user_id
       AND a.active_month = strftime(
            '%Y-%m',
            date(f.cohort_month || '-01', '+1 month')
       )
)
SELECT
    cohort_month,
    acquisition_channel,
    COUNT(*) AS cohort_user_count,
    SUM(month_1_retained) AS month_1_retained_users,
    ROUND(
        SUM(month_1_retained) * 100.0 / COUNT(*),
        2
    ) AS month_1_retention_rate
FROM retention_flags
GROUP BY
    cohort_month,
    acquisition_channel
ORDER BY
    cohort_month,
    acquisition_channel;
