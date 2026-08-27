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
    / "channel_funnel_week10_day2.sql"
)

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

    header = "  ".join(
        name.ljust(widths[index])
        for index, name in enumerate(column_names)
    )
    print(header)
    for row in table_rows:
        print(
            "  ".join(
                str(value).ljust(widths[index])
                for index, value in enumerate(row)
            )
        )


monthly_totals = {}
for visit_month, _, visit_count, cart_count, _ in rows:
    month_values = monthly_totals.setdefault(visit_month, [0, 0])
    month_values[0] += visit_count
    month_values[1] += cart_count

monthly_rows = []
for visit_month, (visit_count, cart_count) in monthly_totals.items():
    monthly_rows.append(
        (
            visit_month,
            visit_count,
            cart_count,
            round(cart_count * 100.0 / visit_count, 2),
        )
    )

count_check = all(row[3] <= row[2] for row in rows)
rate_check = all(0 <= row[4] <= 100 for row in rows)

print("===== 渠道漏斗查询结果 =====")
print_table(columns, rows)
print("\n===== 月度整体结果 =====")
print_table(
    ["visit_month", "visit_count", "cart_count", "visit_to_cart_rate"],
    monthly_rows,
)
print("\n===== 验证 =====")
print("各组加购用户数不超过访问用户数：", count_check)
print("各组转化率位于 0% 到 100%：", rate_check)
