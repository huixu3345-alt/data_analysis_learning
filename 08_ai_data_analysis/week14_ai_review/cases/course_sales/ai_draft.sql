-- W14-I: AI draft for learner review; not validated or an accepted solution.
SELECT
    o.course_category,
    ROUND(
        SUM(o.paid_amount) - SUM(COALESCE(r.refund_amount, 0)),
        2
    ) AS net_revenue,
    COUNT(o.order_id) AS paid_order_count
FROM course_orders AS o
LEFT JOIN course_refunds AS r
    ON o.order_id = r.order_id
WHERE o.payment_status = '已支付'
GROUP BY o.course_category
ORDER BY net_revenue DESC;
