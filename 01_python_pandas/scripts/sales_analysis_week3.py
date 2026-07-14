from pathlib import Path

import pandas as pd


# 1. 确定项目路径
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "outputs"

INPUT_FILE = DATA_DIR / "sales_dirty_week3.csv"

OUTPUT_DIR.mkdir(exist_ok=True)


# 2. 按字符串读取原始数据
raw_df = pd.read_csv(
    INPUT_FILE,
    dtype="string"
)


# 3. 初步检查原始数据
print("===== 原始数据概况 =====")
print("数据行数：", len(raw_df))
print("数据列数：", len(raw_df.columns))

print("\n===== 前5行 =====")
print(raw_df.head())

print("\n===== 字段类型 =====")
print(raw_df.dtypes)

print("\n===== 各字段缺失数量 =====")
print(raw_df.isna().sum())

print("\n===== 重复检查 =====")
print("整行重复数量：", raw_df.duplicated().sum())
print(
    "订单编号重复数量：",
    raw_df["order_id"].duplicated().sum()
)

# 4. 建立清洗工作副本
df = raw_df.copy()


# 5. 统一文本字段的前后空格
for column in df.columns:
    df[column] = (
        df[column]
        .astype("string")
        .str.strip()
    )


# 6. 删除完全重复的订单记录
before_dedup_count = len(df)

df = df.drop_duplicates().copy()

after_dedup_count = len(df)
removed_duplicate_count = (
    before_dedup_count - after_dedup_count
)

print("\n===== 基础清洗结果 =====")
print("删除重复记录前：", before_dedup_count)
print("删除重复记录后：", after_dedup_count)
print("删除的完全重复记录：", removed_duplicate_count)

print("\n清洗后订单编号重复数量：")
print(df["order_id"].duplicated().sum())

# 7. 保留需要转换的原始字段
df["order_date_raw"] = df["order_date"]
df["quantity_raw"] = df["quantity"]
df["unit_price_raw"] = df["unit_price"]
df["discount_rate_raw"] = df["discount_rate"]


# 8. 日期字段标准化与转换
date_normalized = (
    df["order_date"]
    .str.replace("年", "-", regex=False)
    .str.replace("月", "-", regex=False)
    .str.replace("日", "", regex=False)
    .str.replace("/", "-", regex=False)
    .str.replace(".", "-", regex=False)
)

df["order_date"] = pd.to_datetime(
    date_normalized,
    errors="coerce"
)

invalid_date_rows = df[
    df["order_date_raw"].notna() &
    df["order_date"].isna()
][
    ["order_id", "order_date_raw"]
]


# 9. 销量转换
quantity_normalized = (
    df["quantity"]
    .str.replace("件", "", regex=False)
)

df["quantity"] = pd.to_numeric(
    quantity_normalized,
    errors="coerce"
)

invalid_quantity_rows = df[
    df["quantity_raw"].notna() &
    df["quantity"].isna()
][
    ["order_id", "quantity_raw"]
]


# 10. 单价转换
unit_price_normalized = (
    df["unit_price"]
    .str.replace("元", "", regex=False)
)

df["unit_price"] = pd.to_numeric(
    unit_price_normalized,
    errors="coerce"
)

invalid_price_rows = df[
    df["unit_price_raw"].notna() &
    df["unit_price"].isna()
][
    ["order_id", "unit_price_raw"]
]


# 11. 折扣率转换
discount_text = (
    df["discount_rate"]
    .replace("无折扣", "0")
)

is_percentage = discount_text.str.endswith(
    "%",
    na=False
)

discount_number = pd.to_numeric(
    discount_text.str.replace(
        "%",
        "",
        regex=False
    ),
    errors="coerce"
)

df["discount_rate"] = discount_number.where(
    ~is_percentage,
    discount_number / 100
)


# 12. 输出转换失败记录
print("\n===== 日期转换失败记录 =====")
print(invalid_date_rows)

print("\n===== 销量转换失败记录 =====")
print(invalid_quantity_rows)

print("\n===== 单价转换失败记录 =====")
print(invalid_price_rows)

print("\n===== 转换后的字段类型 =====")
print(
    df[
        [
            "order_date",
            "quantity",
            "unit_price",
            "discount_rate",
        ]
    ].dtypes
)

# 13. 记录折扣缺失并按练习假设填充
missing_discount_count = int(
    df["discount_rate"].isna().sum()
)

df["discount_rate"] = (
    df["discount_rate"].fillna(0)
)


# 14. 创建数据质量标记
df["has_valid_date"] = (
    df["order_date"].notna()
)

df["has_valid_quantity"] = (
    df["quantity"].notna()
)

df["has_valid_price"] = (
    df["unit_price"].notna()
)

df["is_completed"] = (
    df["order_status"] == "已完成"
)


# 15. 提取订单月份
df["order_month"] = (
    df["order_date"]
    .dt.strftime("%Y-%m")
)


# 16. 计算折前与实付销售额
df["gross_sales"] = (
    df["quantity"] *
    df["unit_price"]
)

df["net_sales"] = (
    df["gross_sales"] *
    (1 - df["discount_rate"])
)


# 17. 取消订单的正式销售额记为0
df.loc[
    ~df["is_completed"],
    ["gross_sales", "net_sales"]
] = 0


# 18. 标记销售额是否可用于正式分析
df["sales_amount_valid"] = (
    df["is_completed"] &
    df["quantity"].notna() &
    df["unit_price"].notna() &
    df["discount_rate"].notna()
)


print("\n===== 业务指标检查 =====")
print("折扣缺失并暂按0处理：", missing_discount_count)
print("有效日期记录：", df["has_valid_date"].sum())
print("已完成订单：", df["is_completed"].sum())
print(
    "已完成但销售额无法计算：",
    (
        df["is_completed"] &
        df["net_sales"].isna()
    ).sum()
)

print("\n===== 订单指标预览 =====")
print(
    df[
        [
            "order_id",
            "order_status",
            "quantity",
            "unit_price",
            "discount_rate",
            "gross_sales",
            "net_sales",
            "sales_amount_valid",
        ]
    ]
)

# 19. 准备正式销售分析数据
valid_sales_df = df[
    df["sales_amount_valid"]
].copy()

monthly_sales_df = valid_sales_df[
    valid_sales_df["has_valid_date"]
].copy()


# 20. 保存清洗结果
CLEAN_OUTPUT_FILE = (
    OUTPUT_DIR / "sales_clean_week3.csv"
)

VALID_SALES_OUTPUT_FILE = (
    OUTPUT_DIR / "sales_valid_analysis_week3.csv"
)

df.to_csv(
    CLEAN_OUTPUT_FILE,
    index=False,
    encoding="utf-8-sig",
)

valid_sales_df.to_csv(
    VALID_SALES_OUTPUT_FILE,
    index=False,
    encoding="utf-8-sig",
)


print("\n===== 分析数据范围 =====")
print("去重后的全部订单：", len(df))
print("正式销售分析订单：", len(valid_sales_df))
print("月份分析订单：", len(monthly_sales_df))

print("\n已生成：")
print(CLEAN_OUTPUT_FILE)
print(VALID_SALES_OUTPUT_FILE)

# 21. 按月份和商品统计销量
monthly_product_summary = (
    monthly_sales_df
    .groupby(
        ["order_month", "product_name"],
        as_index=False,
    )
    .agg(
        sales_quantity=("quantity", "sum"),
        net_sales=("net_sales", "sum"),
    )
)

monthly_product_summary["net_sales"] = (
    monthly_product_summary["net_sales"]
    .round(2)
)


# 22. 找出每个月销量最高的商品
top_product_index = (
    monthly_product_summary
    .groupby("order_month")["sales_quantity"]
    .idxmax()
)

monthly_top_product = (
    monthly_product_summary
    .loc[top_product_index]
    .sort_values("order_month")
    .reset_index(drop=True)
)

print("\n===== 每月销量最高商品 =====")
print(monthly_top_product)

# 23. 按月份统计销售表现
monthly_sales_summary = (
    monthly_sales_df
    .groupby(
        "order_month",
        as_index=False,
    )
    .agg(
        order_count=("order_id", "nunique"),
        sales_quantity=("quantity", "sum"),
        gross_sales=("gross_sales", "sum"),
        net_sales=("net_sales", "sum"),
    )
    .sort_values(
        "net_sales",
        ascending=False,
    )
)

monthly_sales_summary[
    ["gross_sales", "net_sales"]
] = (
    monthly_sales_summary[
        ["gross_sales", "net_sales"]
    ]
    .round(2)
)

print("\n===== 月度销售表现 =====")
print(monthly_sales_summary)

# 24. 按城市统计销售表现
city_sales_summary = (
    valid_sales_df
    .groupby(
        "city",
        as_index=False,
        dropna=False,
    )
    .agg(
        order_count=("order_id", "nunique"),
        sales_quantity=("quantity", "sum"),
        net_sales=("net_sales", "sum"),
    )
    .sort_values(
        "net_sales",
        ascending=False,
    )
)

city_sales_summary["net_sales"] = (
    city_sales_summary["net_sales"].round(2)
)


# 25. 按渠道统计销售表现
channel_sales_summary = (
    valid_sales_df
    .groupby(
        "channel",
        as_index=False,
        dropna=False,
    )
    .agg(
        order_count=("order_id", "nunique"),
        sales_quantity=("quantity", "sum"),
        net_sales=("net_sales", "sum"),
    )
    .sort_values(
        "net_sales",
        ascending=False,
    )
)

channel_sales_summary["net_sales"] = (
    channel_sales_summary["net_sales"].round(2)
)


print("\n===== 城市销售表现 =====")
print(city_sales_summary)

print("\n===== 渠道销售表现 =====")
print(channel_sales_summary)

# 26. 汇总结果完整性核对
overall_net_sales = round(
    valid_sales_df["net_sales"].sum(),
    2,
)

city_net_sales_total = round(
    city_sales_summary["net_sales"].sum(),
    2,
)

channel_net_sales_total = round(
    channel_sales_summary["net_sales"].sum(),
    2,
)

print("\n===== 销售额完整性核对 =====")
print("有效订单总销售额：", overall_net_sales)
print("城市汇总销售额：", city_net_sales_total)
print("渠道汇总销售额：", channel_net_sales_total)

# 27. 保存业务分析结果
MONTHLY_TOP_PRODUCT_FILE = (
    OUTPUT_DIR / "monthly_top_product_week3.csv"
)

MONTHLY_SALES_FILE = (
    OUTPUT_DIR / "monthly_sales_summary_week3.csv"
)

CITY_SALES_FILE = (
    OUTPUT_DIR / "city_sales_summary_week3.csv"
)

CHANNEL_SALES_FILE = (
    OUTPUT_DIR / "channel_sales_summary_week3.csv"
)


monthly_top_product.to_csv(
    MONTHLY_TOP_PRODUCT_FILE,
    index=False,
    encoding="utf-8-sig",
)

monthly_sales_summary.to_csv(
    MONTHLY_SALES_FILE,
    index=False,
    encoding="utf-8-sig",
)

city_sales_summary.to_csv(
    CITY_SALES_FILE,
    index=False,
    encoding="utf-8-sig",
)

channel_sales_summary.to_csv(
    CHANNEL_SALES_FILE,
    index=False,
    encoding="utf-8-sig",
)


print("\n===== 已生成业务分析结果 =====")
print(MONTHLY_TOP_PRODUCT_FILE)
print(MONTHLY_SALES_FILE)
print(CITY_SALES_FILE)
print(CHANNEL_SALES_FILE)

# 28. 计算报告所需指标
valid_date_sales_count = len(monthly_sales_df)

monthly_coverage_rate = round(
    valid_date_sales_count /
    len(valid_sales_df) *
    100,
    2,
)

missing_city_order_count = int(
    valid_sales_df["city"].isna().sum()
)

missing_city_sales = round(
    valid_sales_df.loc[
        valid_sales_df["city"].isna(),
        "net_sales",
    ].sum(),
    2,
)

top_month_row = monthly_sales_summary.iloc[0]
top_city_row = city_sales_summary[
    city_sales_summary["city"].notna()
].iloc[0]
top_channel_row = channel_sales_summary.iloc[0]


# 29. 生成销售分析报告
report_text = f"""# 第3周销售数据综合分析报告

## 1. 分析背景

本项目使用2026年第一季度模拟电商订单数据，完成从原始数据检查、数据清洗、指标计算、分组分析到业务结论输出的完整流程。

## 2. 核心业务问题

1. 每个月哪个商品销量最高？
2. 哪个月实付销售额最高？
3. 不同城市和销售渠道的销售额、销量有什么差异？

## 3. 指标口径

- 折前销售额 = 销量 × 商品单价
- 实付销售额 = 折前销售额 ×（1 - 折扣率）
- 正式销售订单 = 订单状态为“已完成”，且销量、单价和折扣率可以用于计算
- 取消订单保留用于数据质量和取消情况分析，但正式销售额记为0

## 4. 数据清洗结果

- 原始订单数量：{len(raw_df)}
- 删除完全重复记录：{removed_duplicate_count}
- 去重后订单数量：{len(df)}
- 已完成订单数量：{int(df["is_completed"].sum())}
- 正式销售分析订单数量：{len(valid_sales_df)}
- 月份分析订单数量：{len(monthly_sales_df)}
- 月份分析覆盖率：{monthly_coverage_rate}%

发现的主要数据质量问题：

1. 2条非空日期无法转换，另有1条原始日期为空。
2. 1条销量“缺货”无法转换，另有1条销量为空。
3. 1条已完成订单的单价为“价格待定”，暂不计入正式销售额分析。
4. 1条折扣为空，本练习暂按无折扣处理，但该假设需要业务确认。
5. 1条有效销售订单缺少城市信息。

## 5. 核心结果

### 5.1 总体表现

- 有效销售订单总实付销售额：{overall_net_sales:.2f}元
- 城市汇总与渠道汇总均能回算到总体销售额，完整性核对通过。

### 5.2 每月销量最高商品

- 2026年1月：无线鼠标，销量7件。
- 2026年2月：无线鼠标，销量6件。
- 2026年3月：蓝牙耳机，销量9件。

### 5.3 月度销售表现

在具有有效日期的销售订单中，{top_month_row["order_month"]}实付销售额最高，为{top_month_row["net_sales"]:.2f}元。

### 5.4 城市销售表现

已知城市中，{top_city_row["city"]}实付销售额最高，为{top_city_row["net_sales"]:.2f}元。

有{missing_city_order_count}笔有效销售订单缺少城市信息，涉及实付销售额{missing_city_sales:.2f}元，因此城市归属仍不完整。

### 5.5 渠道销售表现

{top_channel_row["channel"]}渠道实付销售额最高，为{top_channel_row["net_sales"]:.2f}元，销量为{int(top_channel_row["sales_quantity"])}件。

## 6. 分析限制

1. 本项目为小规模模拟数据，不能据此推断长期稳定趋势。
2. 月份分析只覆盖{monthly_coverage_rate}%的正式销售订单，无有效日期的订单未进入月度统计。
3. 城市字段存在缺失，北京只能称为“已知城市中”销售额最高。
4. 折扣空值暂按0处理属于分析假设，需要业务人员确认。
5. 单价“价格待定”的已完成订单未计入销售额，可能造成整体销售额低估。

## 7. 业务建议

1. 优先回查无效日期、缺失城市和价格待定订单，完善数据后重新运行分析。
2. 继续观察无线鼠标和蓝牙耳机的月度销量，结合库存与利润判断补货策略。
3. 进一步拆解天猫渠道的商品结构、折扣和订单量，判断其高销售额来源。
4. 扩大数据时间范围后，再判断月份、城市和渠道表现是否具有稳定性。
"""

REPORT_OUTPUT_FILE = (
    OUTPUT_DIR / "sales_analysis_report_week3.md"
)

REPORT_OUTPUT_FILE.write_text(
    report_text,
    encoding="utf-8",
)

print("\n===== 已生成销售分析报告 =====")
print(REPORT_OUTPUT_FILE)