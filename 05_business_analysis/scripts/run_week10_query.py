from pathlib import Path
import sqlite3

import pandas as pd


SCRIPT_FILE = Path(__file__).resolve()
WEEK10_DIR = SCRIPT_FILE.parent.parent
PROJECT_DIR = WEEK10_DIR.parent

DATABASE_FILE = PROJECT_DIR / "02_sql" / "data" / "sales_week4.db"
QUERY_FILE = (
    WEEK10_DIR
    / "queries"
    / "channel_sales_share_week10_day1.sql"
)

sql_text = QUERY_FILE.read_text(encoding="utf-8")

with sqlite3.connect(DATABASE_FILE) as connection:
    result_df = pd.read_sql_query(sql_text, connection)

print("===== 执行的 SQL =====")
print(sql_text)
print("\n===== 查询结果 =====")
print(result_df.to_string(index=False))
print("\n返回行数：", len(result_df))
print("贡献率合计：", round(result_df["channel_rate"].sum(), 2))
