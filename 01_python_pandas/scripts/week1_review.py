import pandas as pd
from pathlib import Path
# 1. 读取数据
script_path = Path(__file__).resolve()
week_dir = script_path.parents[1]
csv_path = week_dir / "data" / "students.csv"
df = pd.read_csv(csv_path)

# 2. 查看数据
print("前5行数据：")
print(df.head())

print("数据结构：")
print(df.info())

print("数值统计：")
print(df.describe())

# 3. 查看行列数量
print("数据行列数：")
print(df.shape)

# 4. 选择部分列
print("查看姓名、城市和成绩列：")
print(df[["name", "city", "math_score", "english_score", "python_score"]])

# 5. 筛选：找出 Python 成绩大于等于 90 的学生
high_python = df[df["python_score"] >= 90]
print("Python 成绩 >= 90 的学生：")
print(high_python)

# 6. 筛选：找出数学成绩低于 70 的学生
low_math = df[df["math_score"] < 70]
print("数学成绩低于 70 的学生：")
print(low_math)

# 7. 新增总分和平均分
score_cols = ["math_score", "english_score", "python_score"]

df["total_score"] = df[score_cols].sum(axis=1)
df["avg_score"] = df[score_cols].mean(axis=1).round(2)

print("新增总分和平均分后的数据：")
print(df.head())

# 8. 按平均分从高到低排序
df_sorted = df.sort_values("avg_score", ascending=False)
print("按平均分从高到低排序：")
print(df_sorted)

# 9. 按城市分组统计
city_summary = df.groupby("city").agg(
    student_count=("name", "count"),
    avg_math=("math_score", "mean"),
    avg_english=("english_score", "mean"),
    avg_python=("python_score", "mean"),
    avg_total=("total_score", "mean")
).reset_index()

print("按城市统计结果：")
print(city_summary)

# 10. 按平均总分排序城市
city_summary_sorted = city_summary.sort_values("avg_total", ascending=False)
print("城市平均总分排名：")
print(city_summary_sorted)