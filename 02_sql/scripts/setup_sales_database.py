from pathlib import Path
import sqlite3

import pandas as pd


# 1. 确定路径
SQL_DIR = Path(__file__).resolve().parents[1]
PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = (
    PROJECT_ROOT
    / "01_python_pandas"
    / "outputs"
    / "sales_clean_week3.csv"
)

DATABASE_FILE = (
    SQL_DIR
    / "data"
    / "sales_week4.db"
)

# 每次从空数据库开始创建，避免旧数据库内部状态影响结果
DATABASE_FILE.parent.mkdir(
    parents=True,
    exist_ok=True,
)

if DATABASE_FILE.exists():
    DATABASE_FILE.unlink()
    

# 2. 读取第3周清洗后的销售数据
df = pd.read_csv(INPUT_FILE)


# 3. 选择本周SQL练习需要的字段
sql_columns = [
    "order_id",
    "order_date",
    "city",
    "channel",
    "product_name",
    "category",
    "quantity",
    "unit_price",
    "discount_rate",
    "order_status",
    "order_month",
    "gross_sales",
    "net_sales",
    "sales_amount_valid",
]

orders_df = df[sql_columns].copy()


# 4. 写入SQLite数据库
with sqlite3.connect(DATABASE_FILE) as connection:
    orders_df.to_sql(
        "sales_orders",
        connection,
        if_exists="replace",
        index=False,
    )

    row_count = connection.execute(
        "SELECT COUNT(*) FROM sales_orders"
    ).fetchone()[0]

    table_info = connection.execute(
        "PRAGMA table_info(sales_orders)"
    ).fetchall()


# 5. 输出验证结果
print("SQLite数据库已创建：")
print(DATABASE_FILE)

print("\n数据表：sales_orders")
print("数据行数：", row_count)

print("\n字段结构：")
for column in table_info:
    print(column)