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
)

SELECT
    v.user_id,
    f.cohort_month,
    v.active_month,

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
ORDER BY
    f.cohort_month,
    v.user_id,
    v.active_month;