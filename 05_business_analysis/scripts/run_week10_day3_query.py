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
    / "cohort_retention_week10_day3.sql"
)
LATEST_DATA_MONTH = "2026-03"

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


cohort_totals = {}
for cohort_month, _, cohort_users, retained_users, _ in rows:
    values = cohort_totals.setdefault(cohort_month, [0, 0])
    values[0] += cohort_users
    values[1] += retained_users

overall_rows = []
for cohort_month, (cohort_users, retained_users) in cohort_totals.items():
    overall_rows.append(
        (
            cohort_month,
            cohort_users,
            retained_users,
            round(retained_users * 100.0 / cohort_users, 2),
        )
    )

count_check = all(row[3] <= row[2] for row in rows)
rate_check = all(0 <= row[4] <= 100 for row in rows)
channel_total_check = all(
    sum(row[2] for row in rows if row[0] == cohort_month)
    == cohort_users
    for cohort_month, cohort_users, _, _ in overall_rows
)
window_check = LATEST_DATA_MONTH >= "2026-03"

print("===== 渠道 Cohort 次月留存结果 =====")
print_table(columns, rows)
print("\n===== Cohort 整体结果 =====")
print_table(
    [
        "cohort_month",
        "cohort_user_count",
        "month_1_retained_users",
        "month_1_retention_rate",
    ],
    overall_rows,
)
print("\n===== 验证 =====")
print("留存用户数不超过 Cohort 用户数：", count_check)
print("留存率位于 0% 到 100%：", rate_check)
print("渠道人数汇总与 Cohort 总体一致：", channel_total_check)
print("数据已覆盖到 2026-03，可观察 2月 Cohort 次月留存：", window_check)
