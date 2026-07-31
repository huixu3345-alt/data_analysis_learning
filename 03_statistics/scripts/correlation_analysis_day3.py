from pathlib import Path

import pandas as pd


marketing_data = pd.DataFrame(
    {
        "ad_spend": [10, 12, 15, 18, 20, 25, 28, 30],
        "sales": [100, 115, 140, 170, 180, 230, 250, 280],
    }
)

covariance = marketing_data["ad_spend"].cov(
    marketing_data["sales"]
)

correlation = marketing_data["ad_spend"].corr(
    marketing_data["sales"]
)

print("===== 广告投入与销售额数据 =====")
print(marketing_data)

print("\n===== 协方差与相关系数 =====")
print("协方差：", round(covariance, 2))
print("相关系数：", round(correlation, 4))

# =========================
# 单位变化对结果的影响
# =========================

marketing_data["ad_spend_yuan"] = (
    marketing_data["ad_spend"] * 1000
)

scaled_covariance = marketing_data[
    "ad_spend_yuan"
].cov(marketing_data["sales"])

scaled_correlation = marketing_data[
    "ad_spend_yuan"
].corr(marketing_data["sales"])

print("\n===== 广告投入单位变化后 =====")
print("原协方差：", round(covariance, 2))
print("单位变化后的协方差：", round(scaled_covariance, 2))
print("原相关系数：", round(correlation, 4))
print("单位变化后的相关系数：", round(scaled_correlation, 4))

# =========================
# 多变量相关矩阵
# =========================

business_data = pd.DataFrame(
    {
        "ad_spend": [10, 12, 15, 18, 20, 25, 28, 30],
        "sales": [100, 115, 140, 170, 180, 230, 250, 280],
        "price": [90, 110, 85, 120, 80, 100, 95, 105],
        "quantity": [30, 22, 35, 18, 38, 25, 28, 24],
        "satisfaction": [4.2, 3.8, 4.5, 3.5, 4.7, 4.0, 4.1, 3.9],
    }
)

correlation_matrix = business_data.corr()

print("\n===== 多变量相关矩阵 =====")
print(correlation_matrix.round(2))

# =========================
# 异常点对相关性的影响
# =========================

marketing_with_outlier = pd.concat(
    [
        marketing_data[["ad_spend", "sales"]],
        pd.DataFrame(
            {
                "ad_spend": [100],
                "sales": [50],
            }
        ),
    ],
    ignore_index=True,
)

correlation_with_outlier = marketing_with_outlier[
    "ad_spend"
].corr(marketing_with_outlier["sales"])

print("\n===== 异常点影响分析 =====")
print("原相关系数：", round(correlation, 4))
print(
    "加入异常点后的相关系数：",
    round(correlation_with_outlier, 4),
)
print("\n加入异常点后的数据：")
print(marketing_with_outlier)

# =========================
# 保存Day3分析结果
# =========================

PROJECT_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_DIR / "outputs"

OUTPUT_DIR.mkdir(exist_ok=True)

correlation_matrix_path = (
    OUTPUT_DIR / "correlation_matrix_day3.csv"
)

outlier_comparison_path = (
    OUTPUT_DIR / "correlation_outlier_comparison_day3.csv"
)

correlation_matrix.round(4).to_csv(
    correlation_matrix_path,
    encoding="utf-8-sig",
)

outlier_comparison = pd.DataFrame(
    {
        "scenario": [
            "原始数据",
            "加入异常点",
        ],
        "sample_count": [
            len(marketing_data),
            len(marketing_with_outlier),
        ],
        "correlation": [
            correlation,
            correlation_with_outlier,
        ],
    }
)

outlier_comparison.round(4).to_csv(
    outlier_comparison_path,
    index=False,
    encoding="utf-8-sig",
)

print("\n===== 输出文件 =====")
print(correlation_matrix_path)
print(outlier_comparison_path)
