from pathlib import Path
import sqlite3


SQL_DIR = Path(__file__).resolve().parents[1]
DATABASE_FILE = SQL_DIR / "data" / "sales_week4.db"


user_order_data = [
    ("UO001", "U001", "2026-01-05", "2026-01", "已完成", 300.00),
    ("UO002", "U001", "2026-02-10", "2026-02", "已完成", 450.00),
    ("UO003", "U001", "2026-03-12", "2026-03", "已完成", 500.00),

    ("UO004", "U002", "2026-01-08", "2026-01", "已完成", 280.00),
    ("UO005", "U002", "2026-01-20", "2026-01", "已完成", 320.00),
    ("UO006", "U002", "2026-03-15", "2026-03", "已完成", 600.00),

    ("UO007", "U003", "2026-01-12", "2026-01", "已完成", 260.00),
    ("UO008", "U003", "2026-02-06", "2026-02", "已取消", 350.00),

    ("UO009", "U004", "2026-02-03", "2026-02", "已完成", 400.00),
    ("UO010", "U004", "2026-03-20", "2026-03", "已完成", 550.00),

    ("UO011", "U005", "2026-02-08", "2026-02", "已完成", 380.00),
    ("UO012", "U005", "2026-03-18", "2026-03", "已取消", 420.00),

    ("UO013", "U006", "2026-02-18", "2026-02", "已完成", 480.00),
    ("UO014", "U006", "2026-03-25", "2026-03", "已完成", 650.00),

    ("UO015", "U007", "2026-03-02", "2026-03", "已完成", 360.00),

    ("UO016", "U008", "2026-03-05", "2026-03", "已完成", 420.00),
    ("UO017", "U008", "2026-03-28", "2026-03", "已完成", 520.00),
]


with sqlite3.connect(DATABASE_FILE) as conn:
    conn.execute("DROP TABLE IF EXISTS user_orders")

    conn.execute(
        """
        CREATE TABLE user_orders (
            user_order_id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            order_date TEXT NOT NULL,
            order_month TEXT NOT NULL,
            order_status TEXT NOT NULL,
            net_sales REAL
        )
        """
    )

    conn.executemany(
        """
        INSERT INTO user_orders (
            user_order_id,
            user_id,
            order_date,
            order_month,
            order_status,
            net_sales
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        user_order_data,
    )

    conn.commit()

    row_count = conn.execute(
        "SELECT COUNT(*) FROM user_orders"
    ).fetchone()[0]


print("用户订单表创建完成")
print("数据库：", DATABASE_FILE)
print("订单记录数：", row_count)