WITH category_sales AS (
    SELECT
        s.order_id,
        p.standard_category,
        s.product_name,
        s.net_sales,
        ROW_NUMBER() OVER (
            PARTITION BY p.standard_category
            ORDER BY s.net_sales DESC
        ) AS category_sales_rank
    FROM sales_orders AS s
    INNER JOIN product_info AS p
        ON s.product_name = p.product_name
    WHERE
        s.order_status = '已完成'
        AND s.sales_amount_valid = 1
)

SELECT
    order_id,
    standard_category,
    product_name,
    net_sales,
    category_sales_rank
FROM category_sales
WHERE category_sales_rank = 1
ORDER BY net_sales DESC;