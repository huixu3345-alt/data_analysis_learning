"""第6周 Day1：描述性统计基础。"""
import pandas as pd
from pathlib import Path

group_a = pd.Series([80, 90, 100, 110, 120])
group_b = pd.Series([98, 99, 100, 101, 102])

summary = pd.DataFrame(
    {
        "A组": [
            group_a.mean(),
            group_a.median(),
            group_a.max() - group_a.min(),
            group_a.var(),
            group_a.std(),
        ],
        "B组": [
            group_b.mean(),
            group_b.median(),
            group_b.max() - group_b.min(),
            group_b.var(),
            group_b.std(),
        ],
    },
    index=["均值", "中位数", "极差", "样本方差", "样本标准差"],
)

print("===== 两组数据 =====")
print("A组：", group_a.tolist())
print("B组：", group_b.tolist())

print("\n===== 描述性统计对比 =====")
print(summary.round(2))

# =========================
# 极端值影响分析
# =========================

spending = pd.Series([100, 120, 120, 150, 1010])

# 这里只做对比分析，不代表应该删除1010
spending_without_high_value = spending[spending != 1010]

outlier_comparison = pd.DataFrame(
    {
        "包含高消费值": [
            spending.mean(),
            spending.median(),
            spending.std(),
        ],
        "暂不包含高消费值": [
            spending_without_high_value.mean(),
            spending_without_high_value.median(),
            spending_without_high_value.std(),
        ],
    },
    index=["均值", "中位数", "样本标准差"],
)

print("\n===== 极端值影响分析 =====")
print("原始消费金额：", spending.tolist())
print(outlier_comparison.round(2))

# =========================
# describe 描述性统计汇总
# =========================

describe_summary = spending.describe().round(2)

print("\n===== 消费金额 describe 汇总 =====")
print(describe_summary)

# =========================
# IQR异常值候选检查
# =========================

q1 = spending.quantile(0.25)
q3 = spending.quantile(0.75)
iqr = q3 - q1

lower_bound = q1 - 1.5 * iqr
upper_bound = q3 + 1.5 * iqr

outlier_candidates = spending[
    (spending < lower_bound)
    | (spending > upper_bound)
]

print("\n===== IQR异常值候选检查 =====")
print("Q1：", q1)
print("Q3：", q3)
print("IQR：", iqr)
print("下界：", lower_bound)
print("上界：", upper_bound)
print("异常值候选：", outlier_candidates.tolist())

# =========================
# 保存统计分析结果
# =========================

PROJECT_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_DIR / "outputs"

OUTPUT_DIR.mkdir(exist_ok=True)

describe_output = (
    describe_summary
    .rename_axis("statistic")
    .reset_index(name="value")
)

iqr_output = pd.DataFrame(
    {
        "q1": [q1],
        "q3": [q3],
        "iqr": [iqr],
        "lower_bound": [lower_bound],
        "upper_bound": [upper_bound],
        "outlier_candidates": [
            ", ".join(map(str, outlier_candidates.tolist()))
        ],
    }
)

describe_output_path = OUTPUT_DIR / "describe_summary_day1.csv"
iqr_output_path = OUTPUT_DIR / "iqr_outlier_check_day1.csv"

describe_output.to_csv(
    describe_output_path,
    index=False,
    encoding="utf-8-sig",
)

iqr_output.to_csv(
    iqr_output_path,
    index=False,
    encoding="utf-8-sig",
)

print("\n===== 输出文件 =====")
print(describe_output_path)
print(iqr_output_path)