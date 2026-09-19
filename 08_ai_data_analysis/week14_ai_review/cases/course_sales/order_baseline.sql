SELECT
    ROUND(SUM(o.paid_amount), 2) AS total_paid_amount,
    COUNT(o.order_id) AS paid_order_count
FROM course_orders AS o
WHERE o.payment_status = '已支付';
