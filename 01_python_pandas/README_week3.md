# 第3周：pandas销售数据综合分析项目

## 项目目标

使用模拟电商订单数据，完成从业务问题定义、数据质量检查、清洗、指标计算、分组分析到业务报告输出的完整分析流程。

## 核心业务问题

1. 每个月哪个商品销量最高？
2. 哪个月实付销售额最高？
3. 不同城市和销售渠道的销售额、销量有什么差异？

## 数据字段

- order_id：订单编号
- order_date：订单日期
- city：城市
- channel：销售渠道
- product_name：商品名称
- category：商品类别
- quantity：销量
- unit_price：商品单价
- discount_rate：折扣率
- order_status：订单状态

## 指标口径

- 折前销售额 = 销量 × 商品单价
- 实付销售额 = 折前销售额 ×（1 - 折扣率）
- 正式销售订单 = 已完成且销量、单价、折扣率可以用于计算的订单
- 取消订单保留用于质量检查，但正式销售额记为0

## 数据质量处理

本项目处理或记录了以下问题：

- 完全重复订单
- 日期格式不统一
- 无效日期和日期缺失
- 销量中的“件”“缺货”和空值
- 单价中的“元”“价格待定”
- 百分比与小数形式混合的折扣率
- 折扣缺失
- 城市缺失
- 取消订单

对于无法确认真实值的字段，不随意使用平均值填充，而是保留原始值、记录问题，并按分析目的决定是否纳入统计。

## 核心结果

- 去重后订单：19笔
- 正式销售分析订单：15笔
- 月份分析订单：12笔
- 月份分析覆盖率：80%
- 有效订单总实付销售额：14234.15元
- 1月销量最高商品：无线鼠标，7件
- 2月销量最高商品：无线鼠标，6件
- 3月销量最高商品：蓝牙耳机，9件
- 月度销售额最高：2026年3月，6462.00元
- 已知城市中销售额最高：北京，3660.40元
- 销售额最高渠道：天猫，6830.65元，销量27件

## 分析限制

- 数据为小规模模拟数据。
- 月份分析未覆盖3笔无有效日期的销售订单。
- 1笔有效销售订单缺少城市，涉及1795.50元销售额。
- 1条折扣空值暂按0处理，仍需业务确认。
- 1笔已完成订单单价为“价格待定”，未计入正式销售额。

## 项目文件

### 数据

- `data/sales_dirty_week3.csv`

### 脚本

- `scripts/generate_sales_dirty.py`
- `scripts/sales_analysis_week3.py`

### 输出

- `outputs/sales_clean_week3.csv`
- `outputs/sales_valid_analysis_week3.csv`
- `outputs/monthly_top_product_week3.csv`
- `outputs/monthly_sales_summary_week3.csv`
- `outputs/city_sales_summary_week3.csv`
- `outputs/channel_sales_summary_week3.csv`
- `outputs/sales_analysis_report_week3.md`

## 运行方式

在项目根目录执行：

```powershell
python .\01_python_pandas\scripts\generate_sales_dirty.py
python .\01_python_pandas\scripts\sales_analysis_week3.py