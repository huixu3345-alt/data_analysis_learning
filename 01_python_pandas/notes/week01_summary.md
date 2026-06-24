我掌握了：

df.head()
df.shape
df.columns
df.dtypes
df.info()
df.describe()

我理解 DataFrame 可以看作一张表，Series 可以看作表中的一列。

Day 4：筛选、排序、列选择

我学习了：

df["name"]
df[["name", "python_score"]]
df[df["python_score"] >= 90]
df[(df["city"] == "Tokyo") & (df["python_score"] >= 86)]
df.sort_values(by="python_score", ascending=False)

我理解了：

单列选择和多列选择的区别
条件筛选会先得到一组 True / False
df[条件] 会保留 True 对应的行
& 表示多个条件同时成立
ascending=False 表示从高到低排序
Day 5：新增列和 groupby

我学习了新增列：

df["total_score"] = df["math_score"] + df["english_score"] + df["python_score"]
df["avg_score"] = df["total_score"] / 3

我学习了分组统计：

df.groupby("city")["avg_score"].mean()
df.groupby("gender")["python_score"].mean()

我还学习了 agg()，可以一次统计多个指标。

本周数据分析结果

基于 students.csv：

数据共有 8 行、8 列。
math_score 的平均值是 81.875。
python_score 的最高分是 95。
Osaka 和 Tokyo 的 avg_score 平均值相同，都是 87.777778。
Nagoya 的 avg_score_min 最低。
女生的 python_score 平均值是 85.25，男生是 83.75。
本周遇到的问题
一开始 PowerShell 找不到 python 命令。
虚拟环境 .venv 没有成功创建。
不理解 .gitignore 的作用。
不理解 pathlib 的作用。
不理解 pandas 输出中的 Name 和 dtype。
本周解决的问题
重新安装 Python，并勾选 Add python.exe to PATH。
在项目根目录创建并激活 .venv。
理解 .gitignore 是 Git 的忽略清单，用来避免提交 .venv 等文件。
理解 pathlib 是 Python 自带的路径处理工具。
理解 DataFrame 是表，Series 是一列。
我还需要继续熟悉
pandas 的中括号选择语法。
groupby 和 agg 的写法。
Series 和 DataFrame 的区别。
如何把分析结果整理成更清晰的报告。
下一周计划

第2周继续学习 pandas 数据清洗和 EDA，包括：

缺失值处理
重复值处理
字段类型转换
异常值观察
基础探索性分析