# 第1周：Python基础 + pandas入门

## 学习目标

本周目标是掌握 Python 基础语法，并使用 pandas 完成最基础的数据读取、查看、筛选、排序、新增列和分组统计。

本阶段使用模拟学生成绩数据 `students.csv` 进行练习。

## 使用工具

* Python
* pandas
* VS Code
* PowerShell
* Git / GitHub

## 目录结构

```text
01_python_pandas/
├── README.md
├── data/
│   └── students.csv
├── scripts/
│   ├── day01_python_basics.py
│   └── pandas_basic.py
├── notes/
│   ├── day01_python_basics.md
│   ├── day02_students_csv.md
│   ├── day03_pandas_read_csv.md
│   ├── day04_filter_sort_select.md
│   └── day05_new_columns_groupby.md
├── notebooks/
└── outputs/
```

## 数据说明

数据文件：

```text
data/students.csv
```

字段说明：

| 字段名           | 含义        |
| ------------- | --------- |
| student_id    | 学生编号      |
| name          | 学生姓名      |
| gender        | 性别        |
| age           | 年龄        |
| city          | 城市        |
| math_score    | 数学成绩      |
| english_score | 英语成绩      |
| python_score  | Python 成绩 |

这是一份模拟学生成绩数据，共 8 行、8 列。

## 学习进度

* [x] Day 1：Python基础
* [x] Day 2：创建 students.csv
* [x] Day 3：pandas读取CSV
* [x] Day 4：筛选、排序、列选择
* [x] Day 5：新增列和 groupby
* [x] Day 6：整理 README
* [x] Day 7：提交 GitHub 和本周总结

## 核心学习内容

### Day 1：Python基础

学习内容：

* 变量
* 列表
* 字典
* if / elif / else 条件判断
* for 循环
* def 函数
* return 返回值

练习内容：

* 根据分数返回 A、B、C、D 等级
* 理解列表索引从 0 开始
* 理解字典中的键值对

### Day 2：CSV 数据结构

学习内容：

* CSV 是用逗号分隔的表格文件
* 第一行通常是字段名
* 从第二行开始，每一行是一条数据记录

核心概念：

* 行 row
* 列 column
* 字段 field
* 值 value

### Day 3：pandas 读取 CSV

学习内容：

```python
df = pd.read_csv(csv_path)
df.head()
df.shape
df.columns
df.dtypes
df.info()
df.describe()
```

理解内容：

* DataFrame 可以理解成 pandas 中的一张表
* Series 可以理解成 DataFrame 中的一列
* `head()` 默认查看前 5 行
* `shape` 查看行数和列数
* `info()` 查看字段、非空数量和数据类型
* `describe()` 查看数值列统计信息

### Day 4：筛选、排序、列选择

学习内容：

```python
df["name"]
df[["name", "python_score"]]
df[df["python_score"] >= 90]
df[(df["city"] == "Tokyo") & (df["python_score"] >= 86)]
df.sort_values(by="python_score", ascending=False)
```

理解内容：

* 一个中括号选择单列
* 两个中括号选择多列
* 条件筛选会先得到一组 True / False
* `df[条件]` 会保留条件为 True 的行
* `ascending=False` 表示从高到低排序

### Day 5：新增列和 groupby 分组统计

学习内容：

```python
df["total_score"] = df["math_score"] + df["english_score"] + df["python_score"]
df["avg_score"] = df["total_score"] / 3

df.groupby("city")["avg_score"].mean()
df.groupby("gender")["python_score"].mean()
df.groupby("city").agg(
    student_count=("student_id", "count"),
    avg_score_mean=("avg_score", "mean"),
    avg_score_max=("avg_score", "max"),
    avg_score_min=("avg_score", "min")
)
```

理解内容：

* `df["新列名"] = ...` 可以新增列
* `groupby()` 用来分组
* `mean()` 用来计算平均值
* `count()` 用来计数
* `agg()` 可以一次性计算多个统计指标

## 当前练习结论

基于 `students.csv` 的练习结果：

1. `students.csv` 一共有 8 行学生数据、8 个字段。
2. `math_score` 的平均值是 81.875。
3. `python_score` 的最高分是 95。
4. Osaka 和 Tokyo 的 `avg_score` 平均值相同，都是 87.777778。
5. Nagoya 的 `avg_score_min` 最低。
6. 女生的 `python_score` 平均值是 85.25，男生的 `python_score` 平均值是 83.75。

## 遇到的问题与解决方法

### 1. Python 环境问题

问题：PowerShell 中一开始无法识别 `python` 命令。

解决：重新安装 Python，并确认安装时勾选 `Add python.exe to PATH`。

### 2. 虚拟环境问题

问题：一开始找不到 `.venv\Scripts\Activate.ps1`。

解决：在项目根目录重新创建 `.venv`，并用 PowerShell 激活虚拟环境。

### 3. pandas 输出中的省略号

问题：`df.head()` 或 `df.describe()` 中间出现 `...`。

理解：这是 pandas 为了适应终端宽度自动省略显示，不代表数据丢失。

### 4. Series 输出中的 Name 和 dtype

问题：输出布尔条件时出现：

```text
Name: python_score, dtype: bool
```

理解：这是 pandas 在说明当前结果是一个 Series，名字是 `python_score`，数据类型是布尔值。

## 下一步计划

第1周 Day 7 将进行本周总结，检查代码和 README，并提交 GitHub。

第2周将继续学习 pandas 数据清洗和探索性分析，包括缺失值、重复值、字段类型转换和基础 EDA。
