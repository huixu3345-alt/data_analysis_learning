WITH valid_purchases AS (
    SELECT
        user_id,
        order_month
    FROM user_orders
    WHERE order_status = '已完成'
),

user_cohorts AS (
    SELECT
        user_id,
        MIN(order_month) AS cohort_month
    FROM valid_purchases
    GROUP BY user_id
),

cohort_activity AS (
    SELECT DISTINCT
        v.user_id,
        c.cohort_month,
        v.order_month AS active_month,

        (
            CAST(SUBSTR(v.order_month, 1, 4) AS INTEGER)
            - CAST(SUBSTR(c.cohort_month, 1, 4) AS INTEGER)
        ) * 12
        +
        (
            CAST(SUBSTR(v.order_month, 6, 2) AS INTEGER)
            - CAST(SUBSTR(c.cohort_month, 6, 2) AS INTEGER)
        ) AS month_number

    FROM valid_purchases AS v
    INNER JOIN user_cohorts AS c
        ON v.user_id = c.user_id
),

data_range AS (
    SELECT
        MAX(order_month) AS latest_month
    FROM valid_purchases
),

cohort_summary AS (
    SELECT
        a.cohort_month,

        COUNT(
            DISTINCT CASE
                WHEN a.month_number = 0 THEN a.user_id
            END
        ) AS cohort_user_count,

        COUNT(
            DISTINCT CASE
                WHEN a.month_number = 1 THEN a.user_id
            END
        ) AS month_1_retained_users,

        COUNT(
            DISTINCT CASE
                WHEN a.month_number = 2 THEN a.user_id
            END
        ) AS month_2_retained_users,

        (
            CAST(SUBSTR(d.latest_month, 1, 4) AS INTEGER)
            - CAST(SUBSTR(a.cohort_month, 1, 4) AS INTEGER)
        ) * 12
        +
        (
            CAST(SUBSTR(d.latest_month, 6, 2) AS INTEGER)
            - CAST(SUBSTR(a.cohort_month, 6, 2) AS INTEGER)
        ) AS observable_months

    FROM cohort_activity AS a
    CROSS JOIN data_range AS d
    GROUP BY
        a.cohort_month,
        d.latest_month
)

SELECT
    cohort_month,
    cohort_user_count,

    CASE
        WHEN observable_months >= 1
        THEN month_1_retained_users
    END AS month_1_retained_users,

    CASE
        WHEN observable_months >= 1
        THEN ROUND(
            100.0 * month_1_retained_users / cohort_user_count,
            2
        )
    END AS month_1_retention_rate,

    CASE
        WHEN observable_months >= 2
        THEN month_2_retained_users
    END AS month_2_retained_users,

    CASE
        WHEN observable_months >= 2
        THEN ROUND(
            100.0 * month_2_retained_users / cohort_user_count,
            2
        )
    END AS month_2_retention_rate

FROM cohort_summary
ORDER BY cohort_month;