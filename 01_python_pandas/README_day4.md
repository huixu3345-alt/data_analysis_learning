# 第2周 Day4：描述性统计与组合分析

## 学习目标

本次学习在 Day3 清洗结果的基础上，使用 `describe()`、`value_counts()` 和多字段 `groupby()` 完成探索性分析，并将缺失值、重复值、字段类型、成绩范围和潜在异常值整合为数据质量检查报告。

## 输入数据

- `outputs/students_clean_day3.csv`

数据共有16行、16列。

## 本次学习内容

### 1. describe()

对以下成绩字段进行描述性统计：

- math
- english
- python
- total_score
- avg_score

主要指标包括：

- count：有效数据数量
- mean：平均值
- std：标准差
- min / max：最小值与最大值
- 25% / 50% / 75%：四分位数

### 2. value_counts()

检查以下类别字段的数量和比例：

- class_name
- gender
- is_pass
- enroll_month

使用 `dropna=False` 保留缺失值，避免数据质量问题被隐藏。

### 3. groupby() 组合分析

完成两组多维分析：

1. 班级 + 性别
2. 入学月份 + 班级

每个小组计算：

- 学生人数
- 平均成绩
- 通过率

### 4. 数据质量检查

检查内容包括：

- 字段缺失数量与缺失比例
- 整行重复
- 学生ID重复
- 成绩是否超出0到100分
- 数学成绩IQR潜在异常值
- 入学月份分析覆盖率

## 主要发现

1. 16名学生中有15人通过，通过率为93.75%。
2. 男女各8人，性别数量均衡。
3. B班女生组平均分最高，为88.16分。
4. A班女生组平均分和通过率相对较低，主要受到一名低分学生影响。
5. 只有12条记录具有有效入学月份，月份分析覆盖率为75%。
6. 三科成绩均处于0到100分的合法范围。
7. 数学45分被IQR规则标记为潜在异常值，但不能在没有核对原始记录的情况下直接删除。

## 分析限制

- 总样本只有16人。
- “班级 + 性别”小组只有2到4人。
- “月份 + 班级”小组只有1到2人。
- 4条记录缺少有效入学月份。

因此，本次结果用于描述当前样本和发现检查线索，不能证明性别、班级或入学月份导致了成绩差异。

## 输出文件

- `outputs/describe_summary_day4.csv`
- `outputs/category_distribution_day4.csv`
- `outputs/groupby_summary_day4.csv`
- `outputs/data_quality_report_day4.md`

## 运行方式

在项目根目录执行：

```powershell
python .\01_python_pandas\scripts\cleaning_eda_day4.py