# 需求、输入与指标口径

## 渠道销售

问题：按渠道比较有效订单净销售额与有效订单量，量化差异，并将渠道合计与同范围总体核对。

输入为第12周清洗结果的冻结副本：[CSV](../cases/channel_sales/inputs/sales_clean_week12.csv)和[SQLite](../cases/channel_sales/inputs/sales_week12.db)。来源为仓库`06_data_warehouse/week12_pipeline/outputs`，未修改上游管道。两者均19行18字段，一行一笔订单、19个唯一订单号；SQLite表名`sales_orders`。

| 字段 | 含义/处理 |
| --- | --- |
| order_id | 订单标识，本输入唯一，但SQLite表没有主键约束 |
| channel | 渠道：天猫、抖音、京东 |
| order_date | 有效订单中3笔日期为空，本次不按日期筛选 |
| net_sales | 每笔订单净销售额，单位元，沿用上游清洗结果 |
| sales_amount_valid | SQLite为整数0/1；本CSV经课堂pandas读取为bool |

纳入SQLite标记为1、pandas标记为True的15笔订单。上游有效标记要求状态为已完成，数量、单价、折扣率非空；原始折扣缺失按0处理是练习假设。日期不属于本次有效判定条件。

净销售额为范围内`net_sales`总和；有效订单量为范围内订单行数。按渠道分组、金额展示两位小数；整体核对保持相同有效范围。

## 课程订单与退款

问题：按课程类别统计已支付订单量和退款后净收入，再独立从原表计算总体基准。

输入为教师提供的模拟[SQLite](../cases/course_sales/inputs/course_sales_review.db)、[订单CSV](../cases/course_sales/inputs/course_orders.csv)和[退款CSV](../cases/course_sales/inputs/course_refunds.csv)。完整字段与指纹见[输入清单](../cases/course_sales/inputs/manifest.json)。

| 表 | 粒度 | 规模 | 字段 |
| --- | --- | --- | --- |
| course_orders | 一行一笔订单 | 8行4列，order_id为主键 | order_id、course_category、payment_status、paid_amount |
| course_refunds | 一行一笔成功退款流水 | 6行3列，refund_id为主键 | refund_id、order_id、refund_amount |

同一订单可有多笔退款，原表关联是一对多。先按订单号聚合退款，再左连接订单，保留无退款订单并将其退款额按0处理。仅纳入`payment_status = '已支付'`的6笔；部分和全额退款的已支付订单仍计入订单量。没有日期条件，金额单位元。

退款后净收入＝已支付订单实付总额－这些订单对应的成功退款总额。实付金额与订单量直接从订单原表计算；退款基准从退款原表连接唯一订单表并筛选已支付范围，避免用同一个修正汇总查询自证。

本案例没有成本、营销曝光、访问和随机实验结果，不能判断利润、营销归因或页面改动效果。
