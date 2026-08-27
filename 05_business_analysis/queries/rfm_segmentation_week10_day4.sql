WITH rfm_orders(
    order_id,
    user_id,
    order_date,
    order_status,
    net_sales
) AS (
    VALUES
        ('R001', 'U001', '2026-01-10', '已完成', 650.00),
        ('R002', 'U001', '2026-02-12', '已完成', 650.00),
        ('R003', 'U001', '2026-03-10', '已完成', 650.00),
        ('R004', 'U001', '2026-03-25', '已完成', 650.00),
        ('R005', 'U001', '2026-04-02', '已完成', 999.00),
        ('R006', 'U002', '2026-02-15', '已完成', 500.00),
        ('R007', 'U002', '2026-03-20', '已完成', 700.00),
        ('R008', 'U003', '2026-01-02', '已完成', 700.00),
        ('R009', 'U003', '2026-01-08', '已完成', 800.00),
        ('R010', 'U003', '2026-01-15', '已完成', 750.00),
        ('R011', 'U003', '2026-01-20', '已完成', 750.00),
        ('R012', 'U004', '2026-03-28', '已完成', 500.00),
        ('R013', 'U004', '2026-03-29', '已取消', 5000.00),
        ('R014', 'U005', '2026-01-18', '已完成', 200.00),
        ('R015', 'U005', '2026-03-10', '已完成', 400.00),
        ('R016', 'U006', '2026-01-15', '已完成', 2500.00),
        ('R017', 'U007', '2026-01-05', '已完成', 400.00),
        ('R018', 'U007', '2026-02-15', '已完成', 600.00),
        ('R019', 'U008', '2026-02-01', '已完成', 800.00),
        ('R020', 'U008', '2026-03-05', '已完成', 900.00),
        ('R021', 'U008', '2026-03-18', '已完成', 800.00),
        ('R022', 'U009', '2026-02-15', '已完成', 900.00),
        ('R023', 'U010', '2025-12-15', '已完成', 1000.00),
        ('R024', 'U010', '2026-01-10', '已完成', 400.00),
        ('R025', 'U010', '2026-01-30', '已完成', 500.00)
),
user_rfm AS (
    SELECT
        user_id,
        MAX(order_date) AS last_order_date,
        CAST(
            julianday('2026-04-01')
            - julianday(MAX(order_date))
            AS INTEGER
        ) AS recency_days,
        COUNT(DISTINCT order_id) AS frequency,
        ROUND(SUM(net_sales), 2) AS monetary
    FROM rfm_orders
    WHERE order_status = '已完成'
      AND order_date >= '2026-01-01'
      AND order_date < '2026-04-01'
    GROUP BY user_id
),
rfm_scores AS (
    SELECT
        *,
        CASE
            WHEN recency_days <= 30 THEN 3
            WHEN recency_days <= 60 THEN 2
            ELSE 1
        END AS r_score,
        CASE
            WHEN frequency >= 4 THEN 3
            WHEN frequency >= 2 THEN 2
            ELSE 1
        END AS f_score,
        CASE
            WHEN monetary >= 2000 THEN 3
            WHEN monetary >= 800 THEN 2
            ELSE 1
        END AS m_score
    FROM user_rfm
),
rfm_segments AS (
    SELECT
        *,
        CASE
            WHEN r_score = 3
             AND f_score >= 2
             AND m_score >= 2
                THEN '高价值活跃用户'
            WHEN r_score = 1
             AND f_score >= 2
             AND m_score >= 2
                THEN '高价值待唤回用户'
            WHEN r_score >= 2
             AND (f_score = 1 OR m_score = 1)
                THEN '潜力用户'
            ELSE '一般用户'
        END AS segment
    FROM rfm_scores
),
segment_summary AS (
    SELECT
        segment,
        COUNT(user_id) AS user_count,
        ROUND(SUM(monetary), 2) AS segment_monetary,
        ROUND(
            SUM(monetary) * 100.0
            / SUM(SUM(monetary)) OVER (),
            2
        ) AS monetary_share
    FROM rfm_segments
    GROUP BY segment
)
SELECT *
FROM segment_summary
ORDER BY monetary_share DESC;
