from pathlib import Path

import pandas as pd

import matplotlib.pyplot as plt


# 当前脚本所在文件夹：04_visualization/scripts
SCRIPT_DIR = Path(__file__).resolve().parent

# 项目根目录：D:\data_analysis_learning
PROJECT_ROOT = SCRIPT_DIR.parent.parent

# 找到之前生成的渠道销售汇总数据
DATA_FILE = (
    PROJECT_ROOT
    / "01_python_pandas"
    / "outputs"
    / "channel_sales_summary_week3.csv"
)

# 读取CSV文件
df = pd.read_csv(DATA_FILE)

print("===== 渠道销售数据 =====")
print(df)

print("\n数据行数：", len(df))
print("字段名称：", df.columns.tolist())

# =========================
# 2. 准备绘图数据
# =========================

# 排序指标
plot_data = df.sort_values(
    "sales_quantity",
    ascending=False,
)

print("\n===== 排序后的绘图数据 =====")
print(plot_data[["channel", "sales_quantity"]])


# =========================
# 3. 设置中文字体
# =========================

plt.rcParams["font.sans-serif"] = [
    "Microsoft YaHei",
    "SimHei",
]

# 避免坐标轴负号显示异常
plt.rcParams["axes.unicode_minus"] = False


# =========================
# 4. 创建柱状图
# =========================

fig, ax = plt.subplots(
    figsize=(8, 5),
)

# 第一根柱子是销售额最高的渠道
bar_colors = [
    "#F2A104",
    "#2878B5",
    "#2878B5",
]

# 柱子高度
bars = ax.bar(
    plot_data["channel"],
    plot_data["sales_quantity"],
    color=bar_colors,
    width=0.6,
)

ax.set_title("各渠道有效订单销量", fontsize=16)

ax.set_xlabel("销售渠道")
ax.set_ylabel("销量（件）")

# 柱状图比较绝对数值时，纵轴应该从0开始
ax.set_ylim(
    0,
    plot_data["sales_quantity"].max() * 1.2,
)

# 在每根柱子上方显示具体销售额
ax.bar_label(
    bars,
    fmt="%.0f",
    padding=3,
)

# 只保留横向辅助线
ax.grid(
    axis="y",
    linestyle="--",
    alpha=0.3,
)

# 去掉上方和右侧边框
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)


# =========================
# 5. 保存图片
# =========================

OUTPUT_FILE = (
    PROJECT_ROOT
    / "04_visualization"
    / "outputs"
    / "channel_quantity_bar_week8_day1.png"
)

# 计算本图包含的有效订单总数
valid_order_count = int(
    plot_data["order_count"].sum()
)

# 在图表底部添加数据范围说明
fig.text(
    0.5,
    0.01,
    f"数据范围：{valid_order_count}笔有效订单；销量为实际销售数量",
    ha="center",
    fontsize=10,
    color="#666666",
)

plt.tight_layout(
    rect=[0, 0.05, 1, 1]
)


plt.savefig(
    OUTPUT_FILE,
    dpi=150,
    bbox_inches="tight",
)

print("\n图表已生成：")
print(OUTPUT_FILE)

plt.show()