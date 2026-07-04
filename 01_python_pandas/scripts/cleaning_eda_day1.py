from pathlib import Path
import pandas as pd

# =========================
# 1. 设置文件路径
# =========================

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "students_dirty.csv"
OUTPUT_PATH = BASE_DIR / "outputs" / "cleaning_summary_day1.md"

# =========================
# 2. 读取数据
# =========================

df = pd.read_csv(DATA_PATH)

print("===== 原始数据前5行 =====")
print(df.head())

print("\n===== 数据基本信息 =====")
df.info()

print("\n===== 数值字段统计 =====")
print(df.describe())

# =========================
# 3. 检查缺失值
# =========================

print("\n===== 每一列缺失值数量 =====")
missing_count = df.isnull().sum()
print(missing_count)

print("\n===== 每一列缺失值比例 =====")
missing_rate = df.isnull().mean()
print(missing_rate)

# =========================
# 4. 查看包含缺失值的行
# =========================

rows_with_missing = df[df.isnull().any(axis=1)]

print("\n===== 存在缺失值的学生记录 =====")
print(rows_with_missing)

# =========================
# 5. 缺失值处理方式一：删除缺失行
# =========================

df_dropna = df.dropna()

print("\n===== 删除缺失值后的数据 =====")
print(df_dropna)

print("\n删除前行数：", len(df))
print("删除后行数：", len(df_dropna))

# =========================
# 6. 缺失值处理方式二：填充缺失值
# =========================

df_fillna = df.copy()

score_cols = ["math", "english", "python"]

for col in score_cols:
    df_fillna[col] = df_fillna[col].fillna(df_fillna[col].mean())

df_fillna["enroll_date"] = df_fillna["enroll_date"].fillna("未知日期")

print("\n===== 填充缺失值后的数据 =====")
print(df_fillna)

print("\n===== 填充后缺失值检查 =====")
print(df_fillna.isnull().sum())

# =========================
# 7. 新增总分和平均分
# 回忆第1周：新增字段
# =========================

df_fillna["total_score"] = df_fillna[score_cols].sum(axis=1)
df_fillna["avg_score"] = df_fillna[score_cols].mean(axis=1).round(2)

print("\n===== 新增总分和平均分 =====")
print(df_fillna[["name", "class_name", "math", "english", "python", "total_score", "avg_score"]])

# =========================
# 8. 按班级分组统计
# 回忆第1周：groupby
# =========================

class_summary = df_fillna.groupby("class_name").agg(
    student_count=("student_id", "count"),
    avg_math=("math", "mean"),
    avg_english=("english", "mean"),
    avg_python=("python", "mean"),
    avg_score=("avg_score", "mean")
).round(2).reset_index()

print("\n===== 按班级统计平均成绩 =====")
print(class_summary)

# =========================
# 9. 输出简单数据质量报告
# =========================

OUTPUT_PATH.parent.mkdir(exist_ok=True)

summary_text = f"""# 第2周 Day 1 数据质量检查报告

## 一、数据背景

本次练习使用 students_dirty.csv，模拟真实数据中常见的缺失值问题。

## 二、原始数据规模

- 原始数据行数：{len(df)}
- 原始数据列数：{df.shape[1]}

## 三、缺失值检查结果

每列缺失值数量如下：

{missing_count.to_string()}

## 四、发现的问题

1. 英语、数学、Python成绩中存在缺失值。
2. enroll_date 入学日期字段存在缺失值。
3. 如果直接删除所有缺失行，会导致样本数量减少。
4. 如果直接用平均值填充成绩，需要在报告中说明处理逻辑。

## 五、处理方法

本次练习采用以下处理方式：

1. 成绩类字段使用该字段平均值填充。
2. 日期字段 enroll_date 使用“未知日期”填充。
3. 填充后重新计算 total_score 和 avg_score。
4. 使用 groupby 按班级统计平均成绩。

## 六、初步结论

1. 缺失值会影响总分、平均分和班级统计结果。
2. 缺失值不能盲目删除，需要根据字段含义决定处理方式。
3. 数据清洗是分析前的必要步骤，否则后续结论可能不可靠。
"""

OUTPUT_PATH.write_text(summary_text, encoding="utf-8")

print(f"\n数据质量报告已生成：{OUTPUT_PATH}")