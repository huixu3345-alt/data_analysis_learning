from pathlib import Path
from math import sqrt
import pandas as pd
from scipy.stats import chisquare, norm


observed_users = [5000, 5100]
expected_users = [5050, 5050]

chi_square_stat, srm_p_value = chisquare(
    f_obs=observed_users,
    f_exp=expected_users,
)

alpha = 0.05
srm_detected = srm_p_value < alpha

print("===== A/B分流比例检查 =====")
print("实际人数：", observed_users)
print("期望人数：", expected_users)
print(
    "卡方统计量：",
    round(chi_square_stat, 4),
)
print(
    "SRM p-value：",
    round(srm_p_value, 4),
)
print("是否发现SRM异常：", srm_detected)

# =========================
# 两组转化率置信区间
# =========================

group_a_users = 5000
group_a_conversions = 400

group_b_users = 5100
group_b_conversions = 459

group_a_rate = (
    group_a_conversions / group_a_users
)

group_b_rate = (
    group_b_conversions / group_b_users
)

z_value = 1.96

group_a_se = sqrt(
    group_a_rate
    * (1 - group_a_rate)
    / group_a_users
)

group_b_se = sqrt(
    group_b_rate
    * (1 - group_b_rate)
    / group_b_users
)

group_a_ci = (
    group_a_rate - z_value * group_a_se,
    group_a_rate + z_value * group_a_se,
)

group_b_ci = (
    group_b_rate - z_value * group_b_se,
    group_b_rate + z_value * group_b_se,
)

print("\n===== 两组转化率置信区间 =====")
print(
    "A组转化率：",
    round(group_a_rate * 100, 2),
    "%",
)
print(
    "A组95%置信区间：",
    (
        round(group_a_ci[0] * 100, 2),
        round(group_a_ci[1] * 100, 2),
    ),
    "%",
)
print(
    "B组转化率：",
    round(group_b_rate * 100, 2),
    "%",
)
print(
    "B组95%置信区间：",
    (
        round(group_b_ci[0] * 100, 2),
        round(group_b_ci[1] * 100, 2),
    ),
    "%",
)

# =========================
# 转化率差异的置信区间
# =========================

rate_difference = (
    group_b_rate - group_a_rate
)

difference_standard_error = sqrt(
    (
        group_a_rate
        * (1 - group_a_rate)
        / group_a_users
    )
    +
    (
        group_b_rate
        * (1 - group_b_rate)
        / group_b_users
    )
)

difference_margin_of_error = (
    z_value * difference_standard_error
)

difference_ci_lower = (
    rate_difference
    - difference_margin_of_error
)

difference_ci_upper = (
    rate_difference
    + difference_margin_of_error
)

difference_ci_includes_zero = (
    difference_ci_lower <= 0
    <= difference_ci_upper
)

print("\n===== B组减A组的转化率差异 =====")
print(
    "转化率差异：",
    round(rate_difference * 100, 2),
    "个百分点",
)
print(
    "差异标准误：",
    round(difference_standard_error * 100, 2),
    "个百分点",
)
print(
    "差异95%置信区间：",
    (
        round(difference_ci_lower * 100, 2),
        round(difference_ci_upper * 100, 2),
    ),
    "个百分点",
)
print(
    "差异区间是否包含0：",
    difference_ci_includes_zero,
)


# =========================
# 两比例Z检验
# =========================

pooled_conversion_rate = (
    group_a_conversions
    + group_b_conversions
) / (
    group_a_users
    + group_b_users
)

pooled_standard_error = sqrt(
    pooled_conversion_rate
    * (1 - pooled_conversion_rate)
    * (
        1 / group_a_users
        + 1 / group_b_users
    )
)

z_statistic = (
    rate_difference
    / pooled_standard_error
)

two_sided_p_value = (
    2
    * (
        1
        - norm.cdf(abs(z_statistic))
    )
)

statistically_significant = (
    two_sided_p_value < alpha
)

print("\n===== 两比例Z检验 =====")
print(
    "合并转化率：",
    round(pooled_conversion_rate * 100, 2),
    "%",
)
print(
    "Z统计量：",
    round(z_statistic, 4),
)
print(
    "双侧p-value：",
    round(two_sided_p_value, 4),
)
print(
    "是否达到0.05显著性水平：",
    statistically_significant,
)

# =========================
# 保存Week7 Day2结果
# =========================

PROJECT_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_DIR / "outputs"

OUTPUT_DIR.mkdir(exist_ok=True)

srm_summary = pd.DataFrame(
    {
        "chi_square_stat": [
            chi_square_stat
        ],
        "srm_p_value": [
            srm_p_value
        ],
        "alpha": [
            alpha
        ],
        "srm_detected": [
            srm_detected
        ],
    }
)

group_interval_summary = pd.DataFrame(
    {
        "group": ["A", "B"],
        "users": [
            group_a_users,
            group_b_users,
        ],
        "conversions": [
            group_a_conversions,
            group_b_conversions,
        ],
        "conversion_rate": [
            group_a_rate,
            group_b_rate,
        ],
        "ci_lower": [
            group_a_ci[0],
            group_b_ci[0],
        ],
        "ci_upper": [
            group_a_ci[1],
            group_b_ci[1],
        ],
    }
)

difference_test_summary = pd.DataFrame(
    {
        "rate_difference": [
            rate_difference
        ],
        "difference_standard_error": [
            difference_standard_error
        ],
        "difference_ci_lower": [
            difference_ci_lower
        ],
        "difference_ci_upper": [
            difference_ci_upper
        ],
        "ci_includes_zero": [
            difference_ci_includes_zero
        ],
        "z_statistic": [
            z_statistic
        ],
        "two_sided_p_value": [
            two_sided_p_value
        ],
        "statistically_significant": [
            statistically_significant
        ],
    }
)

srm_output_path = (
    OUTPUT_DIR / "ab_test_srm_week7_day2.csv"
)

interval_output_path = (
    OUTPUT_DIR
    / "ab_test_group_intervals_week7_day2.csv"
)

test_output_path = (
    OUTPUT_DIR
    / "ab_test_difference_test_week7_day2.csv"
)

srm_summary.round(4).to_csv(
    srm_output_path,
    index=False,
    encoding="utf-8-sig",
)

group_interval_summary.round(4).to_csv(
    interval_output_path,
    index=False,
    encoding="utf-8-sig",
)

difference_test_summary.round(4).to_csv(
    test_output_path,
    index=False,
    encoding="utf-8-sig",
)

print("\n===== 输出文件 =====")
print(srm_output_path)
print(interval_output_path)
print(test_output_path)