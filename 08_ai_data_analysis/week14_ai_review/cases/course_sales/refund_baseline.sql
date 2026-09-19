SELECT
    ROUND(SUM(r.refund_amount), 2) AS total_refund_amount
FROM course_refunds AS r
JOIN course_orders AS o
    ON o.order_id = r.order_id
WHERE o.payment_status = '已支付';
