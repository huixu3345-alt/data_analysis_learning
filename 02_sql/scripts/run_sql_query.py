from pathlib import Path
import sqlite3

import pandas as pd

pd.set_option(
    "display.max_columns",
    None,
)

pd.set_option(
    "display.width",
    120,
)


# 当前脚本所在位置：
# D:\data_analysis_learning\02_sql\scripts\run_sql_query.py
SCRIPT_FILE = Path(__file__).resolve()

# 当前脚本所在文件夹：
# D:\data_analysis_learning\02_sql\scripts
SCRIPTS_DIR = SCRIPT_FILE.parent

# scripts 的上一级就是 02_sql
# D:\data_analysis_learning\02_sql
SQL_DIR = SCRIPTS_DIR.parent


# 数据库文件路径
DATABASE_FILE = (
    SQL_DIR
    / "data"
    / "sales_week4.db"
)


# 修改这个变量，就可以选择要运行的SQL文件
QUERY_FILE_NAME = "47_day2_window_practice.sql"

QUERY_FILE = (
    SQL_DIR
    / "queries"
    / QUERY_FILE_NAME
)

# 读取SQL文件中的文字
sql_text = QUERY_FILE.read_text(
    encoding="utf-8"
)


# 连接数据库并执行SQL
with sqlite3.connect(DATABASE_FILE) as connection:
    result_df = pd.read_sql_query(
        sql_text,
        connection,
    )


# 显示SQL语句
print("===== 执行的SQL =====")
print(sql_text)


# 显示查询结果
print("\n===== 查询结果 =====")
print(result_df)


# 显示查询返回多少行
print("\n返回行数：", len(result_df))