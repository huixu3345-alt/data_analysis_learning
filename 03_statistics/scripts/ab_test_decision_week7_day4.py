from pathlib import Path

import pandas as pd


# =========================
# 1. 路径设置
# =========================

PROJECT_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_DIR / "outputs"


# =========================
# 2. 实验结果
# =========================

experiment = {
    "experiment_name": "新版结算页A/B测试",
    "group_a_users": 5000,
    "group_b_users": 5100,
    "group_a_conversion_rate": 0.08,
    "group_b_conversion_rate": 0.09,
    "absolute_lift": 0.01,
    "statistical_mde": 0.01,
    "business_minimum_lift": 0.005,
    "p_value": 0.0717,
    "alpha": 0.05,
    "required_sample_per_group": 12208,
    "refund_rate_increase": 0.0263,
    "refund_guardrail_limit": 0.01,
    "error_rate_increase": 0.0057,
    "error_guardrail_limit": 0.002,
    "srm_detected": False,
}

result = pd.DataFrame([experiment])

print("===== 实验原始结果 =====")
print(result.T)

# =========================
# 3. 自动检查各项条件
# =========================

result["data_quality_pass"] = (
    result["srm_detected"] == False
)

result["sample_size_pass"] = (
    (result["group_a_users"]
     >= result["required_sample_per_group"])
    &
    (result["group_b_users"]
     >= result["required_sample_per_group"])
)

result["statistical_significance_pass"] = (
    result["p_value"] <= result["alpha"]
)

result["business_significance_pass"] = (
    result["absolute_lift"]
    >= result["business_minimum_lift"]
)

result["refund_guardrail_pass"] = (
    result["refund_rate_increase"]
    <= result["refund_guardrail_limit"]
)

result["error_guardrail_pass"] = (
    result["error_rate_increase"]
    <= result["error_guardrail_limit"]
)

check_columns = [
    "data_quality_pass",
    "sample_size_pass",
    "statistical_significance_pass",
    "business_significance_pass",
    "refund_guardrail_pass",
    "error_guardrail_pass",
]

print("\n===== 各项决策检查 =====")
print(result[check_columns].T)

# =========================
# 4. 生成失败原因
# =========================

def get_failed_checks(row):
    failed_checks = []

    if not row["data_quality_pass"]:
        failed_checks.append("数据质量或SRM未通过")

    if not row["sample_size_pass"]:
        failed_checks.append("样本量不足")

    if not row["statistical_significance_pass"]:
        failed_checks.append("未达到统计显著")

    if not row["business_significance_pass"]:
        failed_checks.append("业务提升不足")

    if not row["refund_guardrail_pass"]:
        failed_checks.append("退款率护栏未通过")

    if not row["error_guardrail_pass"]:
        failed_checks.append("错误率护栏未通过")

    if len(failed_checks) == 0:
        return "全部通过"

    return "；".join(failed_checks)


result["failed_checks"] = result.apply(
    get_failed_checks,
    axis=1,
)


# =========================
# 5. 生成最终建议
# =========================

def make_decision(row):
    if not row["data_quality_pass"]:
        return "暂停分析，先检查分流、埋点和数据质量"

    if (
        not row["refund_guardrail_pass"]
        or not row["error_guardrail_pass"]
    ):
        return "暂停上线，调查并修复护栏指标异常"

    if (
        not row["sample_size_pass"]
        or not row["statistical_significance_pass"]
    ):
        return "继续实验并积累足够样本"

    if not row["business_significance_pass"]:
        return "不建议上线，业务收益不足"

    return "具备上线条件，建议先小流量灰度发布"


result["final_decision"] = result.apply(
    make_decision,
    axis=1,
)

print("\n===== 最终实验决策 =====")
print(
    result[
        [
            "experiment_name",
            "failed_checks",
            "final_decision",
        ]
    ].T
)

# =========================
# 6. 不同实验场景测试
# =========================

decision_scenarios = pd.DataFrame(
    [
        {
            "experiment_name": "场景1_全部通过",
            "data_quality_pass": True,
            "sample_size_pass": True,
            "statistical_significance_pass": True,
            "business_significance_pass": True,
            "refund_guardrail_pass": True,
            "error_guardrail_pass": True,
        },
        {
            "experiment_name": "场景2_统计证据不足",
            "data_quality_pass": True,
            "sample_size_pass": False,
            "statistical_significance_pass": False,
            "business_significance_pass": True,
            "refund_guardrail_pass": True,
            "error_guardrail_pass": True,
        },
        {
            "experiment_name": "场景3_业务价值不足",
            "data_quality_pass": True,
            "sample_size_pass": True,
            "statistical_significance_pass": True,
            "business_significance_pass": False,
            "refund_guardrail_pass": True,
            "error_guardrail_pass": True,
        },
        {
            "experiment_name": "场景4_护栏未通过",
            "data_quality_pass": True,
            "sample_size_pass": True,
            "statistical_significance_pass": True,
            "business_significance_pass": True,
            "refund_guardrail_pass": False,
            "error_guardrail_pass": True,
        },
        {
            "experiment_name": "场景5_数据质量异常",
            "data_quality_pass": False,
            "sample_size_pass": True,
            "statistical_significance_pass": True,
            "business_significance_pass": True,
            "refund_guardrail_pass": True,
            "error_guardrail_pass": True,
        },
    ]
)

decision_scenarios["failed_checks"] = (
    decision_scenarios.apply(
        get_failed_checks,
        axis=1,
    )
)

decision_scenarios["final_decision"] = (
    decision_scenarios.apply(
        make_decision,
        axis=1,
    )
)

print("\n===== 不同实验场景决策 =====")
print(
    decision_scenarios[
        [
            "experiment_name",
            "failed_checks",
            "final_decision",
        ]
    ]
)

# =========================
# 7. 输出结果
# =========================

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

experiment_output_file = (
    OUTPUT_DIR
    / "ab_test_final_decision_week7_day4.csv"
)

scenario_output_file = (
    OUTPUT_DIR
    / "ab_test_decision_scenarios_week7_day4.csv"
)

result.to_csv(
    experiment_output_file,
    index=False,
    encoding="utf-8-sig",
)

decision_scenarios.to_csv(
    scenario_output_file,
    index=False,
    encoding="utf-8-sig",
)

print("\n===== 输出文件 =====")
print(experiment_output_file)
print(scenario_output_file)