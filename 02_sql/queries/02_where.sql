SELECT
    order_id,
    product_name,
    order_status,
    net_sales
FROM sales_orders
WHERE
    order_status = '已完成'
    AND sales_amount_valid = 1;