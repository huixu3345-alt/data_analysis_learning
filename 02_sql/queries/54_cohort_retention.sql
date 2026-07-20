WITH valid_user_months AS (
    SELECT DISTINCT
        user_id,
        order_month AS active_month
    FROM user_orders
    WHERE order_status = '已完成'
),

first_purchase AS (
    SELECT
        user_id,
        MIN(active_month) AS cohort_month
    FROM valid_user_months
    GROUP BY user_id
),

cohort_activity AS (
    SELECT
        v.user_id,
        f.cohort_month,

        (
            CAST(
                SUBSTR(v.active_month, 1, 4)
                AS INTEGER
            )
            -
            CAST(
                SUBSTR(f.cohort_month, 1, 4)
                AS INTEGER
            )
        ) * 12

        +

        (
            CAST(
                SUBSTR(v.active_month, 6, 2)
                AS INTEGER
            )
            -
            CAST(
                SUBSTR(f.cohort_month, 6, 2)
                AS INTEGER
            )
        ) AS month_number

    FROM valid_user_months AS v
    INNER JOIN first_purchase AS f
        ON v.user_id = f.user_id
),

cohort_sizes AS (
    SELECT
        cohort_month,
        COUNT(user_id) AS cohort_user_count
    FROM first_purchase
    GROUP BY cohort_month
)

SELECT
    a.cohort_month,
    a.month_number,
    s.cohort_user_count,

    COUNT(
        DISTINCT a.user_id
    ) AS retained_user_count,

    ROUND(
        COUNT(DISTINCT a.user_id)
        * 100.0
        / s.cohort_user_count,
        2
    ) AS retention_rate

FROM cohort_activity AS a
INNER JOIN cohort_sizes AS s
    ON a.cohort_month = s.cohort_month
GROUP BY
    a.cohort_month,
    a.month_number,
    s.cohort_user_count
ORDER BY
    a.cohort_month,
    a.month_number;