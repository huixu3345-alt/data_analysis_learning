"""Teacher-provided connection/display helper; the learner runs the SQL."""

from pathlib import Path
import sqlite3
import sys

import pandas as pd


def main():
    lesson_dir = Path(__file__).resolve().parent
    query_name = sys.argv[1] if len(sys.argv) > 1 else "refund_by_order.sql"
    query_path = lesson_dir / query_name
    sql = query_path.read_text(encoding="utf-8")
    db_path = lesson_dir / "inputs" / "course_sales_review.db"

    with sqlite3.connect(db_path.as_uri() + "?mode=ro", uri=True) as conn:
        result = pd.read_sql_query(sql, conn)

    print(result.to_string(index=False))
    print("Rows:", len(result))


if __name__ == "__main__":
    main()
