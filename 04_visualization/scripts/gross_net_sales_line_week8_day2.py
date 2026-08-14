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
    / "monthly_sales_summary_week3.csv"
)

OUTPUT_PATH = (
    PROJECT_ROOT
    / "04_visualization"
    / "outputs"
    / "gross_net_sales_line_week8_day2.png"
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
# 3. 读取并整理数据
# =========================

df = pd.read_csv(DATA_PATH)

df["order_month"] = pd.to_datetime(
    df["order_month"],
    format="%Y-%m",
)

df = df.sort_values(
    "order_month",
    ascending=True,
).reset_index(drop=True)

print("===== 月度折扣前后销售额 =====")

print(
    df[
        [
            "order_month",
            "gross_sales",
            "net_sales",
        ]
    ]
)


# =========================
# 4. 计算折扣影响金额
# =========================

df["discount_amount"] = (
    df["gross_sales"] - df["net_sales"]
)

print("\n===== 折扣影响金额 =====")

print(
    df[
        [
            "order_month",
            "gross_sales",
            "net_sales",
            "discount_amount",
        ]
    ].round(2)
)


# =========================
# 5. 创建画布
# =========================

fig, ax = plt.subplots(
    figsize=(11, 7),
)


# =========================
# 6. 绘制折扣前销售额
# =========================

ax.plot(
    df["order_month"],
    df["gross_sales"],
    color="#E58B18",
    marker="o",
    linewidth=2.5,
    markersize=8,
    label="折扣前销售额",
)


# =========================
# 7. 绘制折扣后销售额
# =========================

ax.plot(
    df["order_month"],
    df["net_sales"],
    color="#2F7EBB",
    marker="o",
    linewidth=2.5,
    markersize=8,
    label="折扣后销售额",
)


# =========================
# 8. 设置标题和坐标轴
# =========================

ax.set_title(
    "月度折扣前后销售额对比",
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

ax.set_ylim(bottom=0)

ax.grid(
    axis="y",
    linestyle="--",
    alpha=0.3,
)


# =========================
# 9. 设置月份格式
# =========================

month_labels = df["order_month"].dt.strftime("%Y-%m")

ax.set_xticks(df["order_month"])
ax.set_xticklabels(month_labels)


# =========================
# 10. 添加图例
# =========================

ax.legend(
    loc="upper left",
    fontsize=11,
)


# =========================
# 11. 添加数值标签
# =========================

for x, gross_sales, net_sales in zip(
    df["order_month"],
    df["gross_sales"],
    df["net_sales"],
):
    ax.annotate(
        f"{gross_sales:.2f}",
        xy=(x, gross_sales),
        xytext=(0, 9),
        textcoords="offset points",
        ha="center",
        fontsize=10,
        color="#B66D0F",
    )

    ax.annotate(
        f"{net_sales:.2f}",
        xy=(x, net_sales),
        xytext=(0, -17),
        textcoords="offset points",
        ha="center",
        fontsize=10,
        color="#245F8D",
    )


# =========================
# 12. 添加数据范围说明
# =========================

fig.text(
    0.5,
    0.02,
    "数据范围：3个有效月份；折扣前后销售额单位均为元",
    ha="center",
    fontsize=11,
    color="#666666",
)

plt.tight_layout(
    rect=[0, 0.05, 1, 1],
)


# =========================
# 13. 保存并显示图表
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