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
    / "quantity_sales_scatter_week8_day5.png"
)


# =========================
# 2. 读取并筛选有效订单
# =========================

df = pd.read_csv(DATA_PATH)

valid_mask = (
    df["sales_amount_valid"]
    .astype(str)
    .str.lower()
    .eq("true")
)

analysis_df = df.loc[
    (df["order_status"] == "已完成")
    & valid_mask,
    [
        "order_id",
        "channel",
        "product_name",
        "quantity",
        "unit_price",
        "discount_rate",
        "net_sales",
    ],
].copy()

analysis_df = analysis_df.dropna(
    subset=["quantity", "net_sales"]
)


# =========================
# 3. 计算相关系数
# =========================

correlation = analysis_df[
    "quantity"
].corr(
    analysis_df["net_sales"]
)

print("===== 散点图分析数据 =====")
print(analysis_df)

print("\n有效订单数量：", len(analysis_df))
print("销量与销售额相关系数：", round(correlation, 4))


# =========================
# 4. 绘制散点图
# =========================

plt.rcParams["font.sans-serif"] = [
    "Microsoft YaHei",
    "SimHei",
]

plt.rcParams["axes.unicode_minus"] = False

channel_colors = {
    "天猫": "#F1A208",
    "抖音": "#2F7EBB",
    "京东": "#8A8F98",
}

fig, ax = plt.subplots(
    figsize=(11, 7)
)

for channel, group in analysis_df.groupby("channel"):
    ax.scatter(
        group["quantity"],
        group["net_sales"],
        s=110,
        alpha=0.85,
        color=channel_colors.get(
            channel,
            "#666666",
        ),
        edgecolor="#333333",
        linewidth=0.8,
        label=f"{channel}（n={len(group)}）",
    )

    for _, row in group.iterrows():
        ax.annotate(
            row["order_id"],
            (
                row["quantity"],
                row["net_sales"],
            ),
            xytext=(5, 5),
            textcoords="offset points",
            fontsize=8,
        )

ax.set_title(
    "订单销量与净销售额关系",
    fontsize=20,
    pad=18,
)

ax.set_xlabel(
    "单笔订单销量（件）",
    fontsize=13,
)

ax.set_ylabel(
    "单笔订单净销售额（元）",
    fontsize=13,
)

ax.grid(
    linestyle="--",
    alpha=0.3,
)

ax.legend(
    title="销售渠道"
)

fig.text(
    0.5,
    0.02,
    "数据范围：15笔有效订单；每个点代表一笔订单；相关关系不代表因果关系",
    ha="center",
    fontsize=11,
    color="#666666",
)

plt.tight_layout(
    rect=[0, 0.06, 1, 1]
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