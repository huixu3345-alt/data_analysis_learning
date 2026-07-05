# 第2周 Day3：字段类型转换与日期字段处理总结

## 1. 今日主线

数据质量 → 字段类型 → 日期处理 → 指标计算 → 分组分析 → 业务结论 → GitHub 项目资产

## 2. 原始数据质量发现

- 原始数据行数：16 行。
- 原始数据统一按字符串读取，目的是先暴露字段类型问题，而不是一开始就假设字段可信。
- 字段转换前缺失值数量如下：

| field       |   missing_count_before_conversion |
|:------------|----------------------------------:|
| student_id  |                                 0 |
| name        |                                 0 |
| class_name  |                                 0 |
| gender      |                                 0 |
| math        |                                 0 |
| english     |                                 2 |
| python      |                                 0 |
| enroll_date |                                 1 |

## 3. 字段类型转换结果

| field       | type_before   | type_after     |
|:------------|:--------------|:---------------|
| student_id  | string        | Int64          |
| name        | string        | string         |
| class_name  | string        | category       |
| gender      | string        | category       |
| math        | string        | Float64        |
| english     | string        | Int64          |
| python      | string        | Int64          |
| enroll_date | string        | datetime64[ns] |

关键理解：字段类型不正确，后面的排序、求和、平均值、月份分析都可能失真。比如成绩字段如果还是字符串，`"100"` 和 `"59"` 的排序可能不是业务想要的数值排序。

## 4. 数值字段转换问题

本次发现无法直接转换为数字的成绩记录数量：2。

| field   |   student_id | name   | class_name   | raw_value   |
|:--------|-------------:|:-------|:-------------|:------------|
| math    |            4 | 赵六   | B班          | 缺考        |
| python  |            6 | 孙八   | C班          | 优秀        |

处理策略：

1. 先把成绩里的“分”等单位去掉。
2. 使用 `pd.to_numeric(errors="coerce")` 把无法转换的内容变成 NaN。
3. 用每科中位数填充转换失败后的缺失值。
4. 再重新计算 `total_score` 和 `avg_score`。

## 5. 日期字段处理结果

- 可成功转换的日期数量：12。
- 无法成功转换或为空的日期数量：4。

|   student_id | name   | class_name   | enroll_date_raw   |
|-------------:|:-------|:-------------|:------------------|
|            8 | 吴十   | B班          | 2026-04-31        |
|           10 | 王十二 | C班          | not_a_date        |
|           12 | 陈十四 | A班          | <NA>              |
|           16 | 沈十八 | C班          | 2026-02-30        |

处理策略：

1. 先统一日期格式，把 `/`、`.`、`年/月/日` 转成接近 `YYYY-MM-DD` 的格式。
2. 使用 `pd.to_datetime(errors="coerce")` 转换为 datetime。
3. 转换失败的日期会变成 `NaT`，可以理解为日期字段里的缺失值。
4. 本次不随意填充日期，因为真实业务中错误日期可能影响趋势分析，应回查数据来源。

## 6. 日期信息提取

本次新增字段：

- `enroll_year`：入学年份
- `enroll_month_num`：入学月份数字
- `enroll_day`：入学日
- `enroll_month`：用于按月分析的年月字段，例如 `2026-03`

## 7. 按月份分组统计

| enroll_month   |   student_count |   avg_math |   avg_english |   avg_python |   avg_score |   pass_rate |
|:---------------|----------------:|-----------:|--------------:|-------------:|------------:|------------:|
| 2026-03        |               4 |      84.75 |         84    |        84    |       84.25 |      100    |
| 2026-04        |               3 |      81.67 |         83.67 |        80.67 |       82    |      100    |
| 2026-05        |               2 |      88    |         89.5  |        92    |       89.83 |      100    |
| 2026-06        |               3 |      77.83 |         81.33 |        82.33 |       80.5  |       66.67 |

## 8. 按班级分组统计

| class_name   |   student_count |   avg_score |   pass_rate |
|:-------------|----------------:|------------:|------------:|
| A班          |               6 |       75.95 |       83.33 |
| B班          |               5 |       85.07 |      100    |
| C班          |               5 |       83.3  |      100    |

## 9. 初步业务结论

1. 平均成绩最高的入学月份是 2026-05，平均分为 89.83。
2. 平均成绩最低的入学月份是 2026-06，平均分为 80.5。
3. 日期字段里存在无法转换的记录，本次已从月份统计中排除，避免错误日期污染时间趋势。
4. 成绩字段里存在“缺考”“优秀”等非标准数值，这类问题在真实业务中对应“字段口径不统一”，需要推动数据录入规则标准化。
5. 清洗后再计算总分、平均分和通过率，比直接在原始数据上计算更可靠。

## 10. GitHub 资产说明

本次建议提交以下文件：

- `data/students_dirty_day3.csv`：字段类型与日期字段脏数据练习集
- `scripts/cleaning_eda_day3.py`：可从头运行的数据清洗脚本
- `outputs/students_clean_day3.csv`：清洗后的明细数据
- `outputs/monthly_summary_day3.csv`：按月份统计结果
- `outputs/class_summary_day3.csv`：按班级统计结果
- `outputs/cleaning_summary_day3.md`：本报告

## 11. 今日一句话总结

Day3 的核心不是记住 `astype()` 或 `pd.to_datetime()`，而是理解：字段类型决定指标能不能正确计算，日期字段决定能不能做趋势分析；数据分析师必须先让数据可信，再谈业务结论。


<!-- 这份代码先读取学生成绩脏数据，并且故意把所有字段按字符串读取，方便暴露字段类型问题。然后通过 normalize_blank_values() 去除空格，并把 N/A、not_available、空字符串统一处理成缺失值。

接着代码把 student_id 转成整数，把班级和性别转成 category。对于 math、english、python 三个成绩字段，先去掉“分”这个单位，再用 pd.to_numeric(errors="coerce") 转成数字，无法转换的“缺考”“优秀”会变成 NaN，并被记录到 score_issues 表里。

日期字段 enroll_date 会先统一格式，把 /、.、年、月、日 替换成标准格式，再用 pd.to_datetime(errors="coerce") 转成日期。无法转换的日期，比如 2026-04-31、2026-02-30、not_a_date，会变成 NaT，并被记录到 invalid_date_rows 表里。

之后代码用每科中位数填充成绩缺失值，再从日期中提取年份、月份、日期和年月字段。最后重新计算总分、平均分、是否通过，并分别按月份和班级进行分组统计，输出清洗后的明细数据、分组结果和 Markdown 报告。 -->