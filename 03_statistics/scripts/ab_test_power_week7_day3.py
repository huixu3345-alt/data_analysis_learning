from math import ceil, sqrt
from pathlib import Path

import pandas as pd
from scipy.stats import norm


baseline_rate = 0.08
mde = 0.01

group_a_target_rate = baseline_rate
group_b_target_rate = (
    baseline_rate + mde
)

alpha = 0.05
target_power = 0.80

z_alpha = norm.ppf(
    1 - alpha / 2
)

z_power = norm.ppf(
    target_power
)

average_rate = (
    group_a_target_rate
    + group_b_target_rate
) / 2

sample_size_per_group = (
    (
        z_alpha
        * sqrt(
            2
            * average_rate
            * (1 - average_rate)
        )
        +
        z_power
        * sqrt(
            group_a_target_rate
            * (1 - group_a_target_rate)
            +
            group_b_target_rate
            * (1 - group_b_target_rate)
        )
    )
    ** 2
    / (mde ** 2)
)

required_sample_size = ceil(
    sample_size_per_group
)

required_total_sample_size = (
    required_sample_size * 2
)

print("===== A/B测试样本量设计 =====")
print(
    "基准转化率：",
    baseline_rate * 100,
    "%",
)
print(
    "MDE：",
    mde * 100,
    "个百分点",
)
print(
    "目标B组转化率：",
    group_b_target_rate * 100,
    "%",
)
print("显著性水平：", alpha)
print("目标统计功效：", target_power)
print(
    "每组所需样本量：",
    required_sample_size,
)
print(
    "两组总样本量：",
    required_total_sample_size,
)

# =========================
# 样本量场景对比
# =========================

scenario_comparison = pd.DataFrame(
    {
        "scenario": [
            "基准方案",
            "更小MDE",
            "更高统计功效",
        ],
        "baseline_rate": [
            0.08,
            0.08,
            0.08,
        ],
        "mde": [
            0.01,
            0.005,
            0.01,
        ],
        "target_power": [
            0.80,
            0.80,
            0.90,
        ],
        "required_sample_per_group": [
            12208,
            47528,
            16343,
        ],
    }
)

actual_group_a = 5000
actual_group_b = 5100

scenario_comparison["group_a_sufficient"] = (
    actual_group_a
    >= scenario_comparison["required_sample_per_group"]
)

scenario_comparison["group_b_sufficient"] = (
    actual_group_b
    >= scenario_comparison["required_sample_per_group"]
)

print("\n===== 样本量场景对比 =====")
print(scenario_comparison)

# =========================
# 输出结果
# =========================
PROJECT_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_DIR / "outputs"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

output_file = (
    OUTPUT_DIR
    / "ab_test_sample_size_scenarios_week7_day3.csv"
)

scenario_comparison.to_csv(
    output_file,
    index=False,
    encoding="utf-8-sig",
)

print("\n===== 输出文件 =====")
print(output_file)