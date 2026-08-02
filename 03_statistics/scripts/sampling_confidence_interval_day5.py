from math import sqrt
from pathlib import Path

import numpy as np
import pandas as pd


z_value = 1.96

# =========================
# 均值的95%置信区间
# =========================

sample_mean = 200
sample_std = 50
sample_size = 100

mean_standard_error = (
    sample_std / sqrt(sample_size)
)

mean_margin_of_error = (
    z_value * mean_standard_error
)

mean_ci_lower = (
    sample_mean - mean_margin_of_error
)

mean_ci_upper = (
    sample_mean + mean_margin_of_error
)

print("===== 均值的95%置信区间 =====")
print("样本均值：", sample_mean)
print("样本标准差：", sample_std)
print("样本量：", sample_size)
print(
    "标准误：",
    round(mean_standard_error, 2),
)
print(
    "误差范围：",
    round(mean_margin_of_error, 2),
)
print(
    "95%置信区间：",
    (
        round(mean_ci_lower, 2),
        round(mean_ci_upper, 2),
    ),
)

# =========================
# 转化率的95%置信区间
# =========================

visitor_count = 1000
conversion_count = 80

conversion_rate = (
    conversion_count / visitor_count
)

conversion_standard_error = sqrt(
    conversion_rate
    * (1 - conversion_rate)
    / visitor_count
)

conversion_margin_of_error = (
    z_value * conversion_standard_error
)

conversion_ci_lower = (
    conversion_rate - conversion_margin_of_error
)

conversion_ci_upper = (
    conversion_rate + conversion_margin_of_error
)

print("\n===== 转化率的95%置信区间 =====")
print(
    "样本转化率：",
    round(conversion_rate * 100, 2),
    "%",
)
print(
    "标准误：",
    round(conversion_standard_error, 4),
)
print(
    "误差范围：",
    round(conversion_margin_of_error * 100, 2),
    "个百分点",
)
print(
    "95%置信区间：",
    (
        round(conversion_ci_lower * 100, 2),
        round(conversion_ci_upper * 100, 2),
    ),
    "%",
)

# =========================
# 重复抽样模拟
# =========================

rng = np.random.default_rng(42)

true_mean = 200
true_std = 50
repeat_count = 10000

sample_means_n100 = rng.normal(
    loc=true_mean,
    scale=true_std,
    size=(repeat_count, 100),
).mean(axis=1)

sample_means_n400 = rng.normal(
    loc=true_mean,
    scale=true_std,
    size=(repeat_count, 400),
).mean(axis=1)

simulated_se_n100 = sample_means_n100.std(
    ddof=1
)

simulated_se_n400 = sample_means_n400.std(
    ddof=1
)

theoretical_se_n100 = (
    true_std / sqrt(100)
)

theoretical_se_n400 = (
    true_std / sqrt(400)
)

ci_lower_n100 = (
    sample_means_n100
    - z_value * theoretical_se_n100
)

ci_upper_n100 = (
    sample_means_n100
    + z_value * theoretical_se_n100
)

coverage_rate_n100 = (
    (ci_lower_n100 <= true_mean)
    & (ci_upper_n100 >= true_mean)
).mean()

print("\n===== 重复抽样模拟 =====")
print(
    "样本量100的理论标准误：",
    round(theoretical_se_n100, 2),
)
print(
    "样本量100的模拟标准误：",
    round(simulated_se_n100, 2),
)
print(
    "样本量400的理论标准误：",
    round(theoretical_se_n400, 2),
)
print(
    "样本量400的模拟标准误：",
    round(simulated_se_n400, 2),
)
print(
    "样本量100的95%区间覆盖率：",
    round(coverage_rate_n100 * 100, 2),
    "%",
)

# =========================
# 随机样本与偏差样本
# =========================

regular_user_spending = rng.normal(
    loc=100,
    scale=20,
    size=80000,
)

vip_user_spending = rng.normal(
    loc=500,
    scale=50,
    size=20000,
)

population_spending = np.concatenate(
    [
        regular_user_spending,
        vip_user_spending,
    ]
)

random_sample = rng.choice(
    population_spending,
    size=10000,
    replace=False,
)

biased_vip_sample = rng.choice(
    vip_user_spending,
    size=10000,
    replace=False,
)

population_mean = population_spending.mean()
random_sample_mean = random_sample.mean()
biased_sample_mean = biased_vip_sample.mean()

random_sample_se = (
    random_sample.std(ddof=1)
    / sqrt(len(random_sample))
)

biased_sample_se = (
    biased_vip_sample.std(ddof=1)
    / sqrt(len(biased_vip_sample))
)

print("\n===== 随机样本与偏差样本 =====")
print(
    "总体平均消费：",
    round(population_mean, 2),
)
print(
    "随机样本平均消费：",
    round(random_sample_mean, 2),
)
print(
    "VIP偏差样本平均消费：",
    round(biased_sample_mean, 2),
)
print(
    "随机样本标准误：",
    round(random_sample_se, 2),
)
print(
    "VIP偏差样本标准误：",
    round(biased_sample_se, 2),
)

# =========================
# 保存Day5分析结果
# =========================

PROJECT_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_DIR / "outputs"

OUTPUT_DIR.mkdir(exist_ok=True)

confidence_interval_summary = pd.DataFrame(
    {
        "metric": [
            "mean",
            "conversion_rate",
        ],
        "sample_size": [
            sample_size,
            visitor_count,
        ],
        "estimate": [
            sample_mean,
            conversion_rate,
        ],
        "standard_error": [
            mean_standard_error,
            conversion_standard_error,
        ],
        "ci_lower": [
            mean_ci_lower,
            conversion_ci_lower,
        ],
        "ci_upper": [
            mean_ci_upper,
            conversion_ci_upper,
        ],
    }
)

sampling_simulation_summary = pd.DataFrame(
    {
        "sample_size": [100, 400],
        "theoretical_standard_error": [
            theoretical_se_n100,
            theoretical_se_n400,
        ],
        "simulated_standard_error": [
            simulated_se_n100,
            simulated_se_n400,
        ],
        "coverage_rate": [
            coverage_rate_n100,
            np.nan,
        ],
    }
)

sample_bias_comparison = pd.DataFrame(
    {
        "sample_type": [
            "population",
            "random_sample",
            "vip_biased_sample",
        ],
        "sample_size": [
            len(population_spending),
            len(random_sample),
            len(biased_vip_sample),
        ],
        "mean_spending": [
            population_mean,
            random_sample_mean,
            biased_sample_mean,
        ],
        "standard_error": [
            np.nan,
            random_sample_se,
            biased_sample_se,
        ],
    }
)

confidence_output_path = (
    OUTPUT_DIR / "confidence_interval_day5.csv"
)

simulation_output_path = (
    OUTPUT_DIR / "sampling_simulation_day5.csv"
)

bias_output_path = (
    OUTPUT_DIR / "sample_bias_comparison_day5.csv"
)

confidence_interval_summary.round(4).to_csv(
    confidence_output_path,
    index=False,
    encoding="utf-8-sig",
)

sampling_simulation_summary.round(4).to_csv(
    simulation_output_path,
    index=False,
    encoding="utf-8-sig",
)

sample_bias_comparison.round(4).to_csv(
    bias_output_path,
    index=False,
    encoding="utf-8-sig",
)

print("\n===== 输出文件 =====")
print(confidence_output_path)
print(simulation_output_path)
print(bias_output_path)