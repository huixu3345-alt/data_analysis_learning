from pathlib import Path

import pandas as pd


experiment_results = pd.DataFrame(
    {
        "group": ["A", "B"],
        "exposed_users": [5000, 5100],
        "paying_users": [400, 459],
        "refund_users": [20, 35],
        "error_users": [50, 80],
    }
)

experiment_results["conversion_rate"] = (
    experiment_results["paying_users"]
    / experiment_results["exposed_users"]
)

experiment_results["refund_rate"] = (
    experiment_results["refund_users"]
    / experiment_results["paying_users"]
)

experiment_results["error_rate"] = (
    experiment_results["error_users"]
    / experiment_results["exposed_users"]
)

total_exposed_users = (
    experiment_results["exposed_users"].sum()
)

experiment_results["traffic_share"] = (
    experiment_results["exposed_users"]
    / total_exposed_users
)

print("===== A/B测试基础结果 =====")
print(experiment_results.round(4))

# =========================
# A组与B组指标差异
# =========================

results_by_group = (
    experiment_results
    .set_index("group")
)

group_a = results_by_group.loc["A"]
group_b = results_by_group.loc["B"]

absolute_conversion_uplift = (
    group_b["conversion_rate"]
    - group_a["conversion_rate"]
)

relative_conversion_uplift = (
    absolute_conversion_uplift
    / group_a["conversion_rate"]
)

refund_rate_change = (
    group_b["refund_rate"]
    - group_a["refund_rate"]
)

error_rate_change = (
    group_b["error_rate"]
    - group_a["error_rate"]
)

print("\n===== 核心指标与护栏指标 =====")
print(
    "A组支付转化率：",
    round(group_a["conversion_rate"] * 100, 2),
    "%",
)
print(
    "B组支付转化率：",
    round(group_b["conversion_rate"] * 100, 2),
    "%",
)
print(
    "转化率绝对提升：",
    round(absolute_conversion_uplift * 100, 2),
    "个百分点",
)
print(
    "转化率相对提升：",
    round(relative_conversion_uplift * 100, 2),
    "%",
)
print(
    "退款率变化：",
    round(refund_rate_change * 100, 2),
    "个百分点",
)
print(
    "页面错误率变化：",
    round(error_rate_change * 100, 2),
    "个百分点",
)

# =========================
# 预设护栏阈值与初步决策
# =========================

max_refund_rate_increase = 0.01
max_error_rate_increase = 0.002

refund_guardrail_pass = (
    refund_rate_change
    <= max_refund_rate_increase
)

error_guardrail_pass = (
    error_rate_change
    <= max_error_rate_increase
)

all_guardrails_pass = (
    refund_guardrail_pass
    and error_guardrail_pass
)

if not all_guardrails_pass:
    preliminary_decision = (
        "暂缓上线：护栏指标超过预设范围"
    )
elif absolute_conversion_uplift <= 0:
    preliminary_decision = (
        "不建议上线：核心指标没有提升"
    )
else:
    preliminary_decision = (
        "进入下一步统计显著性检验"
    )

print("\n===== 护栏检查与初步决策 =====")
print(
    "退款率允许最大增幅：",
    max_refund_rate_increase * 100,
    "个百分点",
)
print(
    "实际退款率增幅：",
    round(refund_rate_change * 100, 2),
    "个百分点",
)
print(
    "退款率护栏是否通过：",
    refund_guardrail_pass,
)
print(
    "错误率允许最大增幅：",
    max_error_rate_increase * 100,
    "个百分点",
)
print(
    "实际错误率增幅：",
    round(error_rate_change * 100, 2),
    "个百分点",
)
print(
    "错误率护栏是否通过：",
    error_guardrail_pass,
)
print("初步决策：", preliminary_decision)

# =========================
# 保存Week7 Day1结果
# =========================

PROJECT_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_DIR / "outputs"

OUTPUT_DIR.mkdir(exist_ok=True)

experiment_design = pd.DataFrame(
    {
        "design_item": [
            "business_question",
            "control_group",
            "treatment_group",
            "experiment_unit",
            "randomization",
            "primary_metric",
            "refund_guardrail",
            "error_guardrail",
            "exclusions",
        ],
        "design_value": [
            "新版结算页能否提高支付转化率",
            "旧版结算页",
            "新版结算页",
            "user_id",
            "按user_id随机50/50固定分组",
            "支付独立用户数/曝光独立用户数",
            "退款率增加不超过1个百分点",
            "错误率增加不超过0.2个百分点",
            "员工、测试账号、机器人和异常流量",
        ],
    }
)

decision_summary = pd.DataFrame(
    {
        "absolute_conversion_uplift": [
            absolute_conversion_uplift
        ],
        "relative_conversion_uplift": [
            relative_conversion_uplift
        ],
        "refund_rate_change": [
            refund_rate_change
        ],
        "error_rate_change": [
            error_rate_change
        ],
        "refund_guardrail_pass": [
            refund_guardrail_pass
        ],
        "error_guardrail_pass": [
            error_guardrail_pass
        ],
        "preliminary_decision": [
            preliminary_decision
        ],
    }
)

design_output_path = (
    OUTPUT_DIR / "ab_test_design_week7_day1.csv"
)

metrics_output_path = (
    OUTPUT_DIR / "ab_test_metrics_week7_day1.csv"
)

decision_output_path = (
    OUTPUT_DIR / "ab_test_decision_week7_day1.csv"
)

experiment_design.to_csv(
    design_output_path,
    index=False,
    encoding="utf-8-sig",
)

experiment_results.round(4).to_csv(
    metrics_output_path,
    index=False,
    encoding="utf-8-sig",
)

decision_summary.round(4).to_csv(
    decision_output_path,
    index=False,
    encoding="utf-8-sig",
)

print("\n===== 输出文件 =====")
print(design_output_path)
print(metrics_output_path)
print(decision_output_path)