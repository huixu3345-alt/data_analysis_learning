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