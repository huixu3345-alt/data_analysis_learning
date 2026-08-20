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
    / "sales_visual_report_week8_day5.png"
)


# =========================
# 2. 设置图表样式
# =========================

plt.rcParams["font.sans-serif"] = [
    "Microsoft YaHei",
    "SimHei",
]
plt.rcParams["axes.unicode_minus"] = False

BLUE = "#2F7EBB"
ORANGE = "#F1A208"
GREY = "#8A8F98"
DARK = "#333333"
LIGHT_GREY = "#E6E8EB"

channel_colors = {
    "天猫": ORANGE,
    "抖音": BLUE,
    "京东": GREY,
}


# =========================
# 3. 读取并准备有效订单
# =========================

df = pd.read_csv(DATA_PATH)

for col in ["quantity", "net_sales"]:
    df[col] = pd.to_numeric(
        df[col],
        errors="coerce",
    )

valid_mask = (
    df["sales_amount_valid"]
    .astype(str)
    .str.lower()
    .eq("true")
)

valid_orders = df.loc[
    (df["order_status"] == "已完成")
    & valid_mask,
].copy()

valid_orders = valid_orders.dropna(
    subset=["quantity", "net_sales"]
)

dated_orders = valid_orders.dropna(
    subset=["order_month"]
).copy()


# =========================
# 4. 计算综合指标
# =========================

valid_order_count = len(valid_orders)
dated_order_count = len(dated_orders)
date_coverage_rate = (
    dated_order_count
    / valid_order_count
    * 100
)

total_net_sales = valid_orders["net_sales"].sum()
total_quantity = valid_orders["quantity"].sum()
avg_order_sales = valid_orders["net_sales"].mean()
median_order_sales = valid_orders["net_sales"].median()

quantity_sales_correlation = valid_orders[
    "quantity"
].corr(
    valid_orders["net_sales"]
)

channel_summary = (
    valid_orders
    .groupby("channel", as_index=False)
    .agg(
        order_count=("order_id", "count"),
        total_net_sales=("net_sales", "sum"),
    )
    .sort_values(
        "total_net_sales",
        ascending=False,
    )
)

monthly_summary = (
    dated_orders
    .groupby("order_month", as_index=False)
    .agg(
        order_count=("order_id", "count"),
        total_net_sales=("net_sales", "sum"),
    )
    .sort_values("order_month")
)


# =========================
# 5. 输出计算结果
# =========================

print("===== 综合指标 =====")
print("有效订单数量：", valid_order_count)
print("有效月份订单数量：", dated_order_count)
print("月份覆盖率：", round(date_coverage_rate, 2), "%")
print("总净销售额：", round(total_net_sales, 2))
print("总销量：", int(total_quantity))
print("平均每单销售额：", round(avg_order_sales, 2))
print("中位数销售额：", round(median_order_sales, 2))
print(
    "销量与销售额相关系数：",
    round(quantity_sales_correlation, 4),
)

print("\n===== 渠道汇总 =====")
print(channel_summary.round(2))

print("\n===== 月度汇总 =====")
print(monthly_summary.round(2))


# =========================
# 6. 创建六个分析面板
# =========================

fig, axes = plt.subplots(
    3,
    2,
    figsize=(16, 12),
)

fig.suptitle(
    "销售订单综合可视化分析",
    fontsize=24,
    fontweight="bold",
    y=0.985,
)


# 面板1：核心指标摘要
ax_kpi = axes[0, 0]
ax_kpi.axis("off")
ax_kpi.set_title(
    "核心指标摘要",
    fontsize=16,
    pad=16,
)

kpi_items = [
    ("有效订单", f"{valid_order_count} 笔"),
    ("总净销售额", f"{total_net_sales:,.2f} 元"),
    ("总销量", f"{int(total_quantity)} 件"),
    ("平均每单", f"{avg_order_sales:,.2f} 元"),
]

kpi_positions = [
    (0.25, 0.68),
    (0.75, 0.68),
    (0.25, 0.28),
    (0.75, 0.28),
]

for (label, value), (x_pos, y_pos) in zip(
    kpi_items,
    kpi_positions,
):
    ax_kpi.text(
        x_pos,
        y_pos,
        f"{value}\n{label}",
        ha="center",
        va="center",
        fontsize=16,
        linespacing=1.6,
        bbox={
            "boxstyle": "round,pad=0.5",
            "facecolor": "#F7F8FA",
            "edgecolor": LIGHT_GREY,
            "linewidth": 1.2,
        },
    )

ax_kpi.text(
    0.5,
    0.02,
    (
        f"月份字段覆盖：{dated_order_count}/{valid_order_count} "
        f"（{date_coverage_rate:.0f}%）"
    ),
    ha="center",
    fontsize=11,
    color="#666666",
)


# 面板2：渠道销售额柱状图
ax_channel = axes[0, 1]

channel_bar_colors = [
    ORANGE if index == 0 else BLUE
    for index in range(len(channel_summary))
]

channel_bars = ax_channel.bar(
    channel_summary["channel"],
    channel_summary["total_net_sales"],
    color=channel_bar_colors,
    edgecolor=DARK,
    linewidth=0.7,
)

ax_channel.set_title(
    "各渠道有效订单净销售额",
    fontsize=16,
    pad=14,
)
ax_channel.set_xlabel("销售渠道")
ax_channel.set_ylabel("净销售额（元）")
ax_channel.grid(
    axis="y",
    linestyle="--",
    alpha=0.3,
)

for bar, value in zip(
    channel_bars,
    channel_summary["total_net_sales"],
):
    ax_channel.text(
        bar.get_x() + bar.get_width() / 2,
        value,
        f"{value:.2f}",
        ha="center",
        va="bottom",
        fontsize=10,
    )


# 面板3：月度销售额柱状图
ax_month = axes[1, 0]

month_bar_colors = [
    ORANGE if value == monthly_summary["total_net_sales"].max()
    else BLUE
    for value in monthly_summary["total_net_sales"]
]

month_bars = ax_month.bar(
    monthly_summary["order_month"],
    monthly_summary["total_net_sales"],
    color=month_bar_colors,
    edgecolor=DARK,
    linewidth=0.7,
)

ax_month.set_title(
    "月度有效订单净销售额",
    fontsize=16,
    pad=30,
)
ax_month.set_xlabel("订单月份")
ax_month.set_ylabel("净销售额（元）")
ax_month.grid(
    axis="y",
    linestyle="--",
    alpha=0.3,
)

for bar, value in zip(
    month_bars,
    monthly_summary["total_net_sales"],
):
    ax_month.text(
        bar.get_x() + bar.get_width() / 2,
        value,
        f"{value:.2f}",
        ha="center",
        va="bottom",
        fontsize=10,
    )

ax_month.text(
    0.5,
    1.01,
    (
        f"仅包含{dated_order_count}笔有效月份订单；"
        f"覆盖率{date_coverage_rate:.0f}%；3个月不足以判断长期趋势"
    ),
    transform=ax_month.transAxes,
    ha="center",
    va="bottom",
    fontsize=9,
    color="#666666",
)


# 面板4：订单销售额直方图
ax_hist = axes[1, 1]

ax_hist.hist(
    valid_orders["net_sales"],
    bins=[0, 500, 1000, 1500, 2000],
    color=BLUE,
    edgecolor="white",
    linewidth=1.2,
)

ax_hist.axvline(
    avg_order_sales,
    color=ORANGE,
    linestyle="--",
    linewidth=2,
    label=f"均值 {avg_order_sales:.2f}元",
)
ax_hist.axvline(
    median_order_sales,
    color=DARK,
    linestyle=":",
    linewidth=2,
    label=f"中位数 {median_order_sales:.2f}元",
)

ax_hist.set_title(
    "单笔有效订单销售额分布",
    fontsize=16,
    pad=14,
)
ax_hist.set_xlabel("单笔订单净销售额区间（元）")
ax_hist.set_ylabel("订单数量（笔）")
ax_hist.grid(
    axis="y",
    linestyle="--",
    alpha=0.3,
)
ax_hist.legend(fontsize=9)


# 面板5：分渠道箱线图
ax_box = axes[2, 0]

channel_order = ["天猫", "抖音", "京东"]
box_data = [
    valid_orders.loc[
        valid_orders["channel"] == channel,
        "net_sales",
    ]
    for channel in channel_order
]

boxplot = ax_box.boxplot(
    box_data,
    tick_labels=[
        f"{channel}\nn={len(values)}"
        for channel, values in zip(
            channel_order,
            box_data,
        )
    ],
    patch_artist=True,
    showmeans=True,
    meanprops={
        "marker": "D",
        "markerfacecolor": "white",
        "markeredgecolor": DARK,
    },
    medianprops={
        "color": DARK,
        "linewidth": 2,
    },
)

for patch, channel in zip(
    boxplot["boxes"],
    channel_order,
):
    patch.set_facecolor(
        channel_colors[channel]
    )
    patch.set_alpha(0.75)

ax_box.set_title(
    "各渠道单笔订单销售额分布",
    fontsize=16,
    pad=14,
)
ax_box.set_xlabel("销售渠道")
ax_box.set_ylabel("单笔订单净销售额（元）")
ax_box.grid(
    axis="y",
    linestyle="--",
    alpha=0.3,
)


# 面板6：销量与销售额散点图
ax_scatter = axes[2, 1]

for channel, group in valid_orders.groupby("channel"):
    ax_scatter.scatter(
        group["quantity"],
        group["net_sales"],
        s=85,
        alpha=0.85,
        color=channel_colors.get(
            channel,
            GREY,
        ),
        edgecolor=DARK,
        linewidth=0.7,
        label=f"{channel}（n={len(group)}）",
    )

ax_scatter.set_title(
    (
        "订单销量与净销售额关系\n"
        f"相关系数 r={quantity_sales_correlation:.4f}"
    ),
    fontsize=16,
    pad=10,
)
ax_scatter.set_xlabel("单笔订单销量（件）")
ax_scatter.set_ylabel("单笔订单净销售额（元）")
ax_scatter.grid(
    linestyle="--",
    alpha=0.3,
)
ax_scatter.legend(
    title="销售渠道",
    fontsize=9,
)


# =========================
# 7. 保存并显示综合图表
# =========================

fig.text(
    0.5,
    0.012,
    (
        "数据范围：15笔有效订单；月份分析仅覆盖12笔；"
        "当前结果用于描述样本现象，不代表长期趋势或因果关系"
    ),
    ha="center",
    fontsize=11,
    color="#666666",
)

plt.tight_layout(
    rect=[0, 0.04, 1, 0.965],
    h_pad=3.0,
    w_pad=2.0,
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
