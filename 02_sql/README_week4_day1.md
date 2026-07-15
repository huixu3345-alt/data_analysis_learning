# 第4周 Day1：SQL基础查询

## 学习目标

使用 SQLite 和第3周销售数据，学习 SQL 基础查询语法，并将 SQL 结果与 pandas 分析结果进行核对。

## 数据库

- 数据库文件：`data/sales_week4.db`
- 数据表：`sales_orders`
- 数据行数：19行
- 数据来源：第3周清洗后的销售订单数据

## 核心语法

### SELECT 和 FROM

```sql
SELECT
    order_id,
    product_name,
    net_sales
FROM sales_orders;
```

- `SELECT`：选择需要显示的字段。
- `FROM`：指定数据来源表。

### WHERE 和 AND

```sql
WHERE
    order_status = '已完成'
    AND sales_amount_valid = 1
```

- `WHERE`：筛选订单明细。
- `AND`：要求多个条件同时满足。
- SQL 判断相等使用单个 `=`。
- 文本值需要使用单引号。

### ORDER BY 和 LIMIT

```sql
ORDER BY
    net_sales DESC
LIMIT 5;
```

- `ORDER BY`：对查询结果排序。
- `DESC`：从大到小降序排列。
- `ASC`：从小到大升序排列。
- `LIMIT`：限制返回行数。
- 应先排序再限制行数，才能得到真正的前N名。

### DISTINCT

```sql
SELECT DISTINCT
    channel
FROM sales_orders;
```

- `DISTINCT`：去除查询结果中的重复值。
- 它不会删除数据库中的原始订单。

### 聚合函数

```sql
SELECT
    COUNT(*) AS order_count,
    SUM(quantity) AS total_quantity,
    ROUND(SUM(net_sales), 2) AS total_net_sales,
    ROUND(AVG(net_sales), 2) AS avg_order_sales,
    MIN(net_sales) AS min_order_sales,
    MAX(net_sales) AS max_order_sales
FROM sales_orders
WHERE
    order_status = '已完成'
    AND sales_amount_valid = 1;
```

常用聚合函数：

- `COUNT()`：统计数量。
- `SUM()`：计算合计。
- `AVG()`：计算平均值。
- `MIN()`：查找最小值。
- `MAX()`：查找最大值。
- `ROUND()`：控制小数位。
- `AS`：为结果字段设置别名。

### GROUP BY

```sql
SELECT
    channel,
    COUNT(*) AS order_count,
    SUM(quantity) AS total_quantity,
    ROUND(SUM(net_sales), 2) AS total_net_sales
FROM sales_orders
WHERE
    order_status = '已完成'
    AND sales_amount_valid = 1
GROUP BY
    channel;
```

- `GROUP BY`：按指定字段分组。
- 分组后，每个渠道返回一行汇总结果。
- 不使用 `GROUP BY` 的聚合查询，通常只返回一行整体指标。

### WHERE 和 HAVING 的区别

```sql
SELECT
    channel,
    COUNT(*) AS order_count,
    SUM(quantity) AS total_quantity,
    ROUND(SUM(net_sales), 2) AS total_net_sales
FROM sales_orders
WHERE
    order_status = '已完成'
    AND sales_amount_valid = 1
GROUP BY
    channel
HAVING
    SUM(net_sales) > 4000
ORDER BY
    total_net_sales DESC;
```

- `WHERE`：在分组前筛选订单明细。
- `HAVING`：在分组后筛选汇总结果。
- `WHERE order_status = '已完成'` 是单笔订单条件。
- `HAVING SUM(net_sales) > 4000` 是渠道汇总条件。

## SQL书写顺序

基础查询的常见书写顺序：

```text
SELECT
FROM
WHERE
GROUP BY
HAVING
ORDER BY
LIMIT
```

可以简单理解为：

```text
从哪张表取数据
→ 筛选哪些明细
→ 如何分组
→ 筛选哪些分组
→ 显示哪些字段和指标
→ 如何排序
→ 返回多少行
```

## 查询文件

- `queries/01_select_basic.sql`：基础字段选择和 `LIMIT`
- `queries/02_where.sql`：有效订单筛选
- `queries/03_order_by.sql`：销售额排序
- `queries/04_distinct.sql`：渠道去重
- `queries/05_aggregate.sql`：整体指标汇总
- `queries/06_groupby_having.sql`：渠道分组和 `HAVING`
- `queries/07_independent_practice.sql`：独立筛选练习

## 核心验证结果

- 数据库订单数：19笔
- 正式有效销售订单：15笔
- 有效订单总销量：67件
- 有效订单总实付销售额：14234.15元
- 最低单笔销售额：348.30元
- 最高单笔销售额：1795.50元

渠道销售额：

- 天猫：6830.65元
- 抖音：4198.90元
- 京东：3204.60元

SQL 查询结果与第3周 pandas 分析结果一致。

## 独立练习

业务问题：

> 查询有效销售订单中，实付销售额大于1000元的订单，显示订单编号、商品名称、城市、渠道和实付销售额，并按照实付销售额从高到低排序。

SQL：

```sql
SELECT
    order_id,
    product_name,
    city,
    channel,
    net_sales
FROM sales_orders
WHERE
    order_status = '已完成'
    AND sales_amount_valid = 1
    AND net_sales > 1000
ORDER BY
    net_sales DESC;
```

查询结果共返回7笔订单。

## 项目结构

```text
02_sql/
├── data/
│   └── sales_week4.db
├── outputs/
├── queries/
│   ├── 01_select_basic.sql
│   ├── 02_where.sql
│   ├── 03_order_by.sql
│   ├── 04_distinct.sql
│   ├── 05_aggregate.sql
│   ├── 06_groupby_having.sql
│   └── 07_independent_practice.sql
├── scripts/
│   ├── setup_sales_database.py
│   └── run_sql_query.py
└── README_week4_day1.md
```

## 运行方式

### 重新创建数据库

在项目根目录执行：

```powershell
python .\02_sql\scripts\setup_sales_database.py
```

### 选择要运行的SQL文件

在 `run_sql_query.py` 中修改：

```python
QUERY_FILE_NAME = "07_independent_practice.sql"
```

### 执行SQL查询

```powershell
python .\02_sql\scripts\run_sql_query.py
```

## 常见易错点

1. 订单编号 `O1019` 的开头是字母 `O`，不是数字 `0`。
2. SQL 相等判断使用单个 `=`。
3. 文本值需要使用单引号，例如 `'已完成'`。
4. `WHERE` 筛选明细，`HAVING` 筛选分组结果。
5. 查询订单明细时使用 `order_id`。
6. `order_count` 是聚合查询中通过 `AS` 创建的别名，不是原始字段。
7. 先使用 `ORDER BY` 排序，再使用 `LIMIT`，才能得到真正的前N名。
8. `DISTINCT` 只去除查询结果中的重复值，不删除数据库记录。
9. 没有 `GROUP BY` 的聚合查询通常只返回一行。
10. 数据库中的 `NULL` 表示缺失值，例如城市显示为 `None`。

## 一句话总结

先用 `WHERE` 确定正确的数据范围，再使用聚合、分组和排序回答业务问题；SQL结果还应与整体指标及其他分析工具进行核对。