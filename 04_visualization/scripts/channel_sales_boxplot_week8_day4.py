from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


# =========================
# 1. 设置文件路径
# =========================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = (
    PROJECT_ROOT
    / "01_python_pandas"
    / "outputs"
    / "sales_valid_analysis_week3.csv"
)

OUTPUT_PATH = (
    PROJECT_ROOT
    / "04_visualization"
    / "outputs"
    / "channel_sales_boxplot_week8_day4.png"
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
# 3. 读取数据
# =========================

df = pd.read_csv(DATA_PATH)

df["net_sales"] = pd.to_numeric(
    df["net_sales"],
    errors="coerce",
)

analysis_df = df[
    [
        "channel",
        "net_sales",
    ]
].dropna()

print("===== 渠道订单销售额数据 =====")
print(analysis_df)

print("\n数据行数：", len(analysis_df))


# =========================
# 4. 分渠道描述性统计
# =========================

channel_summary = (
    analysis_df
    .groupby("channel")["net_sales"]
    .describe()
    .round(2)
)

print("\n===== 分渠道描述性统计 =====")

print(
    channel_summary[
        [
            "count",
            "min",
            "25%",
            "50%",
            "75%",
            "max",
        ]
    ]
)

# =========================
# 5. 使用IQR检查异常值候选
# =========================

outlier_summary = []
outlier_records = []

for channel, group in analysis_df.groupby(
    "channel"
):
    q1 = group["net_sales"].quantile(0.25)
    q3 = group["net_sales"].quantile(0.75)

    iqr = q3 - q1

    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    candidates = group[
        (group["net_sales"] < lower_bound)
        | (group["net_sales"] > upper_bound)
    ]

    outlier_summary.append(
        {
            "channel": channel,
            "q1": q1,
            "q3": q3,
            "iqr": iqr,
            "lower_bound": lower_bound,
            "upper_bound": upper_bound,
            "candidate_count": len(candidates),
        }
    )

    for _, row in candidates.iterrows():
        outlier_records.append(
            {
                "channel": channel,
                "net_sales": row["net_sales"],
            }
        )

outlier_summary_df = pd.DataFrame(
    outlier_summary
).round(2)

outlier_records_df = pd.DataFrame(
    outlier_records
)

print("\n===== 各渠道IQR异常值边界 =====")
print(outlier_summary_df)

print("\n===== 异常值候选记录 =====")
print(outlier_records_df)

# =========================
# 6. 准备箱线图数据
# =========================

channel_order = [
    "天猫",
    "抖音",
    "京东",
]

boxplot_data = [
    analysis_df.loc[
        analysis_df["channel"] == channel,
        "net_sales",
    ]
    for channel in channel_order
]

channel_labels = [
    f"{channel}\nn={len(data)}"
    for channel, data in zip(
        channel_order,
        boxplot_data,
    )
]


# =========================
# 7. 创建箱线图
# =========================

fig, ax = plt.subplots(
    figsize=(11, 7),
)

boxplot = ax.boxplot(
    boxplot_data,
    tick_labels=channel_labels,
    patch_artist=True,
    widths=0.55,
    showmeans=True,
    medianprops={
        "color": "#222222",
        "linewidth": 2.2,
    },
    meanprops={
        "marker": "D",
        "markerfacecolor": "white",
        "markeredgecolor": "#222222",
        "markersize": 7,
    },
    whiskerprops={
        "color": "#555555",
        "linewidth": 1.6,
    },
    capprops={
        "color": "#555555",
        "linewidth": 1.6,
    },
    flierprops={
        "marker": "o",
        "markerfacecolor": "#E58B18",
        "markeredgecolor": "#B66D0F",
        "markersize": 8,
    },
)


# =========================
# 8. 设置箱体颜色
# =========================

box_colors = [
    "#F1A208",
    "#2F7EBB",
    "#8A8F98",
]

for patch, color in zip(
    boxplot["boxes"],
    box_colors,
):
    patch.set_facecolor(color)
    patch.set_alpha(0.75)


# =========================
# 9. 设置标题和坐标轴
# =========================

ax.set_title(
    "各渠道有效订单销售额分布",
    fontsize=20,
    pad=18,
)

ax.set_xlabel(
    "销售渠道",
    fontsize=13,
)

ax.set_ylabel(
    "单笔订单销售额（元）",
    fontsize=13,
)

ax.grid(
    axis="y",
    linestyle="--",
    alpha=0.3,
)


# =========================
# 10. 添加图表说明
# =========================

fig.text(
    0.5,
    0.02,
    "数据范围：15笔有效订单；菱形表示均值，箱体中线表示中位数，独立圆点表示异常值候选",
    ha="center",
    fontsize=11,
    color="#666666",
)

plt.tight_layout(
    rect=[0, 0.05, 1, 1],
)


# =========================
# 11. 保存并显示图表
# =========================

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