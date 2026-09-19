SELECT
    order_id,
    ROUND(SUM(refund_amount), 2) AS total_refund_amount
FROM course_refunds
GROUP BY order_id;
