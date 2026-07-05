from pathlib import Path
import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "students_dirty_day3.csv"
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

score_cols = ["math", "english", "python"]


def markdown_table(df: pd.DataFrame) -> str:
    """Return a markdown table. Fall back to plain text if tabulate is not installed."""
    try:
        return df.to_markdown(index=False)
    except Exception:
        return "```text\n" + df.to_string(index=False) + "\n```"


def normalize_blank_values(df: pd.DataFrame) -> pd.DataFrame:
    """Strip spaces and convert common blank-like tokens to missing values."""
    result = df.copy()
    for col in result.columns:
        result[col] = result[col].astype("string").str.strip()
    result = result.replace({"": pd.NA, "NA": pd.NA, "N/A": pd.NA, "not_available": pd.NA})
    return result


# 1. 读取数据：先统一按字符串读取，方便暴露字段类型问题
raw_df = pd.read_csv(DATA_PATH, dtype="string", keep_default_na=False)
print("===== 原始数据预览 head() =====")
print(raw_df.head())
print("\n===== 原始字段类型 info() =====")
raw_df.info()

# 2. 基础数据质量处理：空值标记、去除首尾空格
df = normalize_blank_values(raw_df)
missing_before_conversion = df.isna().sum().reset_index()
missing_before_conversion.columns = ["field", "missing_count_before_conversion"]

# 3. 字段类型转换：ID、文本字段、类别字段
# 说明：astype() 适合在字段内容已经比较干净时进行类型转换。
df["student_id"] = df["student_id"].astype("string").str.strip().astype("Int64")
df["name"] = df["name"].astype("string")
df["class_name"] = df["class_name"].astype("category")
df["gender"] = df["gender"].astype("category")

# 4. 数值字段转换：先清理“分”等单位，再转成数字
# 说明：脏数据里可能出现“缺考”“优秀”等文本，直接 astype(float) 会报错。
# 因此这里使用 pd.to_numeric(errors="coerce")，把无法转换的内容变成 NaN。
score_issue_frames = []
for col in score_cols:
    raw_score = df[col].astype("string").str.strip().str.replace("分", "", regex=False)
    converted_score = pd.to_numeric(raw_score, errors="coerce")
    issue_mask = converted_score.isna() & raw_score.notna()
    if issue_mask.any():
        tmp = df.loc[issue_mask, ["student_id", "name", "class_name", col]].copy()
        tmp = tmp.rename(columns={col: "raw_value"})
        tmp.insert(0, "field", col)
        score_issue_frames.append(tmp)
    df[col] = converted_score

score_issues = (
    pd.concat(score_issue_frames, ignore_index=True)
    if score_issue_frames
    else pd.DataFrame(columns=["field", "student_id", "name", "class_name", "raw_value"])
)

# 5. 日期字段转换：统一日期格式后使用 pd.to_datetime()
date_raw = df["enroll_date"].astype("string").str.strip()
date_normalized = (
    date_raw
    .str.replace("年", "-", regex=False)
    .str.replace("月", "-", regex=False)
    .str.replace("日", "", regex=False)
    .str.replace("/", "-", regex=False)
    .str.replace(".", "-", regex=False)
)
df["enroll_date_raw"] = date_raw
df["enroll_date"] = pd.to_datetime(date_normalized, errors="coerce")
invalid_date_rows = df.loc[df["enroll_date"].isna(), ["student_id", "name", "class_name", "enroll_date_raw"]].copy()

# 6. 处理数值字段转换后产生的缺失值：用每科中位数填充
score_fill_values = df[score_cols].median(numeric_only=True)
for col in score_cols:
    df[col] = df[col].fillna(score_fill_values[col])

# 7. 日期信息提取：year / month / day / enroll_month
# 说明：NaT 是日期类型里的缺失值。无法确认的日期不要乱填，本次保留为 NaT。
df["enroll_year"] = df["enroll_date"].dt.year.astype("Int64")
df["enroll_month_num"] = df["enroll_date"].dt.month.astype("Int64")
df["enroll_day"] = df["enroll_date"].dt.day.astype("Int64")
df["enroll_month"] = df["enroll_date"].dt.strftime("%Y-%m")

# 8. 指标计算：总分、平均分、是否通过
df["total_score"] = df[score_cols].sum(axis=1).round(2)
df["avg_score"] = df[score_cols].mean(axis=1).round(2)
df["is_pass"] = df["avg_score"] >= 60

# 9. 分组分析：按月份统计、按班级统计
monthly_summary = (
    df.dropna(subset=["enroll_month"])
    .groupby("enroll_month", as_index=False)
    .agg(
        student_count=("student_id", "count"),
        avg_math=("math", "mean"),
        avg_english=("english", "mean"),
        avg_python=("python", "mean"),
        avg_score=("avg_score", "mean"),
        pass_rate=("is_pass", "mean"),
    )
)
monthly_summary[["avg_math", "avg_english", "avg_python", "avg_score"]] = monthly_summary[["avg_math", "avg_english", "avg_python", "avg_score"]].round(2)
monthly_summary["pass_rate"] = (monthly_summary["pass_rate"] * 100).round(2)
monthly_summary = monthly_summary.sort_values("enroll_month")

class_summary = (
    df.groupby("class_name", observed=False)
    .agg(
        student_count=("student_id", "count"),
        avg_score=("avg_score", "mean"),
        pass_rate=("is_pass", "mean"),
    )
    .round({"avg_score": 2, "pass_rate": 4})
    .reset_index()
)
class_summary["pass_rate"] = (class_summary["pass_rate"] * 100).round(2)

# 10. 字段类型变化表
field_type_before = raw_df.dtypes.astype(str).reset_index()
field_type_before.columns = ["field", "type_before"]
field_type_after = df[raw_df.columns].dtypes.astype(str).reset_index()
field_type_after.columns = ["field", "type_after"]
field_type_summary = field_type_before.merge(field_type_after, on="field", how="left")

# 11. 输出 CSV 文件
df.to_csv(OUTPUT_DIR / "students_clean_day3.csv", index=False, encoding="utf-8-sig")
monthly_summary.to_csv(OUTPUT_DIR / "monthly_summary_day3.csv", index=False, encoding="utf-8-sig")
class_summary.to_csv(OUTPUT_DIR / "class_summary_day3.csv", index=False, encoding="utf-8-sig")

# 12. 自动生成 Markdown 总结报告
valid_date_count = int(df["enroll_date"].notna().sum())
invalid_date_count = int(df["enroll_date"].isna().sum())
score_issue_count = int(len(score_issues))

if not monthly_summary.empty:
    best_month_row = monthly_summary.loc[monthly_summary["avg_score"].idxmax()]
    weakest_month_row = monthly_summary.loc[monthly_summary["avg_score"].idxmin()]
    best_month_sentence = f"平均成绩最高的入学月份是 {best_month_row['enroll_month']}，平均分为 {best_month_row['avg_score']}。"
    weakest_month_sentence = f"平均成绩最低的入学月份是 {weakest_month_row['enroll_month']}，平均分为 {weakest_month_row['avg_score']}。"
else:
    best_month_sentence = "暂无有效月份数据，无法比较月份表现。"
    weakest_month_sentence = "暂无有效月份数据，无法比较月份表现。"

report = f"""# 第2周 Day3：字段类型转换与日期字段处理总结

## 1. 今日主线

数据质量 → 字段类型 → 日期处理 → 指标计算 → 分组分析 → 业务结论 → GitHub 项目资产

## 2. 原始数据质量发现

- 原始数据行数：{len(raw_df)} 行。
- 原始数据统一按字符串读取，目的是先暴露字段类型问题，而不是一开始就假设字段可信。
- 字段转换前缺失值数量如下：

{markdown_table(missing_before_conversion)}

## 3. 字段类型转换结果

{markdown_table(field_type_summary)}

关键理解：字段类型不正确，后面的排序、求和、平均值、月份分析都可能失真。比如成绩字段如果还是字符串，`"100"` 和 `"59"` 的排序可能不是业务想要的数值排序。

## 4. 数值字段转换问题

本次发现无法直接转换为数字的成绩记录数量：{score_issue_count}。

{markdown_table(score_issues) if not score_issues.empty else "没有发现无法转换的成绩字段。"}

处理策略：

1. 先把成绩里的“分”等单位去掉。
2. 使用 `pd.to_numeric(errors="coerce")` 把无法转换的内容变成 NaN。
3. 用每科中位数填充转换失败后的缺失值。
4. 再重新计算 `total_score` 和 `avg_score`。

## 5. 日期字段处理结果

- 可成功转换的日期数量：{valid_date_count}。
- 无法成功转换或为空的日期数量：{invalid_date_count}。

{markdown_table(invalid_date_rows) if not invalid_date_rows.empty else "没有发现无法转换的日期。"}

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

{markdown_table(monthly_summary)}

## 8. 按班级分组统计

{markdown_table(class_summary)}

## 9. 初步业务结论

1. {best_month_sentence}
2. {weakest_month_sentence}
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
"""

(OUTPUT_DIR / "cleaning_summary_day3.md").write_text(report, encoding="utf-8")

print("\n===== 清洗后数据类型 info() =====")
df.info()
print("\n===== 按月份统计结果 =====")
print(monthly_summary)
print("\n输出完成：")
print(OUTPUT_DIR / "students_clean_day3.csv")
print(OUTPUT_DIR / "monthly_summary_day3.csv")
print(OUTPUT_DIR / "class_summary_day3.csv")
print(OUTPUT_DIR / "cleaning_summary_day3.md")
