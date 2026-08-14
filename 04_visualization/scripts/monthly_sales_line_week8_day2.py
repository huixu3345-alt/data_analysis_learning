from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


# =========================
# 1. 设置项目路径
# =========================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = (
    PROJECT_ROOT
    / "01_python_pandas"
    / "outputs"
    / "monthly_sales_summary_week3.csv"
)

OUTPUT_PATH = (
    PROJECT_ROOT
    / "04_visualization"
    / "outputs"
    / "monthly_sales_line_week8_day2.png"
)


# =========================
# 2. 设置中文字体
# =========================

plt.rcParams["font.sans-serif"] = [
    "Microsoft YaHei",
    "SimHei",
]

plt.rcParams["axes.unicode_minus"] = False


# =========================
# 3. 读取月度销售数据
# =========================

df = pd.read_csv(DATA_PATH)

print("===== 月度销售数据 =====")
print(df)

print("\n数据行数：", len(df))
print("字段名称：", df.columns.tolist())

# =========================
# 4. 转换月份并按时间排序
# =========================

df["order_month"] = pd.to_datetime(
    df["order_month"],
    format="%Y-%m",
)

df = df.sort_values(
    "order_month",
    ascending=True,
).reset_index(drop=True)

print("\n===== 按时间升序排列 =====")
print(df[["order_month", "net_sales"]])

# =========================
# 5. 计算环比变化
# =========================

df["sales_growth_amount"] = (
    df["net_sales"].diff()
)

df["sales_growth_rate"] = (
    df["net_sales"].pct_change() * 100
).round(2)

print("\n===== 月度销售额环比变化 =====")

print(
    df[
        [
            "order_month",
            "net_sales",
            "sales_growth_amount",
            "sales_growth_rate",
        ]
    ].round(2)
)

# =========================
# 5. 绘制月度销售额折线图
# =========================

fig, ax = plt.subplots(
    figsize=(11, 7),
)

ax.plot(
    df["order_month"],
    df["net_sales"],
    color="#2F7EBB",
    marker="o",
    linewidth=2.5,
    markersize=8,
)

ax.set_title(
    "月度有效订单销售额",
    fontsize=20,
    pad=18,
)

ax.set_xlabel(
    "订单月份",
    fontsize=13,
)

ax.set_ylabel(
    "销售额（元）",
    fontsize=13,
)

ax.grid(
    axis="y",
    linestyle="--",
    alpha=0.3,
)

# =========================
# 6. 设置月份格式和数值标签
# =========================

month_labels = df["order_month"].dt.strftime("%Y-%m")

ax.set_xticks(df["order_month"])
ax.set_xticklabels(month_labels)

for x, y in zip(
    df["order_month"],
    df["net_sales"],
):
    ax.annotate(
        f"{y:.2f}",
        xy=(x, y),
        xytext=(0, 10),
        textcoords="offset points",
        ha="center",
        fontsize=11,
    )
    
# =========================
# 7. 标注环比增长率
# =========================

for i in range(1, len(df)):
    previous_month = df.loc[i - 1, "order_month"]
    current_month = df.loc[i, "order_month"]

    previous_sales = df.loc[i - 1, "net_sales"]
    current_sales = df.loc[i, "net_sales"]

    growth_rate = df.loc[i, "sales_growth_rate"]

    middle_x = (
        previous_month
        + (current_month - previous_month) / 2
    )

    middle_y = (
        previous_sales + current_sales
    ) / 2

    ax.annotate(
        f"环比 +{growth_rate:.2f}%",
        xy=(middle_x, middle_y),
        xytext=(0, 12),
        textcoords="offset points",
        ha="center",
        fontsize=11,
        color="#E58B18",
        fontweight="bold",
    )

fig.text(
    0.5,
    0.02,
    "数据范围：3个有效月份；数据点较少，仅用于观察当前阶段变化",
    ha="center",
    fontsize=11,
    color="#666666",
)

plt.tight_layout(
    rect=[0, 0.05, 1, 1],
)

OUTPUT_PATH.parent.mkdir(
    parents=True,
    exist_ok=True,
)

fig.savefig(
    OUTPUT_PATH,
    dpi=150,
    bbox_inches="tight",
)

print("\n已生成：")
print(OUTPUT_PATH)

plt.show()