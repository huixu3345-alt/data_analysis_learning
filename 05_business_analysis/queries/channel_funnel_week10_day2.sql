WITH user_events(user_id, event_name, event_time, channel) AS (
    VALUES
        ('U01', 'visit',       '2026-01-05 09:00:00', '抖音'),
        ('U01', 'visit',       '2026-01-06 09:30:00', '天猫'),
        ('U01', 'add_to_cart', '2026-01-06 10:00:00', '天猫'),
        ('U01', 'add_to_cart', '2026-01-07 11:00:00', '天猫'),
        ('U02', 'visit',       '2026-01-07 12:00:00', '抖音'),
        ('U02', 'add_to_cart', '2026-01-16 12:00:00', '抖音'),
        ('U03', 'visit',       '2026-01-10 08:00:00', '天猫'),
        ('U03', 'add_to_cart', '2026-01-12 08:00:00', '天猫'),
        ('U04', 'visit',       '2026-01-12 13:00:00', '天猫'),
        ('U05', 'visit',       '2026-01-15 14:00:00', '京东'),
        ('U05', 'add_to_cart', '2026-01-15 14:30:00', '京东'),
        ('U06', 'visit',       '2026-01-18 15:00:00', '京东'),
        ('U06', 'add_to_cart', '2026-01-20 15:00:00', '京东'),
        ('U07', 'visit',       '2026-01-31 20:00:00', '天猫'),
        ('U07', 'add_to_cart', '2026-02-01 08:00:00', '天猫'),
        ('U01', 'visit',       '2026-02-02 09:00:00', '天猫'),
        ('U01', 'add_to_cart', '2026-02-03 09:00:00', '天猫'),
        ('U02', 'visit',       '2026-02-04 10:00:00', '抖音'),
        ('U03', 'visit',       '2026-02-05 11:00:00', '抖音'),
        ('U03', 'add_to_cart', '2026-02-10 11:00:00', '抖音'),
        ('U04', 'visit',       '2026-02-06 12:00:00', '天猫'),
        ('U05', 'visit',       '2026-02-07 13:00:00', '京东'),
        ('U05', 'add_to_cart', '2026-02-20 13:00:00', '京东'),
        ('U06', 'visit',       '2026-02-08 14:00:00', '京东'),
        ('U06', 'add_to_cart', '2026-02-14 14:00:00', '京东'),
        ('U08', 'add_to_cart', '2026-02-10 16:00:00', '天猫')
),
ranked_visits AS (
    SELECT
        user_id,
        event_time AS visit_time,
        channel AS visit_channel,
        ROW_NUMBER() OVER (
            PARTITION BY user_id, strftime('%Y-%m', event_time)
            ORDER BY event_time
        ) AS visit_rank
    FROM user_events
    WHERE event_name = 'visit'
),
visits AS (
    SELECT
        user_id,
        visit_time,
        visit_channel
    FROM ranked_visits
    WHERE visit_rank = 1
),
carts AS (
    SELECT
        user_id,
        event_time AS cart_time
    FROM user_events
    WHERE event_name = 'add_to_cart'
),
matched AS (
    SELECT
        v.user_id,
        v.visit_time,
        v.visit_channel,
        MIN(c.cart_time) AS first_cart_time
    FROM visits AS v
    LEFT JOIN carts AS c
        ON v.user_id = c.user_id
       AND c.cart_time >= v.visit_time
       AND c.cart_time <= datetime(v.visit_time, '+7 days')
    GROUP BY
        v.user_id,
        v.visit_time,
        v.visit_channel
)
SELECT
    strftime('%Y-%m', visit_time) AS visit_month,
    visit_channel,
    COUNT(*) AS visit_count,
    COUNT(first_cart_time) AS cart_count,
    ROUND(
        COUNT(first_cart_time) * 100.0 / COUNT(*),
        2
    ) AS visit_to_cart_rate
FROM matched
GROUP BY
    visit_month,
    visit_channel
ORDER BY
    visit_month,
    visit_channel;
