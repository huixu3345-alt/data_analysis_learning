from pathlib import Path
import pandas as pd

script_path = Path(__file__).resolve()
week_dir = script_path.parents[1]
csv_path = week_dir / "data" / "students.csv"

df = pd.read_csv(csv_path)

print(df.head())

print("-" * 50)

print("数据形状:")
print(df.shape)

print("-" * 50)

print("列名:")
print(df.columns)

print("-" * 50)

print("数据类型:")
print(df.dtypes)

print("-" * 50)

print("数据基本信息:")
df.info()

print("-" * 50)

print("数值列统计:")
print(df.describe())

print("-" * 50)

print("math_score 平均值:")
print(df["math_score"].mean())

print("python_score 最高分:")
print(df["python_score"].max())

print("-" * 50)

print("只查看 name 列:")
print(df["name"])

print("-" * 50)

print("查看 name 和 python_score 两列:")
print(df[["name", "python_score"]])

print("-" * 50)

print("Python成绩大于等于90的学生:")
high_python_students = df[df["python_score"] >= 90]
print(high_python_students)

print("-" * 50)

print("Python成绩是否大于等于90:")
python_score_mask = df["python_score"] >= 90
print(python_score_mask)

print("-" * 50)

print("Python成绩大于等于90的学生姓名和成绩:")
high_python_students = df[python_score_mask]
print(high_python_students[["name", "python_score"]])

print("-" * 50)

print("按照 Python 成绩从高到低排序:")
sorted_by_python = df.sort_values(by="python_score", ascending=False)
print(sorted_by_python[["name", "python_score"]])

print("-" * 50)

print("城市是 Tokyo 且 Python 成绩大于等于86的学生:")

tokyo_high_python = df[
    (df["city"] == "Tokyo") & (df["python_score"] >= 86)
]

print(tokyo_high_python[["name", "city", "python_score"]])

print("-" * 50)

print("math成绩大于等于85的学生姓名和成绩:")
high_math_students = df[df["math_score"] >= 85]
print(high_math_students[["name", "math_score","city"]])

print("-" * 50)

print("按照 english 成绩从高到低排序:")
sorted_by_english = df.sort_values(by="english_score", ascending=False)
print(sorted_by_english[["name", "english_score"]] )

print("-" * 50)

print("城市是 Osaka 且 Python 成绩大于等于 80 的学生:")

osaka_high_python = df[(df["city"] == "Osaka") & (df["python_score"] >= 80)]
print(osaka_high_python[["name", "city", "python_score"]])