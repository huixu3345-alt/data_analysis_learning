from math import ceil, comb, sqrt
from pathlib import Path

import numpy as np
import pandas as pd


# 每批100名用户，每名用户购买概率8%
n = 100
p = 0.08
target_successes = 8

expected_successes = n * p
variance = n * p * (1 - p)
standard_deviation = sqrt(variance)

probability_exactly_8 = (
    comb(n, target_successes)
    * (p ** target_successes)
    * ((1 - p) ** (n - target_successes))
)

probability_at_least_one = 1 - ((1 - p) ** n)

print("===== 二项分布理论结果 =====")
print("试验次数：", n)
print("单次成功概率：", p)
print("期望购买人数：", round(expected_successes, 2))
print("方差：", round(variance, 2))
print("标准差：", round(standard_deviation, 2))
print(
    "恰好8人购买的概率：",
    round(probability_exactly_8, 4),
)
print(
    "至少1人购买的概率：",
    round(probability_at_least_one, 4),
)

# =========================
# 模拟10000批用户
# =========================

rng = np.random.default_rng(42)

simulated_successes = rng.binomial(
    n=n,
    p=p,
    size=10000,
)

simulation_summary = pd.Series(
    simulated_successes
).describe(
    percentiles=[0.05, 0.50, 0.95]
)

print("\n===== 10000次模拟结果 =====")
print(simulation_summary.round(2))

# =========================
# 转化概率与活动收益
# =========================

contact_cost = 5
purchase_contribution = 80

expected_profit_per_user = (
    p * purchase_contribution
    - contact_cost
)

expected_profit_per_batch = (
    n * expected_profit_per_user
)

break_even_successes = ceil(
    n * contact_cost / purchase_contribution
)

simulated_batch_profit = (
    simulated_successes * purchase_contribution
    - n * contact_cost
)

profitable_batch_rate = (
    simulated_batch_profit > 0
).mean()

profit_summary = pd.Series(
    simulated_batch_profit
).describe(
    percentiles=[0.05, 0.50, 0.95]
)

print("\n===== 活动收益分析 =====")
print(
    "每名用户期望收益：",
    round(expected_profit_per_user, 2),
)
print(
    "每批100名用户期望收益：",
    round(expected_profit_per_batch, 2),
)
print(
    "达到盈利至少需要购买人数：",
    break_even_successes,
)
print(
    "模拟批次盈利比例：",
    round(profitable_batch_rate * 100, 2),
    "%",
)

print("\n===== 模拟批次收益分布 =====")
print(profit_summary.round(2))

# =========================
# 保存Day4分析结果
# =========================

PROJECT_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_DIR / "outputs"

OUTPUT_DIR.mkdir(exist_ok=True)

binomial_summary = pd.DataFrame(
    {
        "trial_count": [n],
        "success_probability": [p],
        "expected_successes": [expected_successes],
        "variance": [variance],
        "standard_deviation": [standard_deviation],
        "probability_exactly_8": [
            probability_exactly_8
        ],
        "probability_at_least_one": [
            probability_at_least_one
        ],
    }
)

profit_simulation_summary = pd.DataFrame(
    {
        "expected_profit_per_user": [
            expected_profit_per_user
        ],
        "expected_profit_per_batch": [
            expected_profit_per_batch
        ],
        "break_even_successes": [
            break_even_successes
        ],
        "profitable_batch_rate": [
            profitable_batch_rate
        ],
        "simulated_mean_profit": [
            simulated_batch_profit.mean()
        ],
        "simulated_std_profit": [
            simulated_batch_profit.std()
        ],
        "profit_p05": [
        np.quantile(simulated_batch_profit, 0.05)
        ],
        "profit_p50": [
            np.quantile(simulated_batch_profit, 0.50)
        ],
        "profit_p95": [
            np.quantile(simulated_batch_profit, 0.95)
        ],
    }
)

binomial_output_path = (
    OUTPUT_DIR / "binomial_summary_day4.csv"
)

profit_output_path = (
    OUTPUT_DIR / "profit_simulation_summary_day4.csv"
)

binomial_summary.round(4).to_csv(
    binomial_output_path,
    index=False,
    encoding="utf-8-sig",
)

profit_simulation_summary.round(4).to_csv(
    profit_output_path,
    index=False,
    encoding="utf-8-sig",
)

print("\n===== 输出文件 =====")
print(binomial_output_path)
print(profit_output_path)