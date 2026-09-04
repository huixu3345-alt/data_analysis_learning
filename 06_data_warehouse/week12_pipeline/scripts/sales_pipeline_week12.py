from pathlib import Path
import sqlite3

import pandas as pd

WEEK12_DIR = Path(__file__).resolve().parents[1]
PROJECT_DIR = WEEK12_DIR.parent.parent

INPUT_FILE = PROJECT_DIR / "01_python_pandas" / "data" / "sales_dirty_week3.csv"
OUTPUT_DIR = WEEK12_DIR / "outputs"
DATABASE_FILE = OUTPUT_DIR / "sales_week12.db"

print("原始CSV存在：", INPUT_FILE.is_file())
print("输出目录存在：", OUTPUT_DIR.is_dir())
print("本周数据库路径：", DATABASE_FILE)

raw_df = pd.read_csv(
    INPUT_FILE,
    dtype="string",
    encoding="utf-8-sig",
)

print("\n原始数据行列数：", raw_df.shape)
print("\n前5行：")
print(raw_df.head().to_string(index=False))

# 建立清洗工作副本
df = raw_df.copy()

# 当前所有列都按字符串读取，逐列清理首尾空白
for column in df.columns:
    df[column] = df[column].str.strip()

# 对比清洗前后
print("\n清洗前城市：", raw_df["city"].head().tolist())
print("清洗后城市：", df["city"].head().tolist())
print("清洗后行列数：", df.shape)

# 删除完全重复的记录
before_count = len(df)

df = df.drop_duplicates().copy()

after_count = len(df)

print("\n去重前行数：", before_count)
print("去重后行数：", after_count)
print("删除的完全重复行数：", before_count - after_count)
print("剩余完全重复行数：", df.duplicated().sum())

# 保留转换前的日期文本，方便核对
df["order_date_raw"] = df["order_date"]

# 统一日期文本的写法
date_normalized = (
    df["order_date"]
    .str.replace("年", "-", regex=False)
    .str.replace("月", "-", regex=False)
    .str.replace("日", "", regex=False)
    .str.replace("/", "-", regex=False)
    .str.replace(".", "-", regex=False)
)

# 转换成日期类型
df["order_date"] = pd.to_datetime(
    date_normalized,
    format="%Y-%m-%d",
    errors="coerce",
)

# 查看转换结果
check_cols = ["order_id", "order_date_raw", "order_date"]

print("\n日期转换预览：")
print(df[check_cols].head())

print("\n无有效日期的订单：")
print(df.loc[df["order_date"].isna(), check_cols])

# 保留转换前的文本
df["quantity_raw"] = df["quantity"]
df["unit_price_raw"] = df["unit_price"]

# 数量：先去掉单位，再转换成数值
df["quantity"] = pd.to_numeric(
    df["quantity"].str.replace("件", "", regex=False),
    errors="coerce",
)

df["unit_price"] = pd.to_numeric(
    df["unit_price"].str.replace("元", "", regex=False),
    errors="coerce",
)

numeric_cols = [
    "order_id", "quantity_raw", "quantity",
    "unit_price_raw", "unit_price"
]

print("\n数量和单价转换预览：")
print(df[numeric_cols].head())

print("\n转换后缺失数量：")
print(df[["quantity", "unit_price"]].isna().sum())

# 保留转换前的折扣文本
df["discount_rate_raw"] = df["discount_rate"]

discount_text = df["discount_rate_raw"].replace("无折扣", "0")

# 先记住哪些记录原本带百分号
is_percentage = discount_text.str.endswith("%", na=False)

# 去掉百分号，转为能保存小数和缺失值的数值类型
df["discount_rate"] = pd.to_numeric(
    discount_text.str.replace("%", "", regex=False),
    errors="coerce",
).astype("Float64")

# 只有原本带百分号的记录才除以100
df.loc[is_percentage, "discount_rate"] = (
    df.loc[is_percentage, "discount_rate"] / 100
)

discount_cols = ["order_id", "discount_rate_raw", "discount_rate"]

print("\n折扣率转换预览：")
print(df[discount_cols].head(10))

print("折扣缺失数量：", df["discount_rate"].isna().sum())

# 练习假设：原始缺失的折扣暂按0处理
df["discount_assumed_zero"] = df["discount_rate_raw"].isna()

df.loc[df["discount_assumed_zero"], "discount_rate"] = 0

# 检查哪些订单采用了假设
assumption_cols = [
    "order_id", "discount_rate_raw",
    "discount_rate", "discount_assumed_zero"
]

print("\n采用折扣假设的订单：")
print(df.loc[df["discount_assumed_zero"], assumption_cols])

print("采用假设的订单数：", df["discount_assumed_zero"].sum())
print("处理后折扣缺失数量：", df["discount_rate"].isna().sum())

df["sales_amount_valid"] = (
    (df["order_status"] == "已完成")
    & df["quantity"].notnull()
    & df["unit_price"].notnull()
    & df["discount_rate"].notnull()
)

print("\n当前订单总数：", len(df))
print("可计入销售分析：", df["sales_amount_valid"].sum())
print("不计入销售分析：", (~df["sales_amount_valid"]).sum())

check_cols = ["order_id", "order_status", "quantity", "unit_price"]

print("\n不计入销售分析的订单：")
print(df.loc[~df["sales_amount_valid"], check_cols])

# 计算折前销售额、净销售额
df["gross_sales"] = df["quantity"] * df["unit_price"]
df["net_sales"] = df["gross_sales"] * (1 - df["discount_rate"])

# 本练习口径：取消订单的正式销售额记为0
is_cancelled = df["order_status"] == "已取消"
df.loc[is_cancelled, ["gross_sales", "net_sales"]] = 0

# 查看4笔典型订单
amount_cols = ["order_id", "gross_sales", "net_sales"]
check_orders = df["order_id"].isin(["O1001", "O1005", "O1010", "O1011"])

print("\n金额检查：")
print(df.loc[check_orders, amount_cols])

# 只汇总符合正式分析条件的订单
total_net_sales = df.loc[df["sales_amount_valid"], "net_sales"].sum()
print("有效订单净销售额合计：", round(total_net_sales, 2))

CLEAN_FILE = OUTPUT_DIR / "sales_clean_week12.csv"

df.to_csv(
    CLEAN_FILE,
    index=False,             # 不把DataFrame行索引另存为一列
    encoding="utf-8-sig",     # 便于Excel识别中文
    date_format="%Y-%m-%d",   # 统一写出的日期格式
)

print("\n清洗文件路径：", CLEAN_FILE)
print("导出行列数：", df.shape)
print("文件已生成：", CLEAN_FILE.is_file())

# 重新读取已保存的清洗CSV，作为入库数据
db_df = pd.read_csv(
    CLEAN_FILE,
    encoding="utf-8-sig",
)

# 全量刷新本周数据库中的sales_orders表
with sqlite3.connect(DATABASE_FILE) as connection:
    db_df.to_sql(
        "sales_orders",
        connection,
        if_exists="replace",
        index=False,
    )

    database_row_count = connection.execute(
        "SELECT COUNT(*) FROM sales_orders"
    ).fetchone()[0]

    table_info = connection.execute(
        "PRAGMA table_info(sales_orders)"
    ).fetchall()

    valid_summary = connection.execute(
        """
        SELECT
            COUNT(*) AS valid_order_count,
            ROUND(SUM(net_sales), 2) AS valid_net_sales
        FROM sales_orders
        WHERE sales_amount_valid = 1
        """
    ).fetchone()

    channel_summary = pd.read_sql_query(
        """
        SELECT
            channel,
            COUNT(*) AS valid_order_count,
            ROUND(SUM(net_sales), 2) AS valid_net_sales
        FROM sales_orders
        WHERE sales_amount_valid = 1
        GROUP BY channel
        ORDER BY valid_net_sales DESC
        """,
        connection,
    )

print("\n入库源行列数：", db_df.shape)
print("数据库文件已生成：", DATABASE_FILE.is_file())
print("sales_orders行数：", database_row_count)
print("sales_orders字段数：", len(table_info))

print("数据库有效订单数：", valid_summary[0])
print("数据库有效净销售额：", valid_summary[1])

print("\n渠道分析结果：")
print(channel_summary.to_string(index=False))

channel_total = round(channel_summary["valid_net_sales"].sum(), 2)
print("渠道净销售额合计：", channel_total)

ANALYSIS_FILE = OUTPUT_DIR / "channel_summary_week12.csv"

channel_summary.to_csv(
    ANALYSIS_FILE,
    index=False,
    encoding="utf-8-sig",
)

print("\n分析文件路径：", ANALYSIS_FILE)
print("分析结果行列数：", channel_summary.shape)
print("分析文件已生成：", ANALYSIS_FILE.is_file())