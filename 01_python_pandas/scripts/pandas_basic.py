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
print(sorted_by_english[["name", "english_score","city"]] )

print("-" * 50)

print("城市是 Osaka 且 Python 成绩大于等于 80 的学生:")

osaka_high_python = df[(df["city"] == "Osaka") & (df["python_score"] >= 80)]
print(osaka_high_python[["name", "city", "python_score"]])

print("-" * 50)

print("新增 total_score 和 avg_score:")

df["total_score"] = df["math_score"] + df["english_score"] + df["python_score"]

df["avg_score"] = df["total_score"] / 3

print(df[["name", "math_score", "english_score", "python_score", "total_score", "avg_score"]])      

print("-" * 50)

print("按城市统计平均分:")

city_avg_score = df.groupby("city")["avg_score"].mean()

print(city_avg_score)

print("-" * 50)

print("按性别统计平均分:")

gender_avg_score = df.groupby("gender")["avg_score"].mean()

print(gender_avg_score)

print("-" * 50)

print("按城市统计学生人数:")

city_student_count = df.groupby("city")["student_id"].count()

print(city_student_count)

print("-" * 50)

print("按 gender 分组，统计每个性别的 python_score 平均值:")

gender_avg_python_score = df.groupby("gender")["python_score"].mean()
print(gender_avg_python_score)  

print("-" * 50)

print("按城市统计学生人数、平均分、最高分、最低分:")

city_summary = df.groupby("city").agg(
    student_count=("student_id", "count"),
    avg_score_mean=("avg_score", "mean"),
    avg_score_max=("avg_score", "max"),
    avg_score_min=("avg_score", "min")
)

print(city_summary)