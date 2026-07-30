from pathlib import Path

import pandas as pd


spending = pd.Series(
    [80, 90, 100, 110, 120, 130, 150, 180, 250, 500],
    name="spending",
)

percentiles = spending.quantile(
    [0.25, 0.50, 0.75, 0.90, 0.95]
)

print("===== 原始消费数据 =====")
print(spending.tolist())

print("\n===== 中心位置与偏态 =====")
print("均值：", round(spending.mean(), 2))
print("中位数：", round(spending.median(), 2))
print("偏度：", round(spending.skew(), 2))

print("\n===== 百分位数 =====")
print(percentiles.round(2))

# =========================
# 多指标Z-score标准化
# =========================

users = pd.DataFrame(
    {
        "user_id": ["U001", "U002", "U003", "U004", "U005"],
        "monthly_spending": [100, 150, 200, 250, 500],
        "order_count": [2, 10, 4, 6, 8],
    }
)

users["spending_zscore"] = (
    users["monthly_spending"]
    - users["monthly_spending"].mean()
) / users["monthly_spending"].std()

users["order_count_zscore"] = (
    users["order_count"]
    - users["order_count"].mean()
) / users["order_count"].std()

users["composite_score"] = users[
    ["spending_zscore", "order_count_zscore"]
].mean(axis=1)

users = users.sort_values(
    "composite_score",
    ascending=False,
)

print("\n===== 用户标准化结果 =====")
print(users.round(2))

# =========================
# Z-score结果验证
# =========================

zscore_validation = users[
    ["spending_zscore", "order_count_zscore"]
].agg(["mean", "std"])

print("\n===== Z-score验证 =====")
print(zscore_validation.round(6))

# =========================
# 保存Day2分析结果
# =========================

PROJECT_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_DIR / "outputs"

OUTPUT_DIR.mkdir(exist_ok=True)

percentiles_output = (
    percentiles
    .rename_axis("quantile")
    .reset_index(name="spending")
)

percentiles_output_path = (
    OUTPUT_DIR / "spending_percentiles_day2.csv"
)

user_scores_output_path = (
    OUTPUT_DIR / "user_zscore_day2.csv"
)

percentiles_output.to_csv(
    percentiles_output_path,
    index=False,
    encoding="utf-8-sig",
)

users.to_csv(
    user_scores_output_path,
    index=False,
    encoding="utf-8-sig",
)

print("\n===== 输出文件 =====")
print(percentiles_output_path)
print(user_scores_output_path)