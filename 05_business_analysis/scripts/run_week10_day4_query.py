from pathlib import Path
import sqlite3
import sys


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


SCRIPT_FILE = Path(__file__).resolve()
WEEK10_DIR = SCRIPT_FILE.parent.parent
QUERY_FILE = (
    WEEK10_DIR
    / "queries"
    / "rfm_segmentation_week10_day4.sql"
)
EXPECTED_USER_COUNT = 10
EXPECTED_MONETARY = 15700.00

sql_text = QUERY_FILE.read_text(encoding="utf-8")

with sqlite3.connect(":memory:") as connection:
    cursor = connection.execute(sql_text)
    columns = [item[0] for item in cursor.description]
    rows = cursor.fetchall()


def print_table(column_names, table_rows):
    widths = [len(name) for name in column_names]
    for row in table_rows:
        for index, value in enumerate(row):
            widths[index] = max(widths[index], len(str(value)))

    print(
        "  ".join(
            name.ljust(widths[index])
            for index, name in enumerate(column_names)
        )
    )
    for row in table_rows:
        print(
            "  ".join(
                str(value).ljust(widths[index])
                for index, value in enumerate(row)
            )
        )


total_user_count = sum(row[1] for row in rows)
total_monetary = round(sum(row[2] for row in rows), 2)
total_share = round(sum(row[3] for row in rows), 2)

user_count_check = total_user_count == EXPECTED_USER_COUNT
monetary_check = abs(total_monetary - EXPECTED_MONETARY) < 0.01
share_check = abs(total_share - 100.0) <= 0.01
share_formula_check = all(
    abs(
        row[3]
        - round(row[2] * 100.0 / total_monetary, 2)
    )
    <= 0.01
    for row in rows
)

print("===== RFM 用户分层结果 =====")
print_table(columns, rows)
print("\n===== 验证 =====")
print("各分层用户数合计等于分析用户总数：", user_count_check)
print("各分层消费金额合计等于有效订单总金额：", monetary_check)
print("各分层金额贡献率合计约等于 100%：", share_check)
print("各分层金额贡献率与对照计算一致：", share_formula_check)
