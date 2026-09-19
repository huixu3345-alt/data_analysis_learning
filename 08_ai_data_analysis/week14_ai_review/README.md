# 第14周：AI辅助分析代码与结论审查

本作品用两组模拟数据，展示需求口径、AI初稿审查、人工修改和运行对账。重点是发现计算与解释问题，并用数据核对修正结果。

2026-09-19整理。五次课堂及W14-I有辅助完成；核心查询由学习者实际运行，截图随作品保存。教师完成输入准备、连接展示包装、归档及本次路径适配。当前能力记录为“能修改验证”，不记为从空白独立完成。

## 已验证结果

| 案例 | 分组结果 | 同范围总体核对 |
| --- | --- | --- |
| 渠道有效销售 | 天猫6830.65元/7笔；抖音4198.90元/4笔；京东3204.60元/4笔 | 14234.15元、15笔，两项差额均0；SQL与pandas一致 |
| 课程订单与退款 | BI 2250.00元/2笔；Python 1500.00元/2笔；SQL 900.00元/2笔 | 实付6000.00元－退款1350.00元＝净收入4650.00元、6笔；与类别合计差额均0 |

金额单位均为**元**。净销售额和退款后净收入均未扣除成本，不能据此判断哪个渠道或课程最赚钱。模拟数据不证明营销或页面改动的真实效果。

## 阅读顺序

1. [需求、数据粒度和指标口径](docs/requirements.md)
2. [问题、修正、结果及人工贡献](docs/review_report.md)
3. [AI辅助分析工作流](docs/ai_workflow.md)
4. [文件来源与SHA-256清单](manifest.json)

`cases/channel_sales`保存SQL和pandas的初稿、修正代码及冻结输入；`cases/course_sales`保存多次退款案例、修正查询和独立基准。`ai_draft`文件保留为错误审查样本，不能用于正式结果。`evidence`含8张学习者运行截图和2张教师图表前后对照。

## 复现方式

使用已安装pandas的Python环境。课堂实际环境为Windows、`D:\anaconda3\python.exe`、pandas 2.3.3；其他机器替换解释器和作品目录路径。依赖版本见[requirements.txt](requirements.txt)。

```powershell
Set-Location 'D:\data_analysis_learning\08_ai_data_analysis\week14_ai_review'
& 'D:\anaconda3\python.exe' '.\cases\channel_sales\run_query.py' 'missing_dates.sql'
& 'D:\anaconda3\python.exe' '.\cases\channel_sales\run_query.py' 'channel_summary.sql'
& 'D:\anaconda3\python.exe' '.\cases\channel_sales\run_query.py' 'overall_check.sql'
& 'D:\anaconda3\python.exe' '.\cases\channel_sales\channel_review.py'
& 'D:\anaconda3\python.exe' '.\cases\course_sales\run_query.py' 'refund_by_order.sql'
& 'D:\anaconda3\python.exe' '.\cases\course_sales\run_query.py' 'category_summary.sql'
& 'D:\anaconda3\python.exe' '.\cases\course_sales\run_query.py' 'order_baseline.sql'
& 'D:\anaconda3\python.exe' '.\cases\course_sales\run_query.py' 'refund_baseline.sql'
```

正常查询读取作品内冻结输入，SQLite连接为只读，结果打印在终端。课程输入已附齐，无需执行`create_fixture.py`；该文件保留教师生成数据的过程，并拒绝覆盖已有输入。

课堂查询及pandas逻辑已有学习者运行证据。本次整理只做复制指纹、源码抽取一致性、Python语法和文档链接检查；渠道pandas只适配输入路径，课程代码保持字节一致。新目录下的完整命令尚未另行执行，不把归档检查写成重新运行通过。

## 使用限制

总量对账确认本次合计一致，不能单独证明每条分类归属正确。现有输入已核对一行一笔订单，渠道字段在本样本无缺失；换数据时需重新检查订单唯一性、字段类型、缺失渠道和有效范围。`COUNT(sales_amount_valid)`须保留`WHERE sales_amount_valid = 1`才能符合本口径；课程退款基准JOIN依赖订单表中订单号唯一。

保留课堂四舍五入方式和浮点计算，不宣称为财务生产级精度方案。换数据时，分组后取两位再求和可能与总体最后取两位不同，应另行约定精度和核对规则。
