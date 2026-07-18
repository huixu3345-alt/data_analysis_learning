# 我的SQL分析速查表

## 1. 业务分析流程

拿到一个业务问题后，依次思考：

1. 数据来自哪些表？
2. 分析对象是什么？
3. 哪些数据可以参与指标计算？
4. 是否需要关联其他表？
5. 按什么维度分组？
6. 计算哪些指标？
7. 是否需要筛选分组结果？
8. 如何排序？
9. 分组结果能否与整体指标对上？
10. 数据覆盖率和结论限制是什么？

## 2. SQL查询骨架

    SELECT
        维度字段,
        聚合指标
    FROM 主表
    JOIN 其他表
        ON 关联条件
    WHERE 明细筛选条件
    GROUP BY 维度字段
    HAVING 分组筛选条件
    ORDER BY 指标 DESC
    LIMIT 返回数量;

并不是每条查询都需要使用全部语句。

## 3. 各语句的职责

- SELECT：选择需要显示的字段和指标
- FROM：指定数据来源
- JOIN：关联其他数据表
- ON：指定关联条件
- WHERE：分组前筛选订单明细
- GROUP BY：把相同维度的数据归为一组
- HAVING：分组后筛选统计结果
- ORDER BY：对查询结果排序
- LIMIT：限制返回行数

记忆方法：

WHERE筛选行，HAVING筛选组。

## 4. 常用筛选

空值：

    字段 IS NULL
    字段 IS NOT NULL

多个指定值：

    字段 IN ('值1', '值2')

范围：

    字段 BETWEEN 下限 AND 上限

包含文字：

    字段 LIKE '%关键词%'

多个条件：

    条件1 AND 条件2
    条件1 OR 条件2

## 5. 常用指标

订单数量：

    COUNT(order_id)

销售额：

    SUM(net_sales)

平均订单销售额：

    AVG(net_sales)

最大值和最小值：

    MAX(net_sales)
    MIN(net_sales)

保留两位小数：

    ROUND(指标, 2)

空值转换为0：

    COALESCE(指标, 0)

## 6. CASE WHEN分类

    CASE
        WHEN 条件1 THEN '类别1'
        WHEN 条件2 THEN '类别2'
        ELSE '其他'
    END AS 新字段名

CASE WHEN可以把连续指标转换为业务分类。

分类门槛变化会影响分组结果，但不会改变原始业务数据。

## 7. JOIN选择

INNER JOIN：

只保留两张表中能够匹配的数据。

LEFT JOIN：

保留左表全部数据。右表匹配不到时，右表字段显示为空。

如果需要保留没有订单的商品：

- product_info放在左边
- 使用LEFT JOIN
- 右表有效订单条件放在ON中

## 8. JOIN常见错误

统计订单数时：

    COUNT(s.order_id)

不要盲目使用：

    COUNT(*)

因为LEFT JOIN会为没有订单的左表数据保留一行。

如果需要保留零订单商品，有效订单条件应放在ON中。

条件放在WHERE中，可能会删除右表为空的记录，使LEFT JOIN失去保留作用。

## 9. 字段来源

订单信息通常来自sales_orders，别名为s：

- s.order_id
- s.order_date
- s.order_month
- s.channel
- s.quantity
- s.net_sales

商品标准资料来自product_info，别名为p：

- p.product_name
- p.standard_category
- p.standard_cost

两表通过以下条件关联：

    s.product_name = p.product_name

## 10. 当前有效订单定义

    s.order_status = '已完成'
    AND s.sales_amount_valid = 1

取消订单可以保留用于订单质量分析，但不能参与正式销售额指标。

## 11. 模拟成本和模拟毛利

模拟成本：

    s.quantity * p.standard_cost

模拟毛利：

    s.net_sales - s.quantity * p.standard_cost

模拟毛利率：

    模拟毛利 * 100.0 / 销售额

standard_cost为练习数据，且没有包含佣金、物流、仓储、广告和人工等费用，因此不能视为企业真实利润。

## 12. 一致性检查

每次分组分析后检查：

- 分组订单数合计是否等于整体订单数
- 分组销售额合计是否等于整体销售额
- 分组成本合计是否等于整体成本
- 分组模拟毛利合计是否等于整体模拟毛利

当前全部有效订单指标：

- 有效订单数：15
- 有效销售额：14234.15
- 模拟成本：7980.00
- 模拟毛利：6254.15

## 13. 数据覆盖率

- 日期有效订单：12条
- 日期覆盖率：80%
- 城市有效订单：14条
- 城市覆盖率：93.33%

月份分析只能使用日期有效的12条订单。

月份分析结果不能直接代表全部15条有效订单。

## 14. 业务结论结构

写分析结论时按照：

现象
→ 关键数字
→ 主要贡献者
→ 数据覆盖范围
→ 样本量和业务限制

不要因为样本中的现象，直接推断长期规律或因果关系。