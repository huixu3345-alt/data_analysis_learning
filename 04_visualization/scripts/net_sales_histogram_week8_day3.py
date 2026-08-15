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
    / "net_sales_histogram_week8_day3.png"
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
# 3. 读取有效订单
# =========================

df = pd.read_csv(DATA_PATH)

skewness = sales.skew()

print(
    "销售额偏度：",
    round(skewness, 4),
)

sales = pd.to_numeric(
    df["net_sales"],
    errors="coerce",
).dropna()

print("===== 有效订单销售额 =====")
print(sales.sort_values().reset_index(drop=True))

print("\n订单数量：", sales.count())
print("最低销售额：", round(sales.min(), 2))
print("最高销售额：", round(sales.max(), 2))
print("平均销售额：", round(sales.mean(), 2))
print("中位数销售额：", round(sales.median(), 2))

# =========================
# 4. 设置分箱
# =========================

bins = [
    0,
    500,
    1000,
    1500,
    2000,
]


# =========================
# 5. 绘制销售额直方图
# =========================

fig, ax = plt.subplots(
    figsize=(11, 7),
)

counts, bin_edges, patches = ax.hist(
    sales,
    bins=bins,
    color="#2F7EBB",
    edgecolor="white",
    linewidth=1.5,
)

# =========================
# 6. 添加均值线和中位数线
# =========================

mean_sales = sales.mean()
median_sales = sales.median()

ax.axvline(
    mean_sales,
    color="#E58B18",
    linestyle="--",
    linewidth=2.5,
    label=f"均值：{mean_sales:.2f}元",
)

ax.axvline(
    median_sales,
    color="#333333",
    linestyle=":",
    linewidth=2.5,
    label=f"中位数：{median_sales:.2f}元",
)

ax.legend(
    loc="upper right",
    fontsize=11,
)

# =========================
# 6. 设置标题和坐标轴
# =========================

ax.set_title(
    "有效订单销售额分布",
    fontsize=20,
    pad=18,
)

ax.set_xlabel(
    "订单销售额区间（元）",
    fontsize=13,
)

ax.set_ylabel(
    "订单数量（笔）",
    fontsize=13,
)

ax.set_xticks(bins)

ax.grid(
    axis="y",
    linestyle="--",
    alpha=0.3,
)


# =========================
# 7. 添加频数标签
# =========================

for count, patch in zip(
    counts,
    patches,
):
    ax.annotate(
        f"{int(count)}",
        xy=(
            patch.get_x()
            + patch.get_width() / 2,
            patch.get_height(),
        ),
        xytext=(0, 7),
        textcoords="offset points",
        ha="center",
        fontsize=11,
    )


# =========================
# 8. 添加数据范围说明
# =========================

fig.text(
    0.5,
    0.02,
    "数据范围：15笔有效订单；每个区间宽度为500元",
    ha="center",
    fontsize=11,
    color="#666666",
)

plt.tight_layout(
    rect=[0, 0.05, 1, 1],
)


# =========================
# 9. 保存并显示图表
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

print("\n===== 各区间订单数量 =====")

for left, right, count in zip(
    bin_edges[:-1],
    bin_edges[1:],
    counts,
):
    print(
        f"{left:.0f}～{right:.0f}元："
        f"{int(count)}笔"
    )

print("\n已生成：")
print(OUTPUT_PATH)

plt.show()