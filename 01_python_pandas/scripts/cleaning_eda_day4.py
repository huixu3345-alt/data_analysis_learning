from pathlib import Path

import pandas as pd


# 1. 确定项目路径
BASE_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = BASE_DIR / "outputs"

INPUT_FILE = OUTPUT_DIR / "students_clean_day3.csv"


# 2. 读取 Day3 清洗后的数据
df = pd.read_csv(INPUT_FILE)

df["enroll_date"] = pd.to_datetime(
    df["enroll_date"],
    errors="coerce"
)


# 3. 查看读取结果
print("Day4 数据读取完成：")
print("数据行数：", len(df))
print("数据列数：", len(df.columns))
print(df.head())

# 4. 恢复适合分析的字段类型
df["name"] = df["name"].astype("string")

df[["class_name", "gender"]] = (
    df[["class_name", "gender"]]
    .astype("category")
)

date_number_cols = [
    "enroll_year",
    "enroll_month_num",
    "enroll_day"
]

df[date_number_cols] = (
    df[date_number_cols]
    .astype("Int64")
)


# 5. 生成成绩描述性统计
score_cols = [
    "math",
    "english",
    "python",
    "total_score",
    "avg_score"
]

score_summary = (
    df[score_cols]
    .describe()
    .round(2)
)

DESCRIBE_OUTPUT_FILE = (
    OUTPUT_DIR / "describe_summary_day4.csv"
)

score_summary.to_csv(
    DESCRIBE_OUTPUT_FILE,
    encoding="utf-8-sig"
)

print("\n成绩描述性统计：")
print(score_summary)

print("\n已生成：")
print(DESCRIBE_OUTPUT_FILE)

# 6. 生成类别字段分布
def create_distribution(data, column_name):
    count_result = (
        data[column_name]
        .value_counts(dropna=False)
    )

    rate_result = (
        data[column_name]
        .value_counts(
            normalize=True,
            dropna=False
        )
        .mul(100)
        .round(2)
    )

    result = pd.DataFrame({
        "field": column_name,
        "category": count_result.index.astype(str),
        "count": count_result.values,
        "percentage": rate_result.values
    })

    return result


distribution_fields = [
    "class_name",
    "gender",
    "is_pass",
    "enroll_month"
]

distribution_tables = []

for field in distribution_fields:
    field_distribution = create_distribution(
        df,
        field
    )
    distribution_tables.append(field_distribution)

category_distribution = pd.concat(
    distribution_tables,
    ignore_index=True
)

CATEGORY_OUTPUT_FILE = (
    OUTPUT_DIR / "category_distribution_day4.csv"
)

category_distribution.to_csv(
    CATEGORY_OUTPUT_FILE,
    index=False,
    encoding="utf-8-sig"
)

print("\n类别字段分布：")
print(category_distribution)

print("\n已生成：")
print(CATEGORY_OUTPUT_FILE)

# 7. 班级 + 性别组合分析
class_gender_summary = (
    df.groupby(
        ["class_name", "gender"],
        as_index=False,
        observed=True
    )
    .agg(
        student_count=("student_id", "count"),
        avg_score=("avg_score", "mean"),
        pass_rate=("is_pass", "mean")
    )
)

class_gender_summary["avg_score"] = (
    class_gender_summary["avg_score"].round(2)
)

class_gender_summary["pass_rate"] = (
    class_gender_summary["pass_rate"]
    .mul(100)
    .round(2)
)

class_gender_output = (
    class_gender_summary
    .rename(
        columns={
            "class_name": "dimension_1",
            "gender": "dimension_2"
        }
    )
)

class_gender_output.insert(
    0,
    "analysis_type",
    "class_and_gender"
)


# 8. 入学月份 + 班级组合分析
month_class_summary = (
    df.dropna(subset=["enroll_month"])
    .groupby(
        ["enroll_month", "class_name"],
        as_index=False,
        observed=True
    )
    .agg(
        student_count=("student_id", "count"),
        avg_score=("avg_score", "mean"),
        pass_rate=("is_pass", "mean")
    )
)

month_class_summary["avg_score"] = (
    month_class_summary["avg_score"].round(2)
)

month_class_summary["pass_rate"] = (
    month_class_summary["pass_rate"]
    .mul(100)
    .round(2)
)

month_class_output = (
    month_class_summary
    .rename(
        columns={
            "enroll_month": "dimension_1",
            "class_name": "dimension_2"
        }
    )
)

month_class_output.insert(
    0,
    "analysis_type",
    "month_and_class"
)


# 9. 合并并保存组合分析结果
groupby_summary = pd.concat(
    [
        class_gender_output,
        month_class_output
    ],
    ignore_index=True
)

GROUPBY_OUTPUT_FILE = (
    OUTPUT_DIR / "groupby_summary_day4.csv"
)

groupby_summary.to_csv(
    GROUPBY_OUTPUT_FILE,
    index=False,
    encoding="utf-8-sig"
)

print("\n班级与性别组合分析：")
print(class_gender_summary)

print("\n月份与班级组合分析：")
print(month_class_summary)

print("\n已生成：")
print(GROUPBY_OUTPUT_FILE)

# 10. 数据质量检查
row_count = len(df)
column_count = len(df.columns)

full_duplicate_count = int(
    df.duplicated().sum()
)

student_id_duplicate_count = int(
    df["student_id"].duplicated().sum()
)

valid_month_count = int(
    df["enroll_month"].notna().sum()
)

missing_month_count = int(
    df["enroll_month"].isna().sum()
)

month_coverage_rate = round(
    valid_month_count / row_count * 100,
    2
)

score_fields = [
    "math",
    "english",
    "python"
]

below_zero_count = int(
    (df[score_fields] < 0)
    .sum()
    .sum()
)

above_hundred_count = int(
    (df[score_fields] > 100)
    .sum()
    .sum()
)


# 11. 检查数学成绩的IQR潜在异常值
math_q1 = df["math"].quantile(0.25)
math_q3 = df["math"].quantile(0.75)
math_iqr = math_q3 - math_q1

math_lower = math_q1 - 1.5 * math_iqr
math_upper = math_q3 + 1.5 * math_iqr

math_outliers = df[
    (df["math"] < math_lower) |
    (df["math"] > math_upper)
]

math_outlier_names = "、".join(
    math_outliers["name"].astype(str).tolist()
)

if not math_outlier_names:
    math_outlier_names = "无"


# 12. 生成Markdown数据质量报告
report_text = f"""# 第2周 Day4 数据质量检查报告

## 1. 数据概况

- 数据行数：{row_count}
- 数据列数：{column_count}
- 有效入学月份记录：{valid_month_count}
- 缺失入学月份记录：{missing_month_count}
- 入学月份覆盖率：{month_coverage_rate}%

## 2. 重复值检查

- 整行重复数量：{full_duplicate_count}
- 学生ID重复数量：{student_id_duplicate_count}
- 结论：清洗后未发现整行重复，也未发现学生ID重复。

## 3. 成绩范围检查

- 小于0分的成绩数量：{below_zero_count}
- 大于100分的成绩数量：{above_hundred_count}
- 结论：三科成绩均处于0到100分的合法范围。

## 4. 潜在异常值检查

- 数学成绩Q1：{math_q1:.2f}
- 数学成绩Q3：{math_q3:.2f}
- 数学成绩IQR：{math_iqr:.2f}
- 数学异常值下界：{math_lower:.2f}
- 数学异常值上界：{math_upper:.2f}
- 被标记的学生：{math_outlier_names}
- 说明：统计异常不等于数据错误，需核对原始记录后再决定是否处理。

## 5. 分析结论

1. 16名学生中有15人通过，通过率为93.75%。
2. B班女生组平均分最高，为88.16分。
3. A班女生组平均分和通过率相对较低，主要受到一名低分学生影响。
4. 入学月份分析只覆盖12条记录，覆盖率为75%。
5. 各月份和班级组合只有1到2人，不能据此推断稳定的群体差异。

## 6. 数据质量建议

1. 回查4条无有效入学月份的原始记录。
2. 核对数学45分是否为真实成绩，不应仅因IQR标记就删除。
3. 保留数据清洗规则和问题记录，确保分析过程可以复现。
4. 扩大样本后，再判断班级、性别和月份之间是否存在稳定差异。
"""

REPORT_OUTPUT_FILE = (
    OUTPUT_DIR / "data_quality_report_day4.md"
)

REPORT_OUTPUT_FILE.write_text(
    report_text,
    encoding="utf-8"
)

print("\n已生成数据质量报告：")
print(REPORT_OUTPUT_FILE)