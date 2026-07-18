SELECT
    COUNT(*) AS valid_order_count,

    SUM(
        CASE
            WHEN order_date IS NOT NULL THEN 1
            ELSE 0
        END
    ) AS valid_date_count,

    ROUND(
        SUM(
            CASE
                WHEN order_date IS NOT NULL THEN 1
                ELSE 0
            END
        ) * 100.0 / COUNT(*),
        2
    ) AS date_coverage_rate,

    SUM(
        CASE
            WHEN city IS NOT NULL THEN 1
            ELSE 0
        END
    ) AS valid_city_count,

    ROUND(
        SUM(
            CASE
                WHEN city IS NOT NULL THEN 1
                ELSE 0
            END
        ) * 100.0 / COUNT(*),
        2
    ) AS city_coverage_rate

FROM sales_orders
WHERE
    order_status = '已完成'
    AND sales_amount_valid = 1;