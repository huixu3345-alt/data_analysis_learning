SELECT order_id, channel, order_date
FROM sales_orders
WHERE order_date IS NULL AND sales_amount_valid = 1;
