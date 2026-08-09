from pathlib import Path

import pandas as pd


# =========================
# 1. 路径设置
# =========================

PROJECT_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_DIR / "outputs"

METRICS_FILE = (
    OUTPUT_DIR
    / "ab_test_metrics_week7_day1.csv"
)

SRM_FILE = (
    OUTPUT_DIR
    / "ab_test_srm_week7_day2.csv"
)

DIFFERENCE_FILE = (
    OUTPUT_DIR
    / "ab_test_difference_test_week7_day2.csv"
)

SAMPLE_SIZE_FILE = (
    OUTPUT_DIR
    / "ab_test_sample_size_scenarios_week7_day3.csv"
)

DECISION_FILE = (
    OUTPUT_DIR
    / "ab_test_final_decision_week7_day4.csv"
)


# =========================
# 2. 读取前4天的分析结果
# =========================

metrics = pd.read_csv(METRICS_FILE)
srm_result = pd.read_csv(SRM_FILE).iloc[0]
difference_result = pd.read_csv(
    DIFFERENCE_FILE
).iloc[0]

sample_size_scenarios = pd.read_csv(
    SAMPLE_SIZE_FILE
)

final_decision = pd.read_csv(
    DECISION_FILE
).iloc[0]


print("===== A/B两组指标 =====")
print(metrics)

print("\n===== SRM结果 =====")
print(srm_result)

print("\n===== 差异检验结果 =====")
print(difference_result)

print("\n===== 样本量方案 =====")
print(sample_size_scenarios)

print("\n===== 最终决策 =====")
print(final_decision)

# =========================
# 3. 提取关键记录
# =========================

group_a = metrics.loc[
    metrics["group"] == "A"
].iloc[0]

group_b = metrics.loc[
    metrics["group"] == "B"
].iloc[0]

baseline_scenario = sample_size_scenarios.loc[
    sample_size_scenarios["scenario"] == "基准方案"
].iloc[0]


# =========================
# 4. 生成核心结果摘要
# =========================

report_summary = pd.DataFrame(
    [
        {
            "metric": "A组转化率",
            "result": (
                f"{group_a['conversion_rate'] * 100:.2f}%"
            ),
            "interpretation": "对照组表现",
        },
        {
            "metric": "B组转化率",
            "result": (
                f"{group_b['conversion_rate'] * 100:.2f}%"
            ),
            "interpretation": "实验组表现",
        },
        {
            "metric": "转化率绝对提升",
            "result": (
                f"{difference_result['rate_difference'] * 100:.2f}"
                " 个百分点"
            ),
            "interpretation": "具有潜在业务价值",
        },
        {
            "metric": "效果检验p值",
            "result": (
                f"{difference_result['two_sided_p_value']:.4f}"
            ),
            "interpretation": "大于0.05，未达到统计显著",
        },
        {
            "metric": "差异95%置信区间",
            "result": (
                f"{difference_result['difference_ci_lower'] * 100:.2f}"
                " 至 "
                f"{difference_result['difference_ci_upper'] * 100:.2f}"
                " 个百分点"
            ),
            "interpretation": "包含0，不能排除没有真实差异",
        },
        {
            "metric": "SRM检查",
            "result": (
                f"p={srm_result['srm_p_value']:.4f}"
            ),
            "interpretation": "暂未发现明显分流异常",
        },
        {
            "metric": "基准方案每组样本要求",
            "result": (
                f"{int(baseline_scenario['required_sample_per_group'])}"
                " 人"
            ),
            "interpretation": "A、B两组实际样本均不足",
        },
        {
            "metric": "退款率护栏",
            "result": (
                f"增加{final_decision['refund_rate_increase'] * 100:.2f}"
                " 个百分点"
            ),
            "interpretation": "超过预设阈值，未通过",
        },
        {
            "metric": "错误率护栏",
            "result": (
                f"增加{final_decision['error_rate_increase'] * 100:.2f}"
                " 个百分点"
            ),
            "interpretation": "超过预设阈值，未通过",
        },
        {
            "metric": "最终建议",
            "result": final_decision["final_decision"],
            "interpretation": final_decision["failed_checks"],
        },
    ]
)

print("\n===== 核心结果摘要 =====")
print(report_summary)

# =========================
# 5. 一致性验证
# =========================

calculated_a_rate = (
    group_a["paying_users"]
    / group_a["exposed_users"]
)

calculated_b_rate = (
    group_b["paying_users"]
    / group_b["exposed_users"]
)

calculated_traffic_share = (
    group_a["traffic_share"]
    + group_b["traffic_share"]
)

calculated_absolute_lift = (
    group_b["conversion_rate"]
    - group_a["conversion_rate"]
)

validation_summary = pd.DataFrame(
    [
        {
            "check_item": "A组转化率一致",
            "check_pass": abs(
                calculated_a_rate
                - group_a["conversion_rate"]
            ) < 0.000001,
        },
        {
            "check_item": "B组转化率一致",
            "check_pass": abs(
                calculated_b_rate
                - group_b["conversion_rate"]
            ) < 0.000001,
        },
        {
            "check_item": "两组流量占比合计为100%",
            "check_pass": abs(
                calculated_traffic_share - 1
            ) < 0.000001,
        },
        {
            "check_item": "转化率绝对提升一致",
            "check_pass": abs(
                calculated_absolute_lift
                - difference_result["rate_difference"]
            ) < 0.000001,
        },
    ]
)

all_validations_pass = (
    validation_summary["check_pass"].all()
)

print("\n===== 一致性验证 =====")
print(validation_summary)

print(
    "\n所有一致性检查是否通过：",
    all_validations_pass,
)


# =========================
# 6. 生成完整实验报告
# =========================

report_text = f"""# 新版结算页 A/B 测试实验报告

## 一、业务问题

本次实验用于判断新版结算页能否提高用户支付转化率，同时确保退款率和页面错误率不超过业务可接受范围。

## 二、实验设计

- A组：对照组，使用旧版结算页
- B组：实验组，使用新版结算页
- 实验单位：用户
- 核心指标：支付转化率
- 护栏指标：退款率、页面错误率
- 显著性水平：{final_decision['alpha']:.2f}
- 统计设计 MDE：{final_decision['statistical_mde'] * 100:.2f} 个百分点
- 业务最低提升要求：{final_decision['business_minimum_lift'] * 100:.2f} 个百分点

## 三、数据质量与分流检查

- A组用户数：{int(group_a['exposed_users'])}
- B组用户数：{int(group_b['exposed_users'])}
- A组流量占比：{group_a['traffic_share'] * 100:.2f}%
- B组流量占比：{group_b['traffic_share'] * 100:.2f}%
- SRM p-value：{srm_result['srm_p_value']:.4f}
- 是否发现 SRM 异常：{srm_result['srm_detected']}
- 所有关键指标一致性检查是否通过：{all_validations_pass}

SRM p-value 大于 0.05，暂未发现实际分流比例明显偏离预期，可以继续分析实验效果。但这不代表已经证明分流绝对不存在问题。

## 四、核心指标结果

- A组转化率：{group_a['conversion_rate'] * 100:.2f}%
- B组转化率：{group_b['conversion_rate'] * 100:.2f}%
- 绝对提升：{difference_result['rate_difference'] * 100:.2f} 个百分点
- 相对提升：{(difference_result['rate_difference'] / group_a['conversion_rate']) * 100:.2f}%

B组样本转化率高于A组，观察到的提升达到业务最低要求，具有潜在业务价值。

## 五、统计显著性

- 双侧 p-value：{difference_result['two_sided_p_value']:.4f}
- 差异95%置信区间：{difference_result['difference_ci_lower'] * 100:.2f} 至 {difference_result['difference_ci_upper'] * 100:.2f} 个百分点
- 置信区间是否包含0：{difference_result['ci_includes_zero']}
- 是否达到统计显著：{difference_result['statistically_significant']}

p-value 大于 0.05，且差异置信区间包含0。目前证据不足以排除随机波动，因此不能认定B组带来了真实提升。但未达到统计显著也不等于已经证明B组无效。

## 六、样本量与统计功效

- 基准方案每组所需样本量：{int(baseline_scenario['required_sample_per_group'])}
- A组实际样本量：{int(group_a['exposed_users'])}
- B组实际样本量：{int(group_b['exposed_users'])}
- A组样本量是否充足：{baseline_scenario['group_a_sufficient']}
- B组样本量是否充足：{baseline_scenario['group_b_sufficient']}

当前两组实际样本量均低于预设要求，统计功效可能不足，存在漏掉真实效果的第二类错误风险。这里不能断言第二类错误已经发生，因为真实效果仍然未知。

## 七、护栏指标

- 退款率增加：{final_decision['refund_rate_increase'] * 100:.2f} 个百分点
- 退款率允许最大增幅：{final_decision['refund_guardrail_limit'] * 100:.2f} 个百分点
- 退款率护栏是否通过：{final_decision['refund_guardrail_pass']}
- 错误率增加：{final_decision['error_rate_increase'] * 100:.2f} 个百分点
- 错误率允许最大增幅：{final_decision['error_guardrail_limit'] * 100:.2f} 个百分点
- 错误率护栏是否通过：{final_decision['error_guardrail_pass']}

退款率和错误率均超过预设容忍范围。即使核心指标以后达到统计显著，也不能忽略这些潜在负面影响。

## 八、综合结论

本次实验暂未发现明显分流异常，B组转化率比A组高1个百分点，观察到的提升具有潜在业务价值。但是核心指标未达到统计显著，实际样本量低于预设要求，而且退款率和错误率护栏均未通过。

失败检查：{final_decision['failed_checks']}

最终建议：{final_decision['final_decision']}

## 九、后续行动

1. 暂不全量上线新版结算页。
2. 优先排查退款率和错误率上升的原因，包括页面流程、支付故障和埋点质量。
3. 修复护栏问题后重新开展实验。
4. 保持预设的显著性水平、MDE和统计功效，不根据结果随意修改标准。
5. 继续积累至预设样本量后，重新检查置信区间、p-value和护栏指标。
6. 如果全部条件通过，先进行小流量灰度发布并持续监控，保留回滚能力。
"""


# =========================
# 7. 输出报告和明细文件
# =========================

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

summary_output_file = (
    OUTPUT_DIR
    / "ab_test_report_summary_week7_day5.csv"
)

validation_output_file = (
    OUTPUT_DIR
    / "ab_test_report_validation_week7_day5.csv"
)

report_output_file = (
    OUTPUT_DIR
    / "ab_test_final_report_week7_day5.md"
)

report_summary.to_csv(
    summary_output_file,
    index=False,
    encoding="utf-8-sig",
)

validation_summary.to_csv(
    validation_output_file,
    index=False,
    encoding="utf-8-sig",
)

report_output_file.write_text(
    report_text,
    encoding="utf-8",
)

print("\n===== 输出文件 =====")
print(summary_output_file)
print(validation_output_file)
print(report_output_file)
