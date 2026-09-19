WITH refunds AS (
    SELECT
        order_id,
        ROUND(SUM(refund_amount), 2) AS total_refund_amount
    FROM course_refunds
    GROUP BY order_id
)
SELECT
    o.course_category,
    ROUND(
        SUM(o.paid_amount) - SUM(COALESCE(r.total_refund_amount, 0)),
        2
    ) AS net_revenue,
    COUNT(o.order_id) AS paid_order_count
FROM course_orders AS o
LEFT JOIN refunds AS r
    ON o.order_id = r.order_id
WHERE o.payment_status = '已支付'
GROUP BY o.course_category
ORDER BY net_revenue DESC;
